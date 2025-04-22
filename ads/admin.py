from django.contrib import admin

from ads.models import Ad, ExchangeProposal


@admin.register(Ad)
class AdAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'user', 'category', 'condition', 'created_at')
    list_filter = ('condition', 'category', 'created_at')
    search_fields = ('title', 'description', 'user__username', 'category')
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)


@admin.register(ExchangeProposal)
class ExchangeProposalAdmin(admin.ModelAdmin):
    list_display = ('id', 'ad_sender', 'ad_receiver', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = (
        'ad_sender__title', 'ad_receiver__title',
        'ad_sender__user__username', 'ad_receiver__user__username',
        'comment',
    )
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)
