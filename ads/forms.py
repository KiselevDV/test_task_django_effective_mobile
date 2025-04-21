from django import forms

from ads.models import Ad, ExchangeProposal


class AdForm(forms.ModelForm):
    class Meta:
        model = Ad
        fields = ['title', 'description', 'image_url', 'category', 'condition']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите заголовок'}),
            'description': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Описание товара'}),
            'image_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Ссылка на изображение'}),
            'category': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Категория'}),
            'condition': forms.Select(attrs={'class': 'form-control'}),
        }


class ProposalForm(forms.ModelForm):
    class Meta:
        model = ExchangeProposal
        fields = ['ad_sender', 'ad_receiver', 'comment']
        widgets = {
            'ad_sender': forms.Select(attrs={'class': 'form-control'}),
            'ad_receiver': forms.Select(attrs={'class': 'form-control'}),
            'comment': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Комментарий к предложению'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        ad_sender = cleaned_data.get('ad_sender')
        ad_receiver = cleaned_data.get('ad_receiver')
        if ad_sender == ad_receiver:
            raise forms.ValidationError('Нельзя предложить обмен одного и того же объявления')
        return cleaned_data
