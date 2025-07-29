from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model

User = get_user_model()

class UserTests(APITestCase):
    def setUp(self):
        self.signup_url = reverse('auth-signup')
        self.login_url = reverse('auth-login')
        self.me_url = reverse('user-me')

        self.user_data = {
            'nickname': 'testuser',
            'email': 'test@example.com',
            'password': 'testpass123'
        }

        self.user = User.objects.create_user(
            nickname='existinguser',
            email='existing@example.com',
            password='existingpass'
        )

    def test_signup(self):
        response = self.client.post(self.signup_url, self.user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(nickname='testuser').exists())

    def test_login(self):
        response = self.client.post(self.login_url, {
            'nickname': 'existinguser',
            'password': 'existingpass'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)

    def authenticate(self):
        res = self.client.post(self.login_url, {
            'nickname': 'existinguser',
            'password': 'existingpass'
        })
        token = res.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

    def test_get_me(self):
        self.authenticate()
        response = self.client.get(self.me_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['nickname'], 'existinguser')

    def test_patch_me(self):
        self.authenticate()
        response = self.client.patch(self.me_url, {'nickname': 'updateduser'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['nickname'], 'updateduser')

    def test_get_other_user(self):
        other_user = User.objects.create_user(
            nickname='otheruser',
            email='other@example.com',
            password='otherpass'
        )
        self.authenticate()
        url = reverse('user-detail', args=[other_user.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['nickname'], 'otheruser')
