from django.urls import path
from .views import *

urlpatterns = [
    path('api/json/IBOV/', stocks_json, name='stocks_json'),
    path('api/fluxo/', FluxoJsonView.as_view(), name='fluxo_json'),  # Alterado aqui
    path('api/volatility-analysis/', VolatilityAnalysisView.as_view(), name='volatility_analysis'),
    path('api/top-volatility-stocks/', TopVolatilityStocksView.as_view(), name='top_volatility_stocks'),
]
