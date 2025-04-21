from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models


User = get_user_model()


class Ad(models.Model):
    class Condition(models.TextChoices):
        NEW = 'new', 'Новый'
        USED = 'used', 'Б/у'

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='ads', verbose_name='Пользователь')
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    description = models.TextField(max_length=10000, verbose_name='Описание')
    image_url = models.URLField(blank=True, null=True, verbose_name='Ссылка на изображение')
    category = models.CharField(max_length=100, verbose_name='Категория')
    condition = models.CharField(max_length=10, choices=Condition.choices, verbose_name='Состояние')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    class Meta:
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.title} ({self.get_condition_display()})'


class ExchangeProposal(models.Model):
    class Status(models.TextChoices):
        PENDING = 'pending', 'Ожидает'
        ACCEPTED = 'accepted', 'Принята'
        REJECTED = 'rejected', 'Отклонена'

    ad_sender = models.ForeignKey(
        Ad, on_delete=models.CASCADE, related_name='sent_exchange_proposals', verbose_name='Отправитель')
    ad_receiver = models.ForeignKey(
        Ad, on_delete=models.CASCADE, related_name='received_exchange_proposals', verbose_name='Получатель')
    comment = models.TextField(max_length=10000, verbose_name='Комментарий')
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDING, verbose_name='Статус')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    class Meta:
        verbose_name = 'Предложение обмена'
        verbose_name_plural = 'Предложения обмена'
        ordering = ['-created_at']

    def __str__(self):
        return f'Предложение от {self.ad_sender} к {self.ad_receiver} ({self.get_status_display()})'

    def clean(self):
        super().clean()
        if self.ad_sender == self.ad_receiver:
            raise ValidationError('Нельзя предложить обмен одного и того же объявления')

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)
