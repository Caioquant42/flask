from django.urls import path
from .views import rsi_analysis

urlpatterns = [
    # Other URL patterns...
    path('api/rsi-analysis/', rsi_analysis, name='rsi-analysis'),
]