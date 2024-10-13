from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib.auth.views import LogoutView, PasswordResetView, PasswordResetConfirmView, PasswordChangeView, \
    PasswordResetDoneView
from django.contrib.auth import login, update_session_auth_hash
from django.contrib.sites.shortcuts import get_current_site

from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import redirect, get_object_or_404, render
from django.urls import reverse_lazy, reverse
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.views import View
from django.views.generic import FormView, TemplateView

from bran.base.emails import email_account_activation
from bran.settings import EMAIL_HOST_USER
from bran.users.forms import RegisterForm, LoginForm, PasswordEmailResetForm, PasswordUpdateForm, SetPasswordForm
from bran.users.models import User
from bran.users.utils.tokens import account_activation_token


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        # login(request, user, backend='django.contrib.auth.backends.ModelBackend')

        return redirect(reverse_lazy('users:activate-done'))
    else:
        return HttpResponse('Activation link is invalid!')


class UserRegisterView(FormView):
    form_class = RegisterForm
    template_name = 'users/register.html'

    def get_form(self, obj=None, **kwargs):
        if self.request.method == "GET":
            return self.form_class()

        return super().get_form(**kwargs)

    def form_valid(self, form):
        user = form.save()
        current_site = get_current_site(self.request)
        email_account_activation(user, current_site, self.request)

        return redirect(reverse('users:register-done', kwargs={'pk': user.pk}))


class UserRegisterSuccessView(View):
    def get(self, request, *args, **kwargs):
        template_name = 'users/register_success.html'
        return render(request, template_name)

    def post(self, request, *args, **kwargs):
        user = get_object_or_404(User, pk=self.kwargs['pk'])
        current_site = get_current_site(self.request)
        email_account_activation(user, current_site, self.request)

        return HttpResponseRedirect(self.request.path_info)


class UserLoginView(FormView):
    form_class = LoginForm
    template_name = 'users/login.html'
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)

        return HttpResponseRedirect(self.request.GET.get('next', reverse_lazy('index')))


class UserLogoutView(LoginRequiredMixin, LogoutView):
    next_page = 'index'


class PasswordEmailResetView(PasswordResetView):
    form_class = PasswordEmailResetForm
    template_name = 'users/password_reset.html'
    from_email = EMAIL_HOST_USER
    success_url = reverse_lazy('users:password-reset-done')
    email_template_name = 'emails/users/password_reset_email.html'
    subject_template_name = 'emails/users/password_reset_subject.html'


class PasswordResetDoneView(PasswordResetDoneView):
    template_name = 'users/password_reset_done.html'


class PasswordConfirmResetView(PasswordResetConfirmView):
    template_name = 'users/password_reset_confirm.html'
    form_class = SetPasswordForm
    success_url = reverse_lazy('index')
    post_reset_login = True


class PasswordUpdateView(LoginRequiredMixin, PasswordChangeView):
    template_name = 'users/password_update.html'
    form_class = PasswordUpdateForm

    def form_valid(self, form):
        form.save()
        update_session_auth_hash(self.request, form.user)
        messages.success(self.request, 'You updated your password successfully!')

        return super().form_valid(form)

    def get_success_url(self):
        return self.request.path


class ActivateSuccessView(TemplateView):
    template_name = 'users/activate_success.html'