from django.db import models
from django.contrib.auth.models import User
from authentication.models import UserProfile
from django.urls import reverse
from django.utils import timezone

class Category(models.Model):
    """Blog post categories"""
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('blog:category_posts', kwargs={'slug': self.slug})

class BlogPost(models.Model):
    """Blog posts that can be created by doctors"""
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE, limit_choices_to={'user_type': 'doctor'})
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='posts')
    image = models.ImageField(upload_to='blog_images/', blank=True, null=True)
    summary = models.TextField(max_length=500, help_text="Brief summary of the blog post")
    content = models.TextField(help_text="Full content of the blog post")
    is_draft = models.BooleanField(default=False, help_text="Check to save as draft")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # Auto-generate slug from title if not provided
        if not self.slug:
            from django.utils.text import slugify
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while BlogPost.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug

        # Set published_at when post is no longer draft
        if not self.is_draft and not self.published_at:
            self.published_at = timezone.now()
        elif self.is_draft:
            self.published_at = None

        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blog:post_detail', kwargs={'slug': self.slug})

    def get_summary_truncated(self, word_limit=15):
        """Return summary truncated to specified word limit"""
        words = self.summary.split()
        if len(words) > word_limit:
            return ' '.join(words[:word_limit]) + '...'
        return self.summary

    @property
    def is_published(self):
        return not self.is_draft and self.published_at is not None
