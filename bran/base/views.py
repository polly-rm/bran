import os
import qrcode
import requests
import time

from io import BytesIO

from django.http import HttpResponse
from django.http import JsonResponse
from django.contrib import messages
from django.shortcuts import redirect
from django.views.generic import TemplateView

from bran import settings
from bran.base.common import get_driving_distance
from bran.base.emails import email_contact_us, email_automatic_answer, email_calculator_to_admin
from bran.base.forms import ContactForm, CalculatorForm
from bran.settings import CURRENT_DOMAIN, GOOGLE_MAPS_DISTANCE_API_KEY
from django_ratelimit.decorators import ratelimit
from django.utils.decorators import method_decorator


def generate_qr_code(request):
    # URL for the Django website (adjust with your actual URL)
    url = f'{CURRENT_DOMAIN}/'

    # Generate the QR code
    qr = qrcode.make(url)

    # Save the QR code to an in-memory file
    buffer = BytesIO()
    qr.save(buffer, format="PNG")
    buffer.seek(0)

    # Return the QR code as an HTTP response
    return HttpResponse(buffer, content_type="image/png")


def robots_txt(request):
    robots_path = os.path.join(settings.BASE_DIR, 'robots.txt')
    with open(robots_path, 'r') as f:
        return HttpResponse(f.read(), content_type="text/plain")


def autocomplete(request):
    query = request.GET.get('input')
    api_url = f"https://maps.googleapis.com/maps/api/place/autocomplete/json"
    params = {
        'input': query,
        'key': settings.GOOGLE_MAPS_API_KEY,
    }
    response = requests.get(api_url, params=params)
    return JsonResponse(response.json())


@method_decorator(
    ratelimit(key='ip', rate='30/m'),
    name='post'
)
class IndexTemplateView(TemplateView):
    template_name = 'index.html'

    def get(self, request, *args, **kwargs):
        request.session.pop('quote_data', None)
        now = str(time.time())

        return self.render_to_response({
            'form': ContactForm(initial={'timestamp': now}),
            'calculator_form': CalculatorForm(initial={'timestamp': now}),
        })

    def post(self, request, *args, **kwargs):
        # SLOW BOTS
        if getattr(request, 'limited', False):
            time.sleep(2)

        # CONTACT FORM
        if 'contact_form_submit' in request.POST:
            form = ContactForm(request.POST)
            calculator_form = CalculatorForm()

            if form.is_valid():
                self.handle_contact_form(form)
                messages.success(request, 'Your message was sent successfully!')
                return redirect(request.path)

        # CALCULATOR FORM
        elif 'calculator_form_submit' in request.POST:
            calculator_form = CalculatorForm(request.POST)
            form = ContactForm()

            if calculator_form.is_valid():
                self.handle_calculator_form(calculator_form)
                return redirect('calculator')

        # invalid → re-render both forms
        return self.render_to_response({
            'form': form,
            'calculator_form': calculator_form,
        })

    @staticmethod
    def handle_contact_form(form):
        email_contact_us(
            form.cleaned_data['name'],
            form.cleaned_data['email'],
            form.cleaned_data['subject'],
            form.cleaned_data['message'],
        )
        email_automatic_answer(form.cleaned_data['email'])

    def handle_calculator_form(self, form):
        quote_data = form.cleaned_data
        self.request.session['quote_data'] = quote_data
        email_calculator_to_admin(quote_data)


class SameDayDeliveryTemplateView(TemplateView):
    template_name = 'same_day_delivery.html'


class CalculatorTemplateView(TemplateView):
    template_name = 'calculator.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        quote_data = self.request.session.get('quote_data', {})
        postcode_from = quote_data.get('postcode_from')
        postcode_to = quote_data.get('postcode_to')
        context['distance'] = get_driving_distance(postcode_from, postcode_to, GOOGLE_MAPS_DISTANCE_API_KEY).get(
            'distance_miles')

        return context
