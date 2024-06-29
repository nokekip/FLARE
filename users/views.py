from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from .forms import RegisterUserForm


# register view
def register(request):
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
