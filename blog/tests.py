from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from authentication.models import UserProfile
from .models import Category, BlogPost

class BlogModelTestCase(TestCase):
    def setUp(self):
        # Create test user and profile
        self.user = User.objects.create_user(
            username='testdoctor',
            first_name='Test',
            last_name='Doctor',
            email='doctor@test.com',
            password='testpass123'
        )

        self.doctor_profile = UserProfile.objects.create(
            user=self.user,
            user_type='doctor',
            address_line1='123 Test St',
            city='Test City',
            state='Test State',
            pincode='123456'
        )

        # Create test category
        self.category = Category.objects.create(
            name='Mental Health',
            slug='mental-health',
            description='Mental health related posts'
        )

    def test_create_blog_post(self):
        blog_post = BlogPost.objects.create(
            title='Test Blog Post',
            author=self.doctor_profile,
            category=self.category,
            summary='This is a test summary',
            content='This is test content for the blog post.',
            is_draft=False
        )

        self.assertEqual(str(blog_post), 'Test Blog Post')
        self.assertFalse(blog_post.is_draft)
        self.assertTrue(blog_post.is_published)

    def test_blog_post_slug_generation(self):
        blog_post = BlogPost.objects.create(
            title='Test Blog Post with Auto Slug',
            author=self.doctor_profile,
            category=self.category,
            summary='This is a test summary',
            content='This is test content for the blog post.',
        )

        self.assertEqual(blog_post.slug, 'test-blog-post-with-auto-slug')

    def test_summary_truncation(self):
        long_summary = 'This is a very long summary that contains more than fifteen words to test the truncation functionality properly'
        blog_post = BlogPost.objects.create(
            title='Test Truncation',
            author=self.doctor_profile,
            category=self.category,
            summary=long_summary,
            content='Test content',
        )

        truncated = blog_post.get_summary_truncated(15)
        word_count = len(truncated.split())

        # Should have 15 words + '...'
        self.assertTrue(truncated.endswith('...'))
        self.assertEqual(len(truncated.replace('...', '').split()), 15)

class BlogViewTestCase(TestCase):
    def setUp(self):
        # Create test users
        self.doctor_user = User.objects.create_user(
            username='testdoctor',
            password='testpass123'
        )

        self.patient_user = User.objects.create_user(
            username='testpatient',
            password='testpass123'
        )

        # Create profiles
        self.doctor_profile = UserProfile.objects.create(
            user=self.doctor_user,
            user_type='doctor',
            address_line1='123 Test St',
            city='Test City',
            state='Test State',
            pincode='123456'
        )

        self.patient_profile = UserProfile.objects.create(
            user=self.patient_user,
            user_type='patient',
            address_line1='456 Test Ave',
            city='Test City',
            state='Test State',
            pincode='654321'
        )

        # Create test category
        self.category = Category.objects.create(
            name='Test Category',
            slug='test-category'
        )

    def test_doctor_can_access_create_post(self):
        self.client.login(username='testdoctor', password='testpass123')
        response = self.client.get(reverse('blog:create_post'))
        self.assertEqual(response.status_code, 200)

    def test_patient_cannot_access_create_post(self):
        self.client.login(username='testpatient', password='testpass123')
        response = self.client.get(reverse('blog:create_post'))
        # Should redirect to patient blog list
        self.assertEqual(response.status_code, 302)

    def test_patient_can_access_blog_list(self):
        self.client.login(username='testpatient', password='testpass123')
        response = self.client.get(reverse('blog:patient_blog_list'))
        self.assertEqual(response.status_code, 200)
