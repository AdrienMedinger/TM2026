from django.http import HttpResponse
from django.shortcuts import render
from . import forms 
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.conf import settings 
from .models import Produit, Variante_produit, User, Panier, PanierProduit, Categorie

def base(request):
    return render(request, 'projet/base.html')

def about_us(request):
    return render(request, 'projet/about_us.html')
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
    produits = Produit.objects.all()
    variante_produit=Variante_produit.objects.all()
    categories = Categorie.objects.all()

    query = request.GET.get("q")
    if query:
        produits = Produit.objects.filter(nom__icontains=query)
    else:
        produits = Produit.objects.all()
    
    if request.GET.get('filter'):
        produits = filtre_produit(request, produits)

    mon_panier= request.session.get('panier', {})

    context = {
        'produits': produits,
        'panier': mon_panier,
        'query': query,
        'variantes_produit': variante_produit,
        'categories': categories,
    }

    return render(request, 'projet/home.html', context)

def signup_page(request):
    form = forms.signupForm()
    if request.method == 'POST':
        form = forms.signupForm(request.POST, request.FILES)
        if form.is_valid():
            user =form.save()
            return redirect('login')
    return render(request, 'projet/signup.html', context={'form': form})

def filtre_produit(request, variante_produit_id = None):
    produits = Produit.objects.all()

    variante_produit=Variante_produit.objects.all()

    categories = Categorie.objects.all()
    categorie_selectionnee = request.GET.get('categorie','')
    


    if categorie_selectionnee :
        produits = produits.filter(categorie__categorie=categorie_selectionnee)

        taille = request.GET.get('taille')
        couleur = request.GET.get('couleur')
        stock = request.GET.get('stock')
        prix_min = request.GET.get('prix_min')
        prix_max = request.GET.get('prix_max')

        if taille:
            produits = produits.filter(variantes__taille=taille)
        
        if couleur:
             produits = produits.filter(variantes__couleur=couleur)
       
        if stock:
             produits = produits.filter(variantes__stock__gte=stock)
       
        if prix_min:
            produits = produits.filter(variantes__prix__gte=prix_min)
        
        if prix_max:
            produits = produits.filter(variantes__prix__lte=prix_max)
    
        
    context = {
        'produits': produits.distinct(),
        'categories': categories,
        'categorie_selectionnee': categorie_selectionnee,
        'variantes_produit': variante_produit,}   

    
    print("CATEGORIES=",list(categories))
    return render(request, 'projet/filtre_produit.html', context)


def affichage_panier(request):
    mon_panier, created = Panier.objects.get_or_create(utilisateur=request.user)
    return render(request, 'projet/panier.html', {'panier': mon_panier})

def ajouter_au_panier(request, variante_produit_id):
    variante = get_object_or_404(Variante_produit, id=variante_produit_id)
    panier, created = Panier.objects.get_or_create(utilisateur=request.user)
    panier_produit, created = PanierProduit.objects.get_or_create(panier=panier, variante_produit=variante)
    panier_produit.quantite += 1
    panier_produit.save()
    return redirect('affichage_panier')

def supprimer_du_panier(request, variante_produit_id):
    variante = get_object_or_404(Variante_produit, id=variante_produit_id)
    panier = get_object_or_404(Panier, utilisateur=request.user)
    panier_produit = get_object_or_404(PanierProduit, panier=panier, variante_produit=variante)
    panier_produit.delete()
    return redirect('affichage_panier')

def modifier_quantite_panier(request, variante_produit_id, action):
    variante = get_object_or_404(Variante_produit, id=variante_produit_id)
    panier = get_object_or_404(Panier, utilisateur=request.user)
    panier_produit = get_object_or_404(PanierProduit, panier=panier, variante_produit=variante)

    if action == 'plus':
        panier_produit.quantite += 1
        panier_produit.save()
    elif action == 'moins':
        if panier_produit.quantite > 1:
            panier_produit.quantite -= 1
            panier_produit.save()
        else:
            panier_produit.delete()
    return redirect('affichage_panier')

def checkout(request):
    panier= get_object_or_404(Panier, utilisateur=request.user)
    panier_produits=PanierProduit.objects.filter(panier=panier)

    if not panier_produits.exists():
        return redirect('panier')
    
    print("panier:", panier)
    print("panier_produits:", panier_produits)

    return redirect('panier')

