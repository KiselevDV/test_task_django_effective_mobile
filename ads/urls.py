from django.urls import path, include
from ads.views import (
    AdListView, AdDetailView, AdCreateView, AdUpdateView, AdDeleteView, ProposalListView, ProposalCreateView,
    ProposalUpdateView
)

app_name = 'ads'

urlpatterns = [
    path('ads/<int:pk>/edit/', AdUpdateView.as_view(), name='ad_edit'),
    path('ads/<int:pk>/delete/', AdDeleteView.as_view(), name='ad_delete'),
    path('ads/create/', AdCreateView.as_view(), name='ad_create'),
    path('ads/<int:pk>/', AdDetailView.as_view(), name='ad_detail'),

    path('proposals/<int:pk>/status/', ProposalUpdateView.as_view(), name='proposal_update'),
    path('proposals/create/', ProposalCreateView.as_view(), name='proposal_create'),
    path('proposals/', ProposalListView.as_view(), name='proposal_list'),

    path('api/', include('ads.api.urls')),
    path('', AdListView.as_view(), name='ad_list'),
]
