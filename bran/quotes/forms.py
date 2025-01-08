from django import forms
from django.core.validators import MaxLengthValidator
from django.forms import formset_factory


class QuoteForm(forms.Form):
    name = forms.CharField(
        required=True,
        label='Name',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        ),
        validators=[
            MaxLengthValidator(50, message="Your name cannot be more than 50 characters long.")
        ]
    )
    contact_telephone = forms.CharField(
        required=True,
        label='Contact telephone',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    email = forms.CharField(
        required=True,
        label='Email',
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control'
            }
        )
    )
    postcode_from = forms.CharField(
        required=True,
        label='Collection address',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'From (Postcode)'
            }
        ),
        validators=[
            MaxLengthValidator(50, message="This field cannot be more than 50 characters long.")
        ]
    )
    postcode_to = forms.CharField(
        required=True,
        label='Delivery address',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'From (Postcode)'
            }
        ),
        validators=[
            MaxLengthValidator(50, message="This field cannot be more than 50 characters long.")
        ]
    )
    time_to_collect_from = forms.CharField(
        required=True,
        label='Collection Time',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control datetimepicker-input',
                'data-target': '#datetimepicker1',
                'placeholder': 'From (Date and Time)',
            }
        )
    )
    time_to_collect_to = forms.CharField(
        required=False,
        label='Collection Time',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control datetimepicker-input',
                'data-target': '#datetimepicker2',
                'placeholder': 'To (Date and Time)'
            }
        )
    )
    time_to_deliver_from = forms.CharField(
        required=True,
        label='Delivery Time',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control datetimepicker-input',
                'data-target': '#datetimepicker3',
                'placeholder': 'From (Date and Time)'
            }
        )
    )
    time_to_deliver_to = forms.CharField(
        required=False,
        label='Delivery Time',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control datetimepicker-input',
                'data-target': '#datetimepicker4',
                'placeholder': 'To (Date and Time)'
            }
        )
    )
    additional_info = forms.CharField(
        required=False,
        label='Additional Information',
        widget=forms.Textarea(
            attrs={
                'rows': '4',
                'class': 'form-control hide'
            },
        )
    )


class ParcelForm(forms.Form):
    count = forms.IntegerField(
        required=True,
        label='Count',
        widget=forms.TextInput(
            attrs={
                'type': 'number',
                'class': 'form-control',
                'min': 1,
                'placeholder': 'Count'
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
                'min': 0,
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
                'min': 0,
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
                'min': 0,
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
                'min': 0,
                'placeholder': 'Height (cm)',
            },
        ),
        error_messages={
            'required': 'Height field is required.',
        }
    )


ParcelFormset = formset_factory(
    ParcelForm,
    extra=1,
)
