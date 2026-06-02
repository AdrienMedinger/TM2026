from django.shortcuts import render

# Create your views here.


# authentication/views.py


from . import forms
from django.contrib.auth import authenticate, login, logout 
from django.shortcuts import redirect, render 

def login_page(request):
    form = forms.LoginForm()
    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
        if form.is_valid():
             user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
        if user is not None:
             login(request, user)
             message = 'Bonjour, {user.username}! Vous êtes connecté.'
             return redirect('home')
        message = 'Identifiants invalides.'
    return render(request, 'authentication/login.html', context={'form': form})


from . import forms
def logout_user(request):
      logout(request)
      return redirect('login')
