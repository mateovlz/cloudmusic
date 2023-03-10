from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from cloudmusic.models import UserAccounts
from rest_framework.parsers import JSONParser
import json

# Create your tests here.
class AccountTests(APITestCase):
    def test_login_account(self):
        """
        Ensure we can only registered users can login.
        """
        url = reverse('login')
        data = {'email': 'mateo.tes@circle.co', 'password': 'MVmv12312]'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(UserAccounts.objects.count(), 0)

    def test_create_account(self):
        """
        Ensure we can register users.
        """
        url = reverse('signUp')
        data = {'email': 'mateo.test2@circle.co', 'password': 'Macirl123]'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(UserAccounts.objects.count(), 1)

    def test_password_validation_1(self):
        """
        Ensure password validations special characters and amount characters at least 10 .
        """
        url = reverse('signUp')
        data = {'email': 'mateo.tes@circle.co', 'password': 'MVmv12312'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_406_NOT_ACCEPTABLE)
        self.assertJSONEqual(response.content, {'message': 'Creating an account [error] Password is invalid, should contain at least 10 characters, one of this characters @ # ? ! ] is missing'})

    def test_password_validation_2(self):
        """
        Ensure password validations using only lowercase characters.
        """
        url = reverse('signUp')
        data = {'email': 'mateo.tes@circle.co', 'password': 'mmmmmmmmmmm'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_406_NOT_ACCEPTABLE)
        self.assertJSONEqual(response.content, {'message': 'Creating an account [error] Password is invalid, one uppercase is missing, one of this characters @ # ? ! ] is missing'})

    def test_password_validation_3(self):
        """
        Ensure password validations using only uppercase characters.
        """
        url = reverse('signUp')
        data = {'email': 'mateo.tes@circle.co', 'password': 'MMMMMMMMMMM'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_406_NOT_ACCEPTABLE)
        self.assertJSONEqual(response.content, {'message': 'Creating an account [error] Password is invalid, one lowercase is missing, one of this characters @ # ? ! ] is missing'})


class SongEndpoints(APITestCase):
    def test_login_account(self):
        """
        Ensure we can only registered users can login.
        """
        url_create = reverse('signUp')
        data_create = {'email': 'mateo.test2@circle.co', 'password': 'Macirl123]'}
        response_create = self.client.post(url_create, data_create, format='json')
        self.assertEqual(response_create.status_code, status.HTTP_200_OK)

        url = reverse('login')
        data = {'email': 'mateo.test2@circle.co', 'password': 'Macirl123]'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_endpoints_security(self):
        """
        Ensure endpoint malformade url show the error.
        """
        response = self.client.get('/song/list/asdasd')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertJSONEqual(response.content, {'message': 'Error to access to Songs, for acces to your own songs please refer to /song/list/private for all the publics songs refer to /songs/list/private'})


