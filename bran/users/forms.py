# from captcha.fields import ReCaptchaField
# from captcha.widgets import ReCaptchaV2Checkbox
from django import forms
from django.contrib.auth import password_validation, authenticate, get_user_model
from django.core.exceptions import ValidationError
from django.forms import PasswordInput, formset_factory
from django.contrib.auth.forms import (
    PasswordResetForm as PasswordResetEmail, PasswordChangeForm,
)

from django.utils.translation import gettext_lazy as _


User = get_user_model()


class RegisterForm(forms.ModelForm):
    email = forms.CharField(
        label='Email',
        required=True,
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Email address',
            }
        )
    )
    password1 = forms.CharField(
        label=_('Password'),
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': _('Password'),
            }
        )
    )
    password2 = forms.CharField(
        label=_('Confirm password'),
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': _('Confirm password'),
            }
        )
    )
    check = forms.BooleanField(
        required=True,
        widget=forms.CheckboxInput(
            attrs={
                'class': 'form-check-input'
            }
        )
    )
    # captcha = ReCaptchaField(
    #     widget=ReCaptchaV2Checkbox(
    #         attrs={
    #             'class': 'form-check-input'
    #         }
    #     )
    # )

    def clean_email(self):
        email = self.cleaned_data.get('email')

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('This email is already used.')

        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 != password2:
            raise forms.ValidationError('The passwords do not match.')

        password_validation.validate_password(password2)

        return password2

    def save(self, *args, **kwargs):
        user = super().save(commit=True)
        user.set_password(self.cleaned_data.get('password2'))
        user.save()

        return user

    class Meta:
        model = User
        fields = [
            'email',
        ]


class LoginForm(forms.Form):
    email = forms.CharField(
        label='Email',
        required=True,
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Email address',
                'autofocus': 'autofocus'
            }
        )
    )
    password = forms.CharField(
        label='Password',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Password'
            }
        )
    )

    def clean(self):
        super().clean()
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        user = authenticate(email=email, password=password)

        if not user:
            self.add_error('email', '')
            self.add_error('password', '')
            raise forms.ValidationError('Invalid login details.')

        self.cached_user = user

        return self.cleaned_data

    def get_user(self):
        return self.cached_user


class PasswordResetForm(forms.Form):
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Password'
            }
        )
    )
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Repeat password'
            }
        )
    )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def clean_new_password2(self):
        """Validates that the old_password field is correct."""
        password1 = self.cleaned_data['new_password1']
        password2 = self.cleaned_data['new_password2']

        if password1 != password2:
            raise forms.ValidationError(
                'The two password fields didn\'t match.',
                code='password_mismatch',
            )

        password_validation.validate_password(password2, self.user)

        return password2


class PasswordEmailResetForm(PasswordResetEmail):
    email = forms.EmailField(
        label='Email',
        required=True,
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Email address',
                'autofocus': 'autofocus'
            }
        )
    )

    def clean_email(self):
        email = self.cleaned_data.get('email')

        if not User.objects.filter(email=email).exists():
            raise ValidationError('The email is invalid.')

        return email


class PasswordUpdateForm(PasswordChangeForm):
    old_password = forms.CharField(
        label='Old password',
        required=True,
        widget=PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter old password'
            }
        )
    )
    new_password1 = forms.CharField(
        label='New password',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter new password'
            }
        ),
    )
    new_password2 = forms.CharField(
        label='Confirm password',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Confirm new password'
            }
        )
    )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.get('user', None)
        super().__init__(*args, **kwargs)

    def clean_new_password2(self):
        password1 = self.cleaned_data['new_password1']
        password2 = self.cleaned_data['new_password2']

        if password1 != password2:
            raise forms.ValidationError(
                'The two new password fields didn\'t match.',
                code='password_mismatch',
            )

        password_validation.validate_password(password2, self.user)

        return password2

    def save(self, commit=True):
        password = self.cleaned_data['new_password2']

        self.user.set_password(password)
        self.user.pass_hash = None
        if commit:
            self.user.save()
        return self.user


class SetPasswordForm(forms.Form):
    error_messages = {
        'password_mismatch': 'The two password fields didn\'t match.',
    }
    new_password1 = forms.CharField(
        label='New password',
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter new password'
            }
        ),
    )
    new_password2 = forms.CharField(
        label=_('Confirm new password'),
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter new password (again)'
            }
        ),
    )

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean_new_password2(self):
        password1 = self.cleaned_data['new_password1']
        password2 = self.cleaned_data['new_password2']

        if password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )

        password_validation.validate_password(password2, self.user)

        return password2

    def save(self, commit=True):
        password = self.cleaned_data['new_password1']
        self.user.set_password(password)

        if commit:
            self.user.save()

        return self.user
