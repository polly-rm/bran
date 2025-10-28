import time

from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponseForbidden, HttpResponse
from django.views.generic import FormView

from bran.base.common import get_driving_distance, check_for_spam
from bran.base.emails import email_get_quote, email_automatic_answer
from bran.base.mixins import QuoteFormMixin
from bran.quotes.forms import QuoteForm, ParcelFormset
from bran.settings import GOOGLE_MAPS_DISTANCE_API_KEY


class GetQuote(QuoteFormMixin, FormView):
    form_class = QuoteForm
    template_name = 'quotes/get_a_quote.html'

    def forms_valid(self, form, formset):
        if form.cleaned_data.get('honeypot'):
            return HttpResponseForbidden('Spam detected!')

        distance = self.get_distance(form)
        email_get_quote(form.cleaned_data, formset.cleaned_data, distance)
        email_automatic_answer(form.cleaned_data.get('email'))
        messages.success(self.request, 'Your quote request was sent successfully!')

        return HttpResponseRedirect(self.request.path_info)

    @staticmethod
    def get_distance(form):
        postcode_from = form.cleaned_data.get('postcode_from')
        postcode_to = form.cleaned_data.get('postcode_to')
        return get_driving_distance(postcode_from, postcode_to, GOOGLE_MAPS_DISTANCE_API_KEY)
