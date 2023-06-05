from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse


class StockApiTest(APITestCase):
    def setUp(self):
        self.url = reverse('buy_stock')
        self.client = APIClient()
        self.payload = {
            'user': 'user1',
            'stockname': 'stock3',
            'quantity': 100
        }

    def test_buy_stock_api_with_wrong_user(self):
        payload = {
            'user': 'wrong_user',
            'stockname': 'stock1',
            'quantity': 100
        }
        response = self.client.post(self.url, payload)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, 'User Not Found')

    def test_buy_stock_api_with_wrong_stock(self):
        payload = {
            'user': 'user1',
            'stockname': 'wrong_stock',
            'quantity': 100
        }
        response = self.client.post(self.url, payload)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, 'Invalid Stock Name')

    def test_buy_stock_api_with_insufficient_credit(self):
        payload = {
            'user': 'user1',
            'stockname': 'stock1',
            'quantity': 10000000
        }
        response = self.client.post(self.url, payload)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, 'Deny')

    def test_buy_stock_api(self):
        payload = {
            'user': 'user1',
            'stockname': 'stock1',
            'quantity': 100
        }
        response = self.client.post(self.url, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, 'Accept')
