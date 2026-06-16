from django.http import HttpResponse
from django.shortcuts import render
from . import forms 
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.conf import settings 
from .models import produit, variante_produit, User
from .models import categorie_produit 

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

def affichage_produit(request, produit_id):
    categorie = produit.objects.get(id=produit_id)


    produit = produit.objects.filter(categorie_produit=categorie)
    

    taille = request.GET.get('taille')
    couleur = request.GET.get('couleur')
    stock = request.GET.get('stock')
    prix_min = request.GET.get('prix_min')
    prix_max = request.GET.get('prix_max')

    if taille:
        produit = produit.filter(variantes__taille=taille)
    if couleur:
        produit = produit.filter(variantes__couleur=couleur)
    if stock:
        produit = produit.filter(variantes__stock__gte=stock)
    if prix_min:
        produit = produit.filter(variantes__prix__gte=prix_min)
    if prix_max:
        produit = produit.filter(variantes__prix__lte=prix_max)

    return render(request, 'projet/affichage_produit.html', {'categorie': categorie, 'produit': produit,})