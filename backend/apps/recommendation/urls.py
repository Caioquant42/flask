from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'br-recommendations', BRStockRecommendationViewSet, basename='br-recommendation')
router.register(r'usa-nasdaq-recommendations', NASDAQRecommendationViewSet, basename='usa-nasdaq-recommendation')
router.register(r'usa-nyse-recommendations', NYSERecommendationViewSet, basename='usa-nyse-recommendation')

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/strong-buy-analysis/', strong_buy_analysis, name='strong-buy-analysis'),
    path('api/buy-analysis/', buy_analysis, name='buy-analysis'),
    path('api/nasdaq/strong-buy-analysis/', nasdaq_strong_buy_analysis, name='nasdaq-strong-buy-analysis'),
    path('api/nasdaq/buy-analysis/', nasdaq_buy_analysis, name='nasdaq-buy-analysis'),
    path('api/nyse/strong-buy-analysis/', nyse_strong_buy_analysis, name='nyse-strong-buy-analysis'),
    path('api/nyse/buy-analysis/', nyse_buy_analysis, name='nyse-buy-analysis'),
    
]