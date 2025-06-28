from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from django.contrib.auth import authenticate

class UserRegistrationTest(TestCase):

    def test_registration_success(self):
        registration_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password1': 'TestPassword123',
            'password2': 'TestPassword123'
        }

        response = self.client.post(reverse('register'), registration_data)

        self.assertRedirects(response, reverse('main'))
        self.assertEqual(User.objects.count(), 1)

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Ваш аккаунт был успешно создан!')

        user = authenticate(username='testuser', password='TestPassword123')
        self.assertIsNotNone(user)

    def test_registration_failure_invalid_data(self):
        registration_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password1': 'TestPassword123',
            'password2': 'WrongPassword123'
        }

        response = self.client.post(reverse('register'), registration_data)

        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'password2', 'Пароли не совпадают.')

        self.assertEqual(User.objects.count(), 0)

    def test_registration_invalid_email(self):
        registration_data = {
            'username': 'testuser',
            'email': 'invalidemail',
            'password1': 'TestPassword123',
            'password2': 'TestPassword123'
        }

        response = self.client.post(reverse('register'), registration_data)

        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'email', 'Введите правильный адрес электронной почты.')

        self.assertEqual(User.objects.count(), 0)


class UserAuthenticationTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='TestPassword123')

    def test_user_login_success(self):
        response = self.client.post(reverse('login'), {'username': 'testuser', 'password': 'TestPassword123'})

        self.assertTrue('_auth_user_id' in self.client.session)

    def test_user_login_invalid_credentials(self):
        response = self.client.post(reverse('login'), {'username': 'testuser', 'password': 'WrongPassword'})

        self.assertContains(response, 'Неверный логин или пароль')

    def test_logout(self):
        self.client.login(username='testuser', password='TestPassword123')

        self.client.logout()


        self.assertNotIn('_auth_user_id', self.client.session)
