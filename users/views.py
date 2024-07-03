from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from .forms import RegisterUserForm, UpdateUserForm


User = get_user_model()

# register view
def register(request):
    if request.user.is_authenticated:
        return redirect('home')
    form = RegisterUserForm()
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}')
            return redirect('login-user')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, error, extra_tags='warning')
            return redirect('register')
    else:
        context = {
            'form': form
        }
        return render(request, 'users/register.html', context)
    
# login view
def login_user(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)

        if user is not None and user.is_active:
            login(request, user)
            messages.success(request, 'You are now logged in')
            return redirect('home')
        else:
            messages.warning(request, 'Invalid credentials')
            return redirect('login-user')
    return render(request, 'users/login.html')

# logout view
def logout_user(request):
    logout(request)
    messages.success(request, 'You are now logged out')
    return redirect('login-user')

# User profile view
@login_required
def userProfile(request):
    user = request.user
    profile_form = UpdateUserForm(instance=user)
    if request.method == 'POST':
        profile_form = UpdateUserForm(request.POST, request.FILES, instance=user)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, 'Profile updated successfully')
            return redirect('profile')
        else:
            for field, errors in profile_form.errors.items():
                for error in errors:
                    messages.error(request, error, extra_tags='warning')
            return redirect('profile')
    context = {
        'user': user,
        'profile_form': profile_form
    }

    return render(request, 'users/profile.html', context)
