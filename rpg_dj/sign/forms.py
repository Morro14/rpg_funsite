from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model


class BaseRegisterForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ("username",
                  "email",
                  "role",
                  "password1",
                  "password2",)
