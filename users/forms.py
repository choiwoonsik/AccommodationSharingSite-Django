from django import forms
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

    birthdate = forms.DateField(initial="1900-00-00", help_text="1900-01-01")
    password = forms.CharField(widget=forms.PasswordInput)
    password1 = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    # ModelForm을 사용함으로서 fields에 지정만 해주면 알아서 clean_data로 생성해준다

    def clean_password1(self):
        password = self.cleaned_data.get("password")
        password1 = self.cleaned_data.get("password1")
        if password != password1:
            raise forms.ValidationError("Password confirmation does not match")
        else:
            return password

    def save(self, *args, **kwargs):
        user = super().save(commit=False)
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        birthdate = self.cleaned_data.get("birthdate")

        user.username = email
        user.birthdate = birthdate
        user.set_password(password)
        user.save()
