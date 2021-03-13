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
