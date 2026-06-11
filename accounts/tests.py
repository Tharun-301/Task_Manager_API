from django.test import TestCase
from django.contrib.auth.models import User, Group
from rest_framework.test import APIClient
from rest_framework import status


class AuthTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        Group.objects.get_or_create(name='Admin')
        Group.objects.get_or_create(name='User')

    def test_user_registration(self):
        data = {
            'username': 'testuser',
            'password': 'testpass123',
            'email': 'test@test.com'
        }

        response = self.client.post('/api/auth/register/', data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.filter(username='testuser').count(), 1)

    def test_registration_assigns_user_role(self):
        data = {
            'username': 'roleuser',
            'password': 'testpass123'
        }

        response = self.client.post('/api/auth/register/', data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        user = User.objects.get(username='roleuser')
        self.assertTrue(user.groups.filter(name='User').exists())

    def test_login_returns_jwt_tokens(self):
        User.objects.create_user(username='loginuser', password='testpass123')

        data = {
            'username': 'loginuser',
            'password': 'testpass123'
        }

        response = self.client.post('/api/auth/login/', data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_token_refresh(self):
        User.objects.create_user(username='refreshuser', password='testpass123')

        login_response = self.client.post(
            '/api/auth/login/',
            {
                'username': 'refreshuser',
                'password': 'testpass123'
            },
            format='json'
        )

        refresh_token = login_response.data['refresh']

        response = self.client.post(
            '/api/auth/refresh/',
            {'refresh': refresh_token},
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)

    def test_unauthenticated_access_to_tasks_denied(self):
        response = self.client.get('/api/tasks/')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)