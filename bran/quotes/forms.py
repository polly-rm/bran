from django import forms
from django.core.validators import MaxLengthValidator
from django.forms.models import modelformset_factory
from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV2Checkbox

from bran.quotes.models import Quote, Parcel


class QuoteForm(forms.ModelForm):
    name = forms.CharField(
        required=True,
        label='Name',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Your name'
            }
        ),
        validators=[
            MaxLengthValidator(50, message="Your name cannot be more than 50 characters long.")
        ]
    )
    invoice_name = forms.CharField(
        required=True,
        label='Invoice name',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Invoice name'
            }
        ),
        validators=[
            MaxLengthValidator(150, message="Your invoice name cannot be more than 150 characters long.")
        ]
    )
    invoice_address = forms.CharField(
        required=True,
        label='Invoice address',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Invoice Address'
            }
        ),
        validators=[
            MaxLengthValidator(150, message="Your invoice address cannot be more than 150 characters long.")
        ]
    )
    contact_telephone = forms.CharField(
        required=True,
        label='Contact telephone',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Your telephone'
            }
        )
    )
    email = forms.CharField(
        required=True,
        label='Email',
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Your email'
            }
        )
    )
    postcode_from = forms.CharField(
        required=True,
        label='Collection address',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'From (postcode)'
            }
        ),
        validators=[
            MaxLengthValidator(150, message="This field cannot be more than 50 characters long.")
        ]
    )
    postcode_to = forms.CharField(
        required=True,
        label='Delivery address',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'To (postcode)'
            }
        ),
        validators=[
            MaxLengthValidator(150, message="This field cannot be more than 50 characters long.")
        ]
    )
    company_from = forms.CharField(
        required=False,
        label='Collect from company',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Company name to collect from'
            }
        ),
        validators=[
            MaxLengthValidator(50, message="This field cannot be more than 50 characters long.")
        ]
    )
    company_to = forms.CharField(
        required=False,
        label='Deliver to company',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Company name to deliver to'
            }
        ),
        validators=[
            MaxLengthValidator(50, message="This field cannot be more than 50 characters long.")
        ]
    )
    time_to_collect_from = forms.DateTimeField(
        required=True,
        label='Collection time',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control datetimepicker-input',
                'data-target': '#datetimepicker1',
                'placeholder': 'From (date and time)',
            }
        ),
        input_formats=['%d/%m/%Y %H:%M']
    )
    time_to_collect_to = forms.DateTimeField(
        required=False,
        label='Collection time',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control datetimepicker-input',
                'data-target': '#datetimepicker2',
                'placeholder': 'To (date and time)'
            }
        ),
        input_formats=['%d/%m/%Y %H:%M']
    )
    time_to_deliver_from = forms.DateTimeField(
        required=True,
        label='Delivery time',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control datetimepicker-input',
                'data-target': '#datetimepicker3',
                'placeholder': 'From (date and time)'
            }
        ),
        input_formats=['%d/%m/%Y %H:%M']
    )
    time_to_deliver_to = forms.DateTimeField(
        required=False,
        label='Delivery time',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control datetimepicker-input',
                'data-target': '#datetimepicker4',
                'placeholder': 'To (date and time)'
            }
        ),
        input_formats=['%d/%m/%Y %H:%M']
    )
    additional_info = forms.CharField(
        required=False,
        label='Additional information',
        widget=forms.Textarea(
            attrs={
                'rows': '4',
                'class': 'form-control hide'
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

    class Meta:
        model = Quote
        fields = ['name',
                  'invoice_name',
                  'invoice_address',
                  'contact_telephone',
                  'email',
                  'postcode_from',
                  'postcode_to',
                  'company_from',
                  'company_to',
                  'time_to_collect_from',
                  'time_to_collect_to',
                  'time_to_deliver_from',
                  'time_to_deliver_to',
                  'additional_info', ]


class ParcelForm(forms.ModelForm):
    count = forms.IntegerField(
        required=True,
        label='Count',
        widget=forms.TextInput(
            attrs={
                'type': 'number',
                'class': 'form-control',
                'min': 1,
                'placeholder': 'Items'
            },
        ),
        error_messages={
            'required': 'Count field is required.',
        }
    )
    weight = forms.DecimalField(
        required=True,
        label='Weight',
        widget=forms.TextInput(
            attrs={
                'type': 'number',
                'class': 'form-control',
                'step': '0.01',
                'placeholder': 'Weight (kg)',
            },
        ),
        error_messages={
            'required': 'Weight field is required.',
        }
    )
    length = forms.DecimalField(
        required=True,
        label='Length',
        widget=forms.TextInput(
            attrs={
                'type': 'number',
                'class': 'form-control',
                'step': '0.01',
                'placeholder': 'Length (cm)',
            },
        ),
        error_messages={
            'required': 'Length field is required.',
        }
    )
    width = forms.DecimalField(
        required=True,
        label='Width',
        widget=forms.TextInput(
            attrs={
                'type': 'number',
                'class': 'form-control',
                'step': '0.01',
                'placeholder': 'Width (cm)',
            },
        ),
        error_messages={
            'required': 'Width field is required.',
        }
    )
    height = forms.DecimalField(
        required=True,
        label='Height',
        widget=forms.TextInput(
            attrs={
                'type': 'number',
                'class': 'form-control',
                'step': '0.01',
                'placeholder': 'Height (cm)',
            },
        ),
        error_messages={
            'required': 'Height field is required.',
        }
    )

    class Meta:
        model = Parcel
        fields = ['count',
                  'weight',
                  'length',
                  'width',
                  'height']


ParcelFormset = modelformset_factory(
    Parcel,
    ParcelForm,
    extra=1,
)
