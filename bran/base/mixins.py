import time
from django.http import HttpResponse

from bran.base.common import check_for_spam
from bran.quotes.forms import ParcelFormset


class QuoteFormMixin:
    FORMSET_PREFIX = 'parcel'

    def get_initial(self):
        return {'timestamp': str(time.time())}

    def post(self, request, *args, **kwargs):
        form = self.get_form(self.get_form_class())
        formset = self.get_formset(request)

        # spam check
        spam_response = check_for_spam(request)
        if isinstance(spam_response, HttpResponse):
            return spam_response

        if form.is_valid() and formset.is_valid():
            return self.forms_valid(form, formset)
        else:
            return self.forms_invalid(form, formset)

    def get_formset(self, request):
        return ParcelFormset(request.POST or None, prefix=self.FORMSET_PREFIX)

    def forms_invalid(self, form, formset):
        return self.render_to_response(
            self.get_context_data(form=form, formset=formset)
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.setdefault('form', self.get_form())
        context.setdefault('formset', ParcelFormset(prefix=self.FORMSET_PREFIX))
        return context
