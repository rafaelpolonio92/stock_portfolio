from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from api.models import User
from rest_framework.authtoken.models import Token

class APITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(email='test@example.com', password='password123')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_register(self):
        url = reverse('register')
        data = {
            'email': 'newuser@example.com',
            'password': 'newpassword123',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_login(self):
        url = reverse('login')
        data = {
            'email': self.user.email,
            'password': 'password123',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

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
