from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from .models import UserProfile

class UserProfileTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            first_name='Test',
            last_name='User',
            email='test@example.com',
            password='testpass123'
        )

    def test_create_user_profile(self):
        profile = UserProfile.objects.create(
            user=self.user,
            user_type='patient',
            address_line1='123 Test St',
            city='Test City',
            state='Test State',
            pincode='123456'
        )
        self.assertEqual(str(profile), 'Test User - patient')

    def test_signup_view(self):
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)

    def test_login_view(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
