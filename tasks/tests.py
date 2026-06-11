from django.test import TestCase
from django.contrib.auth.models import User, Group
from rest_framework.test import APIClient
from rest_framework import status
from .models import Task


def create_user_with_role(username, password, role='User'):
    Group.objects.get_or_create(name='Admin')
    Group.objects.get_or_create(name='User')

    user = User.objects.create_user(username=username, password=password)
    group = Group.objects.get(name=role)
    user.groups.add(group)
    return user


def get_token(client, username, password):
    response = client.post(
        '/api/auth/login/',
        {
            'username': username,
            'password': password
        },
        format='json'
    )
    return response.data['access']


def get_count(response):
    if isinstance(response.data, dict) and 'count' in response.data:
        return response.data['count']
    return len(response.data)


class TaskModelTest(TestCase):
    def setUp(self):
        self.user = create_user_with_role('modeluser', 'pass1234')

    def test_task_creation(self):
        task = Task.objects.create(title='Test Task', owner=self.user)
        self.assertEqual(str(task), 'Test Task (Pending)')

    def test_task_default_status_is_false(self):
        task = Task.objects.create(title='My Task', owner=self.user)
        self.assertFalse(task.status)


class TaskCRUDTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = create_user_with_role('regularuser', 'pass1234', role='User')
        self.token = get_token(self.client, 'regularuser', 'pass1234')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

    def test_create_task(self):
        response = self.client.post(
            '/api/tasks/',
            {'title': 'New Task'},
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 1)

    def test_list_tasks_only_own(self):
        other = create_user_with_role('otheruser', 'pass1234')

        Task.objects.create(title='My Task', owner=self.user)
        Task.objects.create(title='Other Task', owner=other)

        response = self.client.get('/api/tasks/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(get_count(response), 1)

    def test_update_task(self):
        task = Task.objects.create(title='Old Title', owner=self.user)

        response = self.client.patch(
            f'/api/tasks/{task.id}/',
            {'title': 'New Title'},
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'New Title')

    def test_delete_task(self):
        task = Task.objects.create(title='To Delete', owner=self.user)

        response = self.client.delete(f'/api/tasks/{task.id}/')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Task.objects.count(), 0)

    def test_mark_task_complete(self):
        task = Task.objects.create(title='My Task', owner=self.user, status=False)

        response = self.client.patch(
            f'/api/tasks/{task.id}/',
            {'status': True},
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['status'])

    def test_user_cannot_access_others_task(self):
        other = create_user_with_role('otheruser2', 'pass1234')
        task = Task.objects.create(title='Private Task', owner=other)

        response = self.client.get(f'/api/tasks/{task.id}/')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class AdminRBACTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin = create_user_with_role('adminuser', 'pass1234', role='Admin')
        self.regular_user = create_user_with_role('regularuser2', 'pass1234', role='User')

        token = get_token(self.client, 'adminuser', 'pass1234')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

    def test_admin_sees_all_tasks(self):
        other = create_user_with_role('anotheruser', 'pass1234')

        Task.objects.create(title='Task A', owner=self.admin)
        Task.objects.create(title='Task B', owner=other)

        response = self.client.get('/api/tasks/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(get_count(response), 2)

    def test_admin_can_delete_any_task(self):
        task = Task.objects.create(title='Other Task', owner=self.regular_user)

        response = self.client.delete(f'/api/tasks/{task.id}/')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)