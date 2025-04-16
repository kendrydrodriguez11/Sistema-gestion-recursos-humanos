from django import forms
from django.contrib.auth import password_validation
from django.forms import ModelForm
from apps.security.models import User
from django.core.exceptions import ValidationError


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "username",
            "password",
            "dni",
            "email",
            "sucursal",
            "groups",
            "image",
            "is_active"
        ]
    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        # Guarda el valor actual del campo como valor inicial
        self.fields['password'].initial = self.instance.password if self.instance else None


class MyPasswordChangeForm2(ModelForm):
    error_messages = {
        "password_mismatch": "The two password fields didn’t match.",
        "password_incorrect": "Your old password was entered incorrectly. Please enter it again.",
    }


    old_password = forms.CharField(
        label="Old password",
        strip=False,
        widget=forms.PasswordInput(
            attrs={"autocomplete": "current-password", "autofocus": True}
        ),
    )
    new_password1 = forms.CharField(
        label="New password",
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label="New password confirmation",
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
    )

    field_order = ["old_password", "new_password1", "new_password2"]

    class Meta:
        model = User
        fields = [
            "old_password",
            "new_password1",
            "new_password2",

        ]

    def clean_old_password(self):
        """
        Validate that the old_password field is correct.
        """
        old_password = self.cleaned_data["old_password"]
        if not self.instance.check_password(old_password):
            raise ValidationError(
                self.error_messages["password_incorrect"],
                code="password_incorrect",
            )
        return old_password

    """
       A form that lets a user set their password without entering the old
       password
       """

    def clean_new_password2(self):
        password1 = self.cleaned_data.get("new_password1")
        password2 = self.cleaned_data.get("new_password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError(
                self.error_messages["password_mismatch"],
                code="password_mismatch",
            )
        password_validation.validate_password(password2, self.instance)
        return password2

    def save(self, commit=True):
        password = self.cleaned_data["new_password1"]
        self.instance.set_password(password)
        if commit:
            self.instance.save()
        return self.instance