from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import UserCreationForm
from . import models


class LoginForm(forms.Form):

    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

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
                self.add_error("password", forms.ValidationError("Password is wrong"))
        except models.User.DoesNotExist:
            self.add_error("email", forms.ValidationError("User does not exist"))


class SignUpForm(forms.ModelForm):

    class Meta:
        model = models.User
        fields = ("first_name", "last_name", "email")

    password1 = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput,
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label="Password confirmation",
        widget=forms.PasswordInput,
        strip=False,
        help_text="Enter the same password as before, for verification.",
    )

    # password = forms.CharField(widget=forms.PasswordInput)
    # password1 = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    # ModelForm을 사용함으로서 fields에 지정만 해주면 알아서 clean_data로 생성해준다

    # def clean_password1(self):
    #     password = self.cleaned_data.get("password")
    #     password1 = self.cleaned_data.get("password1")
    #     if password != password1:
    #         raise forms.ValidationError("Password confirmation does not match")
    #     else:
    #         return password

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Password confirmation does not match")
        else:
            return password2

    def save(self, *args, **kwargs):
        user = super().save(commit=False)
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password1")
        birthdate = self.cleaned_data.get("birthdate")

        user.username = email
        user.birthdate = birthdate
        user.set_password(password)
        user.save()
