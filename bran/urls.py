"""
URL configuration for bran project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.flatpages import views
from django.contrib.sitemaps.views import sitemap

from bran.base.sitemaps import StaticSitemap, SendEmailSitemap
from bran.base.views import IndexTemplateView, generate_qr_code, robots_txt

sitemaps = {
    'static': StaticSitemap,
    # 'send_email': SendEmailSitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', IndexTemplateView.as_view(), name='index'),
    path('users/', include('bran.users.urls', namespace='users')),
    path('quote/', include('bran.quotes.urls', namespace='quotes')),

    # FlatPages
    path('cookies-policy/', views.flatpage, {'url': '/cookies-policy'}, name='cookies-policy'),

    # Other
    path('qr-code/', generate_qr_code, name="qr-code"),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('robots.txt', robots_txt),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
