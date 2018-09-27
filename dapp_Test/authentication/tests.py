# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from django.urls import reverse
from authentication.models import UserProfile


# Create your tests here.

def create_admin(username, email, password):
    return UserProfile.objects.create_user(username, password, email=email)


class LoginViewTests(TestCase):
    def test_no_email_no_password(self):
        """
        If no email and password, the view should return the message 'This user does not exist.'.
        """
        UserProfile.objects.create_user("admin", "admin", email="admin@gmail.com")
        data = {}
        response = self.client.post(reverse('auth:login'), data=data)
        self.assertEquals(response.context['message'], 'This user does not exist.')


    def test_no_email(self):
        """
        If no email, the view should return a message error.
        """
        UserProfile.objects.create_user("admin", "admin", email="admin@gmail.com")
        data = {'password': 'admin'}
        response = self.client.post(reverse('auth:login'), data=data)
        self.assertEquals(response.context['message'], 'This user does not exist.')

    def test_no_password(self):
        """
        If password, the view should return a message error.
        """
        UserProfile.objects.create_user("admin", "admin", email="admin@gmail.com")
        data = {'email': 'admin@gmail.com'}
        response = self.client.post(reverse('auth:login'), data=data)
        self.assertEquals(response.context['message'], 'This user does not exist.')

    def test_all_credentials(self):
        """
        If all credentials are supplied, the view login and return home page.
        """
        UserProfile.objects.create_user("admin", "admin", email="admin@gmail.com")
        data = {'email': 'admin@gmail.com', 'password': 'admin'}
        response = self.client.post(reverse('auth:login'), data=data)
        self.assertRedirects(response, reverse('home'), 302, 200)

#     def test_inactive_user(self):
#         """
#         If user is inactive, the view should return a message saying 'This account has been disabled!'.
#         """
#         user = UserProfile.objects.create_user("admin", "admin", email="admin@gmail.com", is_active=False)
#         data = {'email': 'admin@gmail.com', 'password': 'admin'}
#         user.is_active = False
#         user.save()
#         response = self.client.post(reverse('auth:login'), data=data)
#         self.assertEquals(response.context['message'], 'This account has been disabled.')


class createAccountTests(TestCase):
    def test_no_data(self):
        """
        If no data, the view should return an error message.
        """
        response = self.client.post(reverse('auth:createAccount'), data={})
        self.assertEquals(response.context['message'], 'Please fill the form!')

    def test_all_fields(self):
        """
        If all required fields are supplied, the view should return a message error.
        """
        data = {'username': 'admin',
                'email': 'admin@gmail.com',
                'password': 'admin'}

        response = self.client.post(reverse('auth:createAccount'), data=data)
        self.assertRedirects(response, reverse('auth:authentication'), 302, 200)


class updateUserTests(TestCase):
    def test_user_not_authenticated(self):
        """
        if user not authenticated, it should return 404.
        """
        UserProfile.objects.create_user("admin", "admin", email="admin@gmail.com")
        data = {'username': 'dimitri', 'email': 'admin@gmail.com'}
        response = self.client.post('auth/1/update/', data=data)
        self.assertEqual(response.status_code, 404)

    def test_user_not_existed(self):
        """
        if user does not exist, it should return 404.
        """
        response = self.client.post('auth/1/update/', data={})
        self.assertEqual(response.status_code, 404)

    def test_user_authenticated_is_not_user(self):
        """
        if user trying to edit is not user, it should return 404.
        """
        user1 = UserProfile.objects.create_user("user1", "user1", email="user1@gmail.com")
        user2 = UserProfile.objects.create_user("user2", "user2", email="user2@gmail.com")
        credentials = {'email': user2.email, 'password': 'user2'}
        self.client.login(**credentials)
        data = {'username': 'user2', 'first_name': 'dimitri'}
        url = reverse('auth:update', args=(user1.id,))
        response = self.client.post(url, data=data)
        self.assertRedirects(response, reverse('home'), 302, 200)

    def test_no_data(self):
        """
        If no data is submitted, it should ask the user to fill in the required fields.
        """
        user = UserProfile.objects.create_user("admin", "admin", email="admin@gmail.com")
        credentials = {'email': 'admin@gmail.com', 'password': 'admin'}
        self.client.login(**credentials)
        url = reverse('auth:update', args=(user.pk,))
        response = self.client.post(url)
        self.assertEquals(response.context['message'], 'Please fill in the required fields!')

    def test_update_data(self):
        """
        If no data, the view should return an error message.
        """
        user1 = UserProfile.objects.create_user("admin", "admin", email="admin@gmail.com")
        credentials = {'email': 'admin@gmail.com', 'password': 'admin'}
        self.client.login(**credentials)
        data = {'username': 'dimitri', 'email': 'admin@gmail.com', 'first_name': 'dimitri'}
        url = reverse('auth:update', args=(user.pk,))
        response = self.client.post(url, data=data)
        self.assertEquals(user1.username, 'dimitri')
        self.assertEquals(user1.first_name, 'dimitri')
