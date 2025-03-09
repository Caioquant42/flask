from django.urls import path
from .views import *

urlpatterns = [
    path('api/json/IBOV/', stocks_json, name='stocks_json'),
    path('api/fluxo/', FluxoJsonView.as_view(), name='fluxo_json'),  # Alterado aqui
    path('api/volatility-analysis/', VolatilityAnalysisView.as_view(), name='volatility_analysis'),
    path('api/top-volatility-stocks/', TopVolatilityStocksView.as_view(), name='top_volatility_stocks'),
    path('api/surface/', SurfaceView.as_view(), name='volatility_surface'),
    path('api/cointegration/', CointegrationView.as_view(), name='cointegration'),
    path('api/cointegration/currency', CurrencyCointegrationView.as_view(), name='cointegration_currency'),
    path('api/rrg/', RRGView.as_view(), name='rrg'),
    path('api/rrg/indices/', RRGINDEXView.as_view(), name='rrg_indices'),
    path('api/opcoes/riscozero/14/', COLLAR14View.as_view(), name='collar14'),
    path('api/opcoes/riscozero/30/', COLLAR30View.as_view(), name='collar30'),
    path('api/opcoes/riscozero/60/', COLLAR60View.as_view(), name='collar60'),
    path('api/opcoes/riscozero/above60/', COLLARABOVE60View.as_view(), name='collarabove60'),
    path('api/opcoes/riscozero/14/otm/', OTMCOLLAR14View.as_view(), name='otm_collar14'),
    path('api/opcoes/riscozero/30/otm/', OTMCOLLAR30View.as_view(), name='otm_collar30'),
    path('api/opcoes/riscozero/60/otm/', OTMCOLLAR60View.as_view(), name='otm_collar60'),
    path('api/opcoes/riscozero/above60/otm/', OTMCOLLARABOVE60View.as_view(), name='otm_collarabove60'),
    path('api/dashboard/benchmarks/', BenchmarksHistorical.as_view(), name='BenchmarksHistorical'),
]
