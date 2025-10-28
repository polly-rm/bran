from django import forms
from django.core.validators import MaxLengthValidator
from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV2Checkbox

from bran.quotes.forms import QuoteForm


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
    captcha = ReCaptchaField(
        widget=ReCaptchaV2Checkbox()
    )
    middle_name = forms.CharField(
        required=False,
        widget=forms.HiddenInput()
    )
    timestamp = forms.CharField(
        widget=forms.HiddenInput()
    )


class CalculatorForm(QuoteForm):
    postcode_from = forms.CharField(
        required=True,
        label='From',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Collection Postcode'
            }
        ),
        validators=[
            MaxLengthValidator(50, message="This field cannot be more than 50 characters long.")
        ]
    )
    postcode_to = forms.CharField(
        required=True,
        label='To',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Delivery Postcode'
            }
        ),
        validators=[
            MaxLengthValidator(50, message="This field cannot be more than 50 characters long.")
        ]
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in ['name', 'contact_telephone', 'email', 'company_from', 'company_to', 'time_to_collect_from',
                      'time_to_collect_to', 'time_to_deliver_from', 'time_to_deliver_to', 'additional_info', 'captcha']:
            self.fields.pop(field, None)
