from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.blog_home, name='blog_home'),
    path('create/', views.create_blog_post, name='create_post'),
    path('my-posts/', views.doctor_posts, name='doctor_posts'),
    path('browse/', views.patient_blog_list, name='patient_blog_list'),
    path('category/<slug:slug>/', views.category_posts, name='category_posts'),
    path('post/<slug:slug>/', views.blog_post_detail, name='post_detail'),
    path('post/<slug:slug>/edit/', views.edit_blog_post, name='edit_post'),
    path('post/<slug:slug>/delete/', views.delete_blog_post, name='delete_post'),
]
