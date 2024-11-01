from django.contrib import messages
from django.http import HttpResponseRedirect
from django.views.generic import FormView

from bran.base.emails import email_contact_us
from bran.base.forms import ContactForm


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


