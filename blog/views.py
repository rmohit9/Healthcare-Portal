from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from authentication.models import UserProfile
from .models import BlogPost, Category
from .forms import BlogPostForm, CategoryFilterForm

@login_required
def blog_home(request):
    """Blog home page - redirects based on user type"""
    try:
        profile = UserProfile.objects.get(user=request.user)
        if profile.user_type == 'doctor':
            return redirect('blog:doctor_posts')
        else:
            return redirect('blog:patient_blog_list')
    except UserProfile.DoesNotExist:
        messages.error(request, 'Profile not found.')
        return redirect('home')

@login_required
def create_blog_post(request):
    """Create new blog post - doctors only"""
    try:
        profile = UserProfile.objects.get(user=request.user)
        if profile.user_type != 'doctor':
            messages.error(request, 'Only doctors can create blog posts.')
            return redirect('blog:patient_blog_list')
    except UserProfile.DoesNotExist:
        messages.error(request, 'Profile not found.')
        return redirect('home')

    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            blog_post = form.save(commit=False)
            blog_post.author = profile
            blog_post.save()

            if blog_post.is_draft:
                messages.success(request, 'Blog post saved as draft successfully!')
            else:
                messages.success(request, 'Blog post published successfully!')

            return redirect('blog:doctor_posts')
    else:
        form = BlogPostForm()

    return render(request, 'blog/create_post.html', {'form': form})

@login_required
def doctor_posts(request):
    """List all posts by the current doctor (including drafts)"""
    try:
        profile = UserProfile.objects.get(user=request.user)
        if profile.user_type != 'doctor':
            messages.error(request, 'Access denied. Doctors only.')
            return redirect('blog:patient_blog_list')
    except UserProfile.DoesNotExist:
        messages.error(request, 'Profile not found.')
        return redirect('home')

    posts = BlogPost.objects.filter(author=profile).order_by('-created_at')

    # Pagination
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    posts_page = paginator.get_page(page_number)

    context = {
        'posts': posts_page,
        'total_posts': posts.count(),
        'published_posts': posts.filter(is_draft=False).count(),
        'draft_posts': posts.filter(is_draft=True).count(),
    }

    return render(request, 'blog/doctor_posts.html', context)

@login_required
def patient_blog_list(request):
    """List all published blog posts for patients, with category filtering"""
    try:
        profile = UserProfile.objects.get(user=request.user)
        if profile.user_type != 'patient':
            messages.error(request, 'Access denied. Patients only.')
            return redirect('blog:doctor_posts')
    except UserProfile.DoesNotExist:
        messages.error(request, 'Profile not found.')
        return redirect('home')

    # Get all published posts (not drafts)
    posts = BlogPost.objects.filter(is_draft=False).order_by('-published_at')

    # Category filtering
    form = CategoryFilterForm(request.GET)
    selected_category = None

    if form.is_valid() and form.cleaned_data['category']:
        selected_category = form.cleaned_data['category']
        posts = posts.filter(category=selected_category)

    # Search functionality
    search_query = request.GET.get('search')
    if search_query:
        posts = posts.filter(
            Q(title__icontains=search_query) | 
            Q(summary__icontains=search_query) |
            Q(content__icontains=search_query)
        )

    # Group posts by category for display
    categories = Category.objects.all()
    categorized_posts = {}

    for category in categories:
        category_posts = posts.filter(category=category)[:6]  # Limit to 6 per category
        if category_posts:
            categorized_posts[category] = category_posts

    # Pagination for all posts view
    paginator = Paginator(posts, 12)
    page_number = request.GET.get('page')
    posts_page = paginator.get_page(page_number)

    context = {
        'posts': posts_page,
        'categorized_posts': categorized_posts,
        'categories': categories,
        'form': form,
        'selected_category': selected_category,
        'search_query': search_query,
        'total_posts': posts.count(),
    }

    return render(request, 'blog/patient_blog_list.html', context)

@login_required
def blog_post_detail(request, slug):
    """View individual blog post details"""
    post = get_object_or_404(BlogPost, slug=slug)

    # Check if user can view this post
    try:
        profile = UserProfile.objects.get(user=request.user)

        # If post is draft, only author can view
        if post.is_draft and post.author != profile:
            messages.error(request, 'This post is not available.')
            return redirect('blog:patient_blog_list')

        # Get related posts from same category
        related_posts = BlogPost.objects.filter(
            category=post.category, 
            is_draft=False
        ).exclude(id=post.id)[:4]

        context = {
            'post': post,
            'related_posts': related_posts,
            'is_author': post.author == profile,
        }

        return render(request, 'blog/post_detail.html', context)

    except UserProfile.DoesNotExist:
        messages.error(request, 'Profile not found.')
        return redirect('home')

@login_required
def category_posts(request, slug):
    """View posts by category"""
    category = get_object_or_404(Category, slug=slug)
    posts = BlogPost.objects.filter(category=category, is_draft=False).order_by('-published_at')

    # Pagination
    paginator = Paginator(posts, 12)
    page_number = request.GET.get('page')
    posts_page = paginator.get_page(page_number)

    context = {
        'category': category,
        'posts': posts_page,
        'total_posts': posts.count(),
    }

    return render(request, 'blog/category_posts.html', context)

@login_required
def edit_blog_post(request, slug):
    """Edit blog post - only by author"""
    post = get_object_or_404(BlogPost, slug=slug)

    try:
        profile = UserProfile.objects.get(user=request.user)

        # Check if user is the author
        if post.author != profile:
            messages.error(request, 'You can only edit your own posts.')
            return redirect('blog:doctor_posts')

        if request.method == 'POST':
            form = BlogPostForm(request.POST, request.FILES, instance=post)
            if form.is_valid():
                form.save()
                messages.success(request, 'Blog post updated successfully!')
                return redirect('blog:doctor_posts')
        else:
            form = BlogPostForm(instance=post)

        context = {
            'form': form,
            'post': post,
            'is_edit': True,
        }

        return render(request, 'blog/create_post.html', context)

    except UserProfile.DoesNotExist:
        messages.error(request, 'Profile not found.')
        return redirect('home')

@login_required
def delete_blog_post(request, slug):
    """Delete blog post - only by author"""
    post = get_object_or_404(BlogPost, slug=slug)

    try:
        profile = UserProfile.objects.get(user=request.user)

        # Check if user is the author
        if post.author != profile:
            messages.error(request, 'You can only delete your own posts.')
            return redirect('blog:doctor_posts')

        if request.method == 'POST':
            post.delete()
            messages.success(request, 'Blog post deleted successfully!')
            return redirect('blog:doctor_posts')

        context = {'post': post}
        return render(request, 'blog/delete_post.html', context)

    except UserProfile.DoesNotExist:
        messages.error(request, 'Profile not found.')
        return redirect('home')
