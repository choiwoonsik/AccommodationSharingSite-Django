from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.db import models
from django.core.mail import send_mail
from django.conf import settings
from django.utils.html import strip_tags
from django.template.loader import render_to_string
from core.models import TimeStampedModel
from django.shortcuts import reverse
from core import managers as core_managers
import uuid


# Django 기본 User를 상속받아서 오버라이드
class User(AbstractUser):

    """ Custom User Model """

    GENDER_MALE = "male"
    GENDER_FEMALE = "female"
    GENDER_OTHER = "other"

    GENDER_CHOICES = (
        (GENDER_MALE, _("Male")),
        (GENDER_FEMALE, _("Female")),
        (GENDER_OTHER, _("Other")),
    )

    LANGUAGE_ENGLISH = "en"
    LANGUAGE_KOREAN = "ko"

    LANGUAGE_CHOICES = (
        (LANGUAGE_ENGLISH, _("English")),
        (LANGUAGE_KOREAN, _("Korean")),
    )

    CURRENCY_USD = "usd"
    CURRENCY_KRW = "krw"

    CURRENCY_CHOICES = (
        (CURRENCY_USD, _("USD")),
        (CURRENCY_KRW, _("KRW")),
    )

    LOGIN_EMAIL = "email"
    LOGIN_GITHUB = "github"
    LOGIN_KAKAO = "kakao"

    LOGIN_CHOICES = (
        (LOGIN_EMAIL, _("Email")),
        (LOGIN_GITHUB, _("Github")),
        (LOGIN_KAKAO, _("Kakao")),
    )

    avatar = models.ImageField(_('avatar'), upload_to="avatars", blank=True)
    gender = models.CharField(_('gender'), choices=GENDER_CHOICES, max_length=10, default=GENDER_MALE)
    bio = models.TextField(_('bio'), blank=True)
    birthdate = models.DateField(_('birthdate'), blank=True, null=True)
    language = models.CharField(_('language'), choices=LANGUAGE_CHOICES, max_length=2, default=LANGUAGE_KOREAN)
    currency = models.CharField(_('currency'), choices=CURRENCY_CHOICES, max_length=3, default=CURRENCY_KRW)
    superhost = models.BooleanField(_('superhost'), default=False)
    email_verified = models.BooleanField(_('email_verified'), default=False)
    email_secret = models.CharField(_('email_secret'), max_length=6, default="", blank=True)
    login_method = models.CharField(_('login_method'), max_length=50, choices=LOGIN_CHOICES, default=LOGIN_EMAIL)
    # objects = core_managers.CustomModelManager()

    def get_absolute_url(self):
        return reverse("users:profile", kwargs={"pk": self.pk})

    def verify_email(self):
        if self.email_verified is False:
            secret = uuid.uuid4().hex[:6]
            self.email_secret = secret
            html_message = render_to_string(
                "emails/verify_email.html",
                {'secret': secret},
            )
            send_mail(
                _("Verify WooHome Account"),
                strip_tags(html_message),
                settings.EMAIL_FROM,
                [self.email],
                fail_silently=False,
                html_message=html_message,
            )
            self.save()
        return

