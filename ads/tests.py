from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse

from ads.models import Ad, ExchangeProposal
from ads.forms import ProposalForm


class AdModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.ad = Ad.objects.create(
            user=self.user,
            title='Test Ad',
            description='Some description',
            image_url='http://example.com/image.jpg',
            category='books',
            condition='new',
        )

    def test_str_representation(self):
        self.assertEqual(str(self.ad), 'Test Ad (Новый)')

    def test_created_at_is_set(self):
        self.assertIsNotNone(self.ad.created_at)


class ExchangeProposalModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.ad1 = Ad.objects.create(
            user=self.user, title='Ad 1', description='...', image_url='', category='books', condition='used')
        self.ad2 = Ad.objects.create(
            user=self.user, title='Ad 2', description='...', image_url='', category='books', condition='used')

    def test_str_representation(self):
        proposal = ExchangeProposal.objects.create(ad_sender=self.ad1, ad_receiver=self.ad2, comment='Want to swap?')
        self.assertIn('Ad 1', str(proposal))
        self.assertIn('Ad 2', str(proposal))

    def test_created_at_is_set(self):
        proposal = ExchangeProposal.objects.create(ad_sender=self.ad1, ad_receiver=self.ad2, comment='Want to swap?')
        self.assertIsNotNone(proposal.created_at)


class AdViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='poster', password='12345')
        self.client.login(username='poster', password='12345')

    def test_create_ad(self):
        response = self.client.post(reverse('ads:ad_create'), {
            'title': 'New Ad',
            'description': 'Description here',
            'image_url': 'http://example.com/image.jpg',
            'category': 'books',
            'condition': 'new',
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Ad.objects.count(), 1)
        self.assertEqual(Ad.objects.first().title, 'New Ad')

    def test_update_ad(self):
        ad = Ad.objects.create(
            user=self.user, title='Old Title', description='...', image_url='', category='books', condition='used')
        response = self.client.post(reverse('ads:ad_edit', args=[ad.pk]), {
            'title': 'Updated Title',
            'description': ad.description,
            'image_url': ad.image_url,
            'category': ad.category,
            'condition': ad.condition,
        })
        self.assertEqual(response.status_code, 302)
        ad.refresh_from_db()
        self.assertEqual(ad.title, 'Updated Title')

    def test_delete_ad(self):
        ad = Ad.objects.create(
            user=self.user, title='To Delete', description='...',
            image_url='', category='books', condition='used')
        response = self.client.post(reverse('ads:ad_delete', args=[ad.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Ad.objects.count(), 0)


class ProposalFormTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='tester', password='12345')
        self.ad1 = Ad.objects.create(
            user=self.user, title='Ad 1', description='...', image_url='', category='books', condition='used')
        self.ad2 = Ad.objects.create(
            user=self.user, title='Ad 2', description='...', image_url='', category='books', condition='used')

    def test_valid_form(self):
        form = ProposalForm(data={
            'ad_sender': self.ad1.pk,
            'ad_receiver': self.ad2.pk,
            'comment': 'Interested?'
        })
        self.assertTrue(form.is_valid())

    def test_invalid_same_ad(self):
        form = ProposalForm(data={
            'ad_sender': self.ad1.pk,
            'ad_receiver': self.ad1.pk,
            'comment': 'Same ad'
        })
        self.assertFalse(form.is_valid())
        self.assertIn('__all__', form.errors)
        self.assertIn('Нельзя предложить обмен одного и того же объявления', form.errors['__all__'])
