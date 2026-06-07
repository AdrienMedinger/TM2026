from django.http import HttpResponse
from django.shortcuts import render
from . import forms 
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect


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