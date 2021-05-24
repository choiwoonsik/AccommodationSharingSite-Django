from django import forms
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import password_validation
from django.contrib.auth.forms import UserCreationForm
from . import models


class LoginForm(forms.Form):

    email = forms.EmailField(widget=forms.EmailInput(attrs={"placeholder": _("Email")}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": _("Password")})
    )

    # 변수를 확인하고 싶은 함수를 생성시 clean_변수명()으로 해야한다 - 장고규칙
    # 아니면 명명하지 않고 통합으로 할수도 있다
    # return 값을 주지 않으면 지워버린다
    def clean(self):

        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        try:
            user = models.User.objects.get(email=email)
            if user.check_password(password):
                return self.cleaned_data
            else:
                self.add_error("password", forms.ValidationError(_("Password is wrong")))
        except models.User.DoesNotExist:
            self.add_error("email", forms.ValidationError(_("User does not exist")))


class SignUpForm(forms.ModelForm):

    class Meta:
        model = models.User
        fields = ("first_name", "last_name", "email")
        widgets = {
            "first_name": forms.TextInput(attrs={"placeholder": _("First Name")}),
            "last_name": forms.TextInput(attrs={"placeholder": _("Last Name")}),
            "email": forms.EmailInput(attrs={"placeholder": _("Email")}),
        }

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": _("Password")})
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": _("Confirm Password")})
    )

    def clean_email(self):
        email = self.cleaned_data.get("email")
        try:
            models.User.objects.get(email=email)
            raise forms.ValidationError(
                _("That email is already taken"), code="existing_user"
            )
        except models.User.DoesNotExist:
            return email

    def clean_password1(self):
        password1 = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password1")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(_("Password confirmation does not match"))
        else:
            return password2

    def save(self, *args, **kwargs):
        user = super().save(commit=False)
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password1")
        birthdate = self.cleaned_data.get("birthdate")

        user.email_verified = True
        user.username = email
        user.birthdate = birthdate
        user.set_password(password)
        user.save()
