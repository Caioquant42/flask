from django.urls import path
from .views import SurvivalAnalysisView

urlpatterns = [
    path('api/survival/all', SurvivalAnalysisView.as_view(), name='survival_analysis'),
]