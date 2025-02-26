from django.urls import path
from .views import optimize_portfolio_view

urlpatterns = [
    path('api/optimize-portfolio/', optimize_portfolio_view, name='optimize_portfolio'),
]