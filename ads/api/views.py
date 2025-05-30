from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied

from ads.models import Ad, ExchangeProposal
from ads.api.serializers import AdSerializer, ExchangeProposalSerializer


class AdViewSet(viewsets.ModelViewSet):
    queryset = Ad.objects.all().order_by('-created_at')
    serializer_class = AdSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        if serializer.instance.user != self.request.user:
            raise PermissionDenied('Нельзя редактировать это объявление')
        serializer.save()

    def perform_destroy(self, instance):
        if instance.user != self.request.user:
            raise PermissionDenied('Нельзя удалить это объявление')
        instance.delete()

    def get_queryset(self):
        queryset = super().get_queryset()
        title = self.request.query_params.get('title')
        category = self.request.query_params.get('category')
        condition = self.request.query_params.get('condition')
        if title:
            queryset = queryset.filter(title__icontains=title)
        if category:
            queryset = queryset.filter(category__iexact=category)
        if condition:
            queryset = queryset.filter(condition__iexact=condition)
        return queryset


class ExchangeProposalViewSet(viewsets.ModelViewSet):
    queryset = ExchangeProposal.objects.all().order_by('-created_at')
    serializer_class = ExchangeProposalSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        ad_sender = serializer.validated_data['ad_sender']
        ad_receiver = serializer.validated_data['ad_receiver']
        if ad_sender.user == ad_receiver.user:
            raise PermissionDenied('Нельзя предложить обмен самому себе')
        serializer.save()

    def perform_update(self, serializer):
        if serializer.instance.ad_sender.user != self.request.user:
            raise PermissionDenied('Нельзя редактировать это предложение')
        serializer.save()

    def perform_destroy(self, instance):
        if instance.ad_sender.user != self.request.user:
            raise PermissionDenied('Нельзя удалить это предложение')
        instance.delete()

    def get_queryset(self):
        queryset = super().get_queryset()
        sender = self.request.query_params.get('sender')
        receiver = self.request.query_params.get('receiver')
        status_ = self.request.query_params.get('status')
        if sender:
            queryset = queryset.filter(ad_sender__user__username=sender)
        if receiver:
            queryset = queryset.filter(ad_receiver__user__username=receiver)
        if status_:
            queryset = queryset.filter(status=status_)
        return queryset

    @action(detail=True, methods=['post'])
    def update_status(self, request, pk=None):
        proposal = self.get_object()
        if proposal.ad_receiver.user != request.user:
            return Response({'error': 'Нельзя обновлять это предложение'}, status=status.HTTP_403_FORBIDDEN)
        new_status = request.data.get('status')
        if new_status in ['accepted', 'rejected']:
            proposal.status = new_status
            proposal.save()
            return Response({'status': 'updated'}, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid status'}, status=status.HTTP_400_BAD_REQUEST)
