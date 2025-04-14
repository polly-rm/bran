import time

from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.views.generic import FormView

from bran.base.common import get_driving_distance, check_for_spam
from bran.base.emails import email_get_quote, email_automatic_answer
from bran.quotes.forms import QuoteForm, ParcelFormset
from bran.settings import GOOGLE_MAPS_DISTANCE_API_KEY


class GetQuote(FormView):
    form_class = QuoteForm
    template_name = 'quotes/get_a_quote.html'

    FORMSET_PREFIX = 'parcel'

    def get_initial(self):
        initial = {'timestamp': str(time.time())}

        return initial

    def post(self, request, *args, **kwargs):
        form = self.get_form(self.get_form_class())
        formset = ParcelFormset(request.POST, prefix=self.FORMSET_PREFIX)
        check_for_spam(request)

        if form.is_valid() and formset.is_valid():
            return self.forms_valid(form, formset)
        else:
            return self.forms_invalid(form, formset)

    def forms_valid(self, form, formset):
        if form.cleaned_data.get('honeypot'):
            return HttpResponseForbidden('Spam detected!')

        distance = self.get_distance(form)

        email_get_quote(form.cleaned_data, formset.cleaned_data, distance)
        email_automatic_answer(form.cleaned_data.get('email'))
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

    @staticmethod
    def get_distance(form):
        postcode_from = form.cleaned_data.get('postcode_from')
        postcode_to = form.cleaned_data.get('postcode_to')

        return get_driving_distance(postcode_from, postcode_to, GOOGLE_MAPS_DISTANCE_API_KEY)
