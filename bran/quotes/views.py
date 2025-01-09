from django.contrib import messages
from django.http import HttpResponseRedirect
from django.views.generic import FormView

from bran.base.emails import email_get_quote
from bran.quotes.forms import QuoteForm, ParcelFormset


class GetQuote(FormView):
    form_class = QuoteForm
    template_name = 'quotes/get_a_quote.html'

    FORMSET_PREFIX = 'parcel'

    def post(self, request, *args, **kwargs):
        form = self.get_form(self.get_form_class())
        formset = ParcelFormset(request.POST, prefix=self.FORMSET_PREFIX)

        if form.is_valid() and formset.is_valid():
            return self.forms_valid(form, formset)
        else:
            return self.forms_invalid(form, formset)

    def forms_valid(self, form, formset):
        email_get_quote(form.cleaned_data, formset.cleaned_data)
        messages.success(self.request, 'Your quote request was sent successfully!')

        return HttpResponseRedirect(self.request.path_info)

    def forms_invalid(self, form, formset):
        return self.render_to_response(
            self.get_context_data(form=form, formset=formset))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if 'formset' not in kwargs:
            context['formset'] = ParcelFormset(prefix=self.FORMSET_PREFIX)
        if 'form' not in kwargs:
            context['form'] = QuoteForm()

        return context
