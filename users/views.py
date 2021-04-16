import os
import requests
from django.views.generic import FormView, DetailView, UpdateView
from django.shortcuts import redirect, reverse
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import PasswordChangeView
from django.core.files.base import ContentFile
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from . import forms, models, mixins


class LoginView(mixins.LoggedOutOnlyView, FormView):
    template_name = "users/login.html"
    form_class = forms.LoginForm

    def form_valid(self, form):
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=email, password=password)
        if user is not None:
            is_verified_user = models.User.objects.get(email=email)
            if is_verified_user.email_verified is False:
                # not yet verified
                logout(self.request)
                return redirect(reverse("core:home"))
            else:
                login(self.request, user)
        return super().form_valid(form)

    def get_success_url(self):
        next_arg = self.request.GET.get("next")
        if next_arg is not None:
            return next_arg
        else:
            return reverse("core:home")


def log_out(request):
    messages.info(request, f"See you later {request.user.first_name}")
    logout(request)
    return redirect(reverse("core:home"))


class SignUpView(mixins.LoggedOutOnlyView, FormView):
    template_name = "users/signup.html"
    form_class = forms.SignUpForm
    success_url = reverse_lazy("core:home")

    def form_valid(self, form):
        # forms.py에서 만든 save() 함수
        form.save()
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password1")
        user = authenticate(self.request, username=email, password=password)
        if user is not None:
            login(self.request, user)
        # user.verify_email()
        user.email_verified = True
        return super().form_valid(form)


def complete_verification(request, key):
    try:
        user = models.User.objects.get(email_secret=key)
        user.email_verified = True
        user.email_secret = ""
        user.save()
        # TODO : add success message
    except models.User.DoesNotExist:
        # TODO : add error message
        pass
    return redirect(reverse("core:home"))


def github_login(request):
    client_id = os.environ.get("GITHUB_ID")
    redirect_uri = "http://127.0.0.1:8000/users/login/github/callback"
    return redirect(
        f"https://github.com/login/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&scope=read:user"
    )


class GithubException(Exception):
    pass


def github_callback(request):
    try:
        code = request.GET.get("code", None)
        client_id = os.environ.get("GITHUB_ID")
        client_secret = os.environ.get("GITHUB_SECRET")
        if code is not None:
            access_request = requests.post(
                f"https://github.com/login/oauth/access_token?client_id={client_id}&client_secret={client_secret}&code={code}",
                headers={"Accept": "application/json"},
            )
            access_json = access_request.json()
            error = access_json.get("error", None)
            if error is None:
                access_token = access_json.get("access_token", None)
                if access_token is not None:
                    profile_request = requests.get(
                        "https://api.github.com/user",
                        headers={
                            "Authorization": f"token {access_token}",
                            "Accept": "application/json",
                        },
                    )
                    profile_json = profile_request.json()
                    username = profile_json.get("login", None)
                    if username is not None:
                        name = profile_json.get('name')
                        email = profile_json.get('email')
                        bio = profile_json.get('bio')
                        if not name:
                            name = username
                        if not email:
                            email = f"{username}@github.com"
                        if not bio:
                            bio = "None"

                        # login 시 case 별로 분류
                        try:
                            # case1: User is not None (Already Exist)
                            user = models.User.objects.get(email=email)
                            if user.login_method != models.User.LOGIN_GITHUB:
                                # Already signup with Email or Kakao
                                raise GithubException(f"Please login with : {user.login_method}")
                        except models.User.DoesNotExist:
                            # case2: User is None (No that user) -> Create the User
                            user = models.User.objects.create(
                                email=email, first_name=name, username=email, bio=bio,
                                login_method=models.User.LOGIN_GITHUB
                            )
                            # Github 유저이므로 비번은 따로 생성 x (깃헙 계정 유저)
                            user.set_unusable_password()
                            user.save()
                        login(request, user)
                        messages.success(request, f"Welcome back {user.first_name}")
                        return redirect(reverse("core:home"))
                    else:
                        raise GithubException("Can't get your profile")
                else:
                    raise GithubException("Can't get Access code")
            else:
                raise GithubException("Error occurred")
        else:
            raise GithubException("Can't get Code")
    except GithubException as e:
        messages.error(request, e)
        return redirect(reverse("users:login"))


class KakaoException(Exception):
    pass


def kakao_login(request):
    REST_API_KEY = os.environ.get("KAKAO_KEY")
    REDIRECT_URI = "http://127.0.0.1:8000/users/login/kakao/callback"
    return redirect(
        f"https://kauth.kakao.com/oauth/authorize?client_id={REST_API_KEY}&redirect_uri={REDIRECT_URI}&response_type=code"
    )


def kakao_callback(request):
    KAKAO_ID = os.environ.get("KAKAO_KEY")
    REDIRECT_URI = "http://127.0.0.1:8000/users/login/kakao/callback"
    try:
        code = request.GET.get("code", None)
        if code is not None:
            token_request = requests.get(
                f"https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={KAKAO_ID}&redirect_uri={REDIRECT_URI}&code={code}")
            token_json = token_request.json()
            error = token_json.get("error")
            if error is None:
                access_token = token_json.get("access_token")
                profile_request = requests.get(
                    f"https://kapi.kakao.com/v2/user/me",
                    headers={"Authorization": f"Bearer {access_token}"},
                )
                # print(profile_request.json())
                profile_json = profile_request.json()
                kakao_account = profile_json.get("kakao_account")
                email = kakao_account.get("email")

                # 이메일이 없다면 로그인 불가
                if email is None:
                    raise KakaoException("Please also give me email")
                else:
                    profile = kakao_account.get("profile")
                    profile_image = profile.get("profile_image_url")
                    nickname = profile.get("nickname")
                    try:
                        # 이메일이 있다면 로그인
                        user = models.User.objects.get(email=email)
                        if user.login_method != models.User.LOGIN_KAKAO:
                            # 해당 이메일이 이미 카톡이 아닌 다른 걸로 로그인 한 경우
                            raise KakaoException(f"Please log in with :{user.login_method}")
                    except models.User.DoesNotExist:
                        # 이메일이 없다면 해당 이메일로 계정 생성, 저장 후 로그인
                        user = models.User.objects.create(
                            email=email,
                            first_name=nickname,
                            login_method=models.User.LOGIN_KAKAO,
                            email_verified=True,
                            username=nickname,
                        )
                        user.set_unusable_password()
                        user.save()
                        if profile_image is not None:
                            photo_request = requests.get(profile_image)
                            user.avatar.save(
                                f"{nickname}-avatar", ContentFile(photo_request.content)
                            )
                    login(request, user)
                    messages.success(request, f"Welcome back {user.first_name}")
                    return redirect(reverse("core:home"))
            else:
                raise KakaoException("Can't get Authorization code")
        else:
            raise KakaoException("something went wrong")
    except KakaoException as e:
        messages.error(request, e)
        return redirect(reverse("users:login"))


class UserProfileView(DetailView):
    model = models.User
    context_object_name = 'user_obj'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class UpdatePasswordView(
    mixins.LoggedInOnlyView,
    mixins.EmailLoginOnlyView,
    SuccessMessageMixin,
    PasswordChangeView
):

    template_name = "users/update-password.html"
    success_message = "Password Updated"

    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)
        form.fields['old_password'].widget.attrs = {"placeholder": "Current password"}
        form.fields['new_password1'].widget.attrs = {"placeholder": "Change password"}
        form.fields['new_password2'].widget.attrs = {"placeholder": "Confirm password"}
        return form

    def get_success_url(self):
        return self.request.user.get_absolute_url()


class UpdateProfileView(
    mixins.LoggedInOnlyView,
    SuccessMessageMixin,
    UpdateView
):

    model = models.User
    template_name = "users/update-profile.html"
    fields = (
        "first_name",
        "last_name",
        "gender",
        "bio",
        "birthdate",
        "language",
        "currency",
    )
    success_message = "Profile Updated"

    def get_object(self, queryset=None):
        return self.request.user

    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)
        form.fields['first_name'].widget.attrs = {"placeholder": "First Name"}
        form.fields['last_name'].widget.attrs = {"placeholder": "Last Name"}
        form.fields['gender'].widget.attrs = {"placeholder": "Gender"}
        form.fields['bio'].widget.attrs = {"placeholder": "bio"}
        form.fields['birthdate'].widget.attrs = {"placeholder": "Birthdate (1990-01-01)"}
        form.fields['language'].widget.attrs = {"placeholder": "Language"}
        form.fields['currency'].widget.attrs = {"placeholder": "Currency"}
        return form

