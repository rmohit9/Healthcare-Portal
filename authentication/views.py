from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from .forms import CustomUserCreationForm, UserProfileForm
from .models import UserProfile

def home(request):
    """Home page view"""
    return render(request, 'authentication/home.html')

@transaction.atomic
def signup(request):
    """User signup view with profile creation"""
    if request.method == 'POST':
        user_form = CustomUserCreationForm(request.POST)
        profile_form = UserProfileForm(request.POST, request.FILES)

        if user_form.is_valid() and profile_form.is_valid():
            # Create user
            user = user_form.save()

            # Create profile
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()

            username = user_form.cleaned_data.get('username')
            messages.success(request, f'Account created successfully for {username}!')

            # Log the user in automatically
            user = authenticate(
                username=user_form.cleaned_data['username'],
                password=user_form.cleaned_data['password1']
            )
            if user:
                login(request, user)
                return redirect('dashboard')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        user_form = CustomUserCreationForm()
        profile_form = UserProfileForm()

    return render(request, 'authentication/signup.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })

@login_required
def dashboard(request):
    """Dashboard view that redirects based on user type"""
    try:
        profile = UserProfile.objects.get(user=request.user)

        context = {
            'user': request.user,
            'profile': profile
        }

        if profile.user_type == 'patient':
            return render(request, 'authentication/patient_dashboard.html', context)
        elif profile.user_type == 'doctor':
            return render(request, 'authentication/doctor_dashboard.html', context)
        else:
            messages.error(request, 'Invalid user type.')
            return redirect('home')

    except UserProfile.DoesNotExist:
        messages.error(request, 'Profile not found. Please contact support.')
        return redirect('home')

def custom_login(request):
    """Custom login view"""
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.get_full_name()}!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'authentication/login.html')
