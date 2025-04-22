from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from ads.models import Ad, ExchangeProposal
from ads.forms import AdForm, ProposalForm


class AdListView(ListView):
    model = Ad
    template_name = 'ads/ad_list.html'
    context_object_name = 'ads'
    paginate_by = 10

    def get_queryset(self):
        queryset = Ad.objects.all().order_by('-created_at')
        query = self.request.GET.get('q')
        category = self.request.GET.get('category')
        condition = self.request.GET.get('condition')

        if query:
            queryset = queryset.filter(Q(title__icontains=query) | Q(description__icontains=query))
        if category:
            queryset = queryset.filter(category=category)
        if condition:
            queryset = queryset.filter(condition=condition)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Ad.objects.values_list('category', flat=True).distinct()
        context['conditions'] = Ad.objects.values_list('condition', flat=True).distinct()
        return context


class AdDetailView(DetailView):
    model = Ad
    template_name = 'ads/ad_detail.html'
    context_object_name = 'ad'


class AdCreateView(LoginRequiredMixin, CreateView):
    model = Ad
    form_class = AdForm
    template_name = 'ads/ad_form.html'
    success_url = reverse_lazy('ads:ad_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class AdUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Ad
    form_class = AdForm
    template_name = 'ads/ad_form.html'
    success_url = reverse_lazy('ads:ad_list')

    def test_func(self):
        ad = self.get_object()
        return ad.user == self.request.user


class AdDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Ad
    template_name = 'ads/ad_confirm_delete.html'
    success_url = reverse_lazy('ads:ad_list')

    def test_func(self):
        ad = self.get_object()
        return ad.user == self.request.user


class ProposalListView(ListView):
    model = ExchangeProposal
    template_name = 'ads/proposal_list.html'
    context_object_name = 'proposals'
    paginate_by = 10

    def get_queryset(self):
        queryset = ExchangeProposal.objects.all().order_by('-created_at')
        sender = self.request.GET.get('sender')
        receiver = self.request.GET.get('receiver')
        status = self.request.GET.get('status')

        if sender:
            queryset = queryset.filter(ad_sender__user__username__icontains=sender)
        if receiver:
            queryset = queryset.filter(ad_receiver__user__username__icontains=receiver)
        if status:
            queryset = queryset.filter(status=status)

        return queryset


class ProposalCreateView(LoginRequiredMixin, CreateView):
    model = ExchangeProposal
    form_class = ProposalForm
    template_name = 'ads/proposal_form.html'
    success_url = reverse_lazy('proposal_list')

    def form_valid(self, form):
        return super().form_valid(form)


class ProposalUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = ExchangeProposal
    fields = ['status']
    template_name = 'ads/proposal_status_form.html'
    success_url = reverse_lazy('proposal_list')

    def test_func(self):
        proposal = self.get_object()
        return self.request.user == proposal.ad_receiver.user
