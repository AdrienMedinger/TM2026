from django.http import HttpResponse
from django.shortcuts import render
from . import forms 
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings 



def login_page(request):
    form = forms.loginForm()
    message =''
    if request.method == 'POST':
        form = forms.loginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )
            if user is not None:
                login(request, user)
                message = 'Connexion réussie'
                return redirect('home')
            else: 
                message = 'Identifiants invalides'
    return render(request, 'projet/login.html', {'form': form, 'message': message})
            

def logout_page(request):
    logout(request)
    return redirect('login')


@login_required
def home(request):
    return render(request, 'projet/home.html')

def signup_page(request):
    form = forms.signupForm()
    if request.method == 'POST':
        form = forms.signupForm(request.POST, request.FILES)
        if form.is_valid():
            user =form.save()
            return redirect('login')
    return render(request, 'projet/signup.html', context={'form': form})