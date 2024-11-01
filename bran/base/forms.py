from django import forms
from django.core.validators import MaxLengthValidator


class ContactForm(forms.Form):
    name = forms.CharField(
        required=True,
        label='Your Name',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'
            }
        ),
        validators=[
            MaxLengthValidator(50, message="Your name cannot be more than 50 characters long.")
        ]
    )
    email = forms.CharField(
        required=True,
        label='Your Email',
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control'
            }
        )
    )
    subject = forms.CharField(
        required=True,
        label='Subject',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'
            }
        ),
        validators=[
            MaxLengthValidator(100, message="Your subject cannot be more than 50 characters long.")
        ]
    )
    message = forms.CharField(
        required=True,
        label='Message',
        widget=forms.Textarea(
            attrs={
                'rows': '10',
                'class': 'form-control'
            },
        )
    )
