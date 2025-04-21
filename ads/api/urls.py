from django.urls import path, include
from rest_framework.routers import DefaultRouter

from ads.api.views import AdViewSet, ExchangeProposalViewSet

app_name = 'api'

router = DefaultRouter()
router.register(r'ads', AdViewSet)
router.register(r'proposals', ExchangeProposalViewSet)

urlpatterns = [
    path('api-auth/', include('rest_framework.urls')),
    path('', include(router.urls)),
]
