import os
import qrcode
import requests

from io import BytesIO

from django.http import HttpResponse
from django.http import JsonResponse
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.views.generic import FormView

from bran import settings
from bran.base.emails import email_contact_us
from bran.base.forms import ContactForm
from bran.settings import CURRENT_DOMAIN


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


class IndexTemplateView(FormView):
    form_class = ContactForm
    template_name = 'index.html'

    def get_initial(self):
        initial = super().get_initial()
        user = self.request.user

        if user.is_authenticated:
            initial['email'] = user.email

        return initial

    def form_valid(self, form):
        name = form.cleaned_data.get('name')
        email = form.cleaned_data.get('email')
        subject = form.cleaned_data.get('subject')
        message = form.cleaned_data.get('message')

        email_contact_us(name, email, subject, message)
        messages.success(self.request, 'Your message was sent successfully!')

        return HttpResponseRedirect(self.request.path_info)
