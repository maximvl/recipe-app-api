from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):

    def test_create_user_with_email_successful(self):
        """create user"""
        email = 'test@email.com'
        password = 'testPass123'
        user = get_user_model().objects.create_user(
            email=email, password=password
        )
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """test email"""
        email = 'test@EMAIL.COM'
        user = get_user_model().objects.create_user(
            email=email, password='password'
        )
        self.assertEqual(user.email, email.lower())

    def test_new_user_valid_email(self):
        """test no email error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(email=None, password='password')

    def test_create_superuser(self):
        """test superuser"""
        user = get_user_model().objects.create_superuser(
            email='test@mail.com',
            password='password'
        )
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
