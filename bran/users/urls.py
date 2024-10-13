from django.urls import path

from bran.users.views import activate, PasswordUpdateView, PasswordResetDoneView, UserRegisterSuccessView, \
    UserRegisterView, UserLoginView, UserLogoutView, PasswordEmailResetView, PasswordConfirmResetView, \
    ActivateSuccessView

app_name = 'users'

urlpatterns = (
    # Authentication and authorization
    path('register/', UserRegisterView.as_view(), name='register'),
    path('register/done/<int:pk>', UserRegisterSuccessView.as_view(), name='register-done'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),

    # Password reset and update
    path('password-reset/', PasswordEmailResetView.as_view(), name='password-reset'),
    path('password-reset/done/', PasswordResetDoneView.as_view(), name='password-reset-done'),
    path('password-reset/<uidb64>/<token>/', PasswordConfirmResetView.as_view(), name='password-reset-confirm'),
    path('password-update/', PasswordUpdateView.as_view(), name='password-update'),

    # Account activation
    path('activate/<slug:uidb64>/<slug:token>/', activate, name='activate'),
    path('activate/done', ActivateSuccessView.as_view(), name='activate-done'),
)
