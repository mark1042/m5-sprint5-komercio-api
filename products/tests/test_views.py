from rest_framework.test import APITestCase
from rest_framework.views import status
from accounts.models import Account
from rest_framework.authtoken.models import Token

from products.models import Product


class TestProductView(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.seller_data = {'email': 'seller@mail.com', 'first_name': 'seller', 'last_name': 'seller', 'password': '1234', 'is_seller': True}
        cls.other_seller_data = {'email': 'seller2@mail.com', 'first_name': 'seller', 'last_name': 'seller', 'password': '1234', 'is_seller': True}
        cls.not_seller_data = {'email': 'notseller@mail.com', 'first_name': 'not', 'last_name': 'seller', 'password': '1234', 'is_seller': False}

        cls.seller = Account.objects.create_user(**cls.seller_data)
        cls.other_seller = Account.objects.create_user(**cls.other_seller_data)
        cls.not_seller = Account.objects.create_user(**cls.not_seller_data)

        cls.seller_token = Token.objects.create(user=cls.seller)
        cls.other_seller_token = Token.objects.create(user=cls.other_seller)
        cls.not_seller_token = Token.objects.create(user=cls.not_seller)

        cls.product_data = {'description': 'test desc', 'price': 10, 'quantity': 1, 'user': cls.seller}
        cls.other_product_data = {'description': 'test desc', 'price': 10, 'quantity': 1, 'user': cls.not_seller}
        cls.update_product_data = {'description': 'test update'}

        cls.product = Product.objects.create(**cls.product_data)
        cls.other_product = Product.objects.create(**cls.other_product_data)

    def test_only_seller_can_create_product(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.seller_token.key)
        res = self.client.post('/api/products/', data=self.product_data)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
    
    def test_only_seller_can_create_product_fail(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.not_seller_token.key)
        res = self.client.post('/api/products/', data=self.product_data)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_only_seller_can_update_product(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.seller_token.key)
        res = self.client.patch(f'/api/products/{self.product.id}/', data=self.update_product_data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
    
    def test_only_seller_can_update_product_fail(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.other_seller_token.key)
        res = self.client.patch(f'/api/products/{self.product.id}/', data=self.update_product_data)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_anyone_can_list_products(self):
        res = self.client.get('/api/products/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
    
    def test_anyone_can_retrieve_products(self):
        res = res = self.client.get(f'/api/products/{self.product.id}/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
    
    def test_create_product_response(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.seller_token.key)
        res = self.client.post('/api/products/', data=self.product_data)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertIn('id' , res.data['user'].keys())
        self.assertIn('email', res.data['user'].keys())
        self.assertIn('first_name', res.data['user'].keys())
        self.assertIn('last_name', res.data['user'].keys())
        



