import time
from django import forms


class AntiSpamFormMixin(forms.Form):
    middle_name = forms.CharField(
        required=False,
        widget=forms.HiddenInput()
    )
    timestamp = forms.CharField(
        widget=forms.HiddenInput()
    )

    def clean_middle_name(self):
        if self.cleaned_data.get('middle_name'):
            raise forms.ValidationError("Spam detected")
        return ''

    def clean_timestamp(self):
        ts = self.cleaned_data.get('timestamp')
        try:
            if time.time() - float(ts) < 3:
                raise forms.ValidationError("Spam detected")
        except (TypeError, ValueError):
            raise forms.ValidationError("Spam detected")
        return ts
