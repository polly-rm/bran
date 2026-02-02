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

    # def clean_middle_name(self):
    #     if self.cleaned_data.get('middle_name'):
    #         raise forms.ValidationError("Spam detected")
    #     return ''
    #
    # def clean_timestamp(self):
    #     ts = self.cleaned_data.get('timestamp')
    #     try:
    #         ts_float = float(ts)
    #     except (TypeError, ValueError):
    #         ts_float = 0
    #
    #     # allow 1 second buffer for very fast submissions
    #     if time.time() - ts_float < 1:
    #         raise forms.ValidationError("Spam detected")
    #     return ts
