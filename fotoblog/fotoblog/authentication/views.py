from django.shortcuts import render

# Create your views here.


# authentication/views.py


from . import forms


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
                message = f'Bonjour, {user.username}! Vous êtes connecté.'
            else:
                message = 'Identifiants invalides.'
    return render(request, 'authentication/login.html', context={'form': form})

from django.contrib.auth import authentification, login, logout 
from django.shortcuts import render, redirrect
from . import forms
def logout_user(request):
      logout(request)
      return redirect('login')
