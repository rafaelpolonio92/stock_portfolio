from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from api.models import User

class APITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(email='test@example.com', password='password123')

        # Obtain JWT token
        response = self.client.post(reverse('token_obtain_pair'), {'email': 'test@example.com', 'password': 'password123'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

    def test_register(self):
        url = reverse('register')
        data = {
            'email': 'newuser@example.com',
            'password': 'newpassword123',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_login(self):
        url = reverse('token_obtain_pair')
        data = {
            'email': self.user.email,
            'password': 'password123',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_buy_stock(self):
        url = reverse('buy_stock')
        data = {'ticker': 'AAPL', 'purchasePrice': 150}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['portfolio']), 1)

    def test_sell_stock(self):
        url = reverse('sell_stock')
        # First buy a stock to be able to sell it
        self.client.post(reverse('buy_stock'), {'ticker': 'AAPL', 'purchasePrice': 150}, format='json')
        data = {'ticker': 'AAPL'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['portfolio']), 0)
