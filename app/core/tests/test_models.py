from django.test import TestCase
from django.contrib.auth import get_user_model

from unittest.mock import patch

from core import models


def sample_user(email='test@email.com', password='passwd'):
    return get_user_model().objects.create_user(email, password)


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

    def test_tag_str(self):
        """test tag string"""
        tag = models.Tag.objects.create(
            user=sample_user(),
            name='Vegan'
        )
        self.assertEqual(str(tag), tag.name)

    def test_ingridient_str(self):
        ingredient = models.Ingredient.objects.create(
            user=sample_user(),
            name='Banana'
        )
        self.assertEqual(str(ingredient), ingredient.name)

    def test_recipe_str(self):
        recipe = models.Recipe.objects.create(
            user=sample_user(),
            title='title',
            time_minutes=5,
            price=100.00
        )
        self.assertEqual(str(recipe), recipe.title)

    @patch('uuid.uuid4')
    def test_recipe_filename_uuid(self, mock_uuid):
        uuid = 'test-uuid'
        mock_uuid.return_value = uuid
        file_path = models.recipe_image_file_path(None, 'myimage.jpg')
        exp_path = f'uploads/recipe/{uuid}.jpg'
        self.assertEqual(file_path, exp_path)
