from django.urls import path

from bran.quotes.views import GetQuote

app_name = 'quotes'

urlpatterns = [
    path('', GetQuote.as_view(), name='get-a-quote'),
]
