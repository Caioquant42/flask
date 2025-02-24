from django.urls import path
from .views import *

urlpatterns = [
    path('api/dividend-agenda/', get_dividend_agenda, name='dividend_agenda'),
    path('api/statements/', statements_view, name='statements-view'),
    path('api/historical_dy/', dividend_yield_view, name='dividend_yield_view'),
]