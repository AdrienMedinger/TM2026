from django.http import HttpResponse
from django.shortcuts import render
from . import forms
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.conf import settings 
from .models import Produit, Variante_produit, User, Panier, PanierProduit, Categorie, AdresseCommande
from .forms import ShippingForm
def base(request):

    produits = Produit.objects.all()
    variante_produit=Variante_produit.objects.all()
    categories = Categorie.objects.all()


    

    mon_panier= request.session.get('panier', {})



   
    context = {
        'produits': produits,
        'panier': mon_panier,
        'variantes_produit': variante_produit,
        'categories': categories,
    }
 
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

    
    context = {
        'produits': produits,
        'variantes_produit': variante_produit,
        'categories': categories,
    }

    return render(request, 'projet/home.html', context)


def affichage_produit(request):
    query = request.GET.get("q", "")
    produits = Produit.objects.all()

    if query:
        produits = produits.filter(nom__icontains=query)


    context = {
        'produits': produits,
        'query': query,
    }
     
    return render(request, 'projet/affichage_produit.html', context)


def detail(request, Produit_id=None):
    produit = get_object_or_404(Produit, id=Produit_id)
    variante= Variante_produit.objects.filter(produit=produit)
    context = {
        'produit': produit,
    }
    return render(request, 'projet/detail.html', context)

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
    if request.method == 'POST':
        variante = get_object_or_404(Variante_produit, id=variante_produit_id)
        panier, created = Panier.objects.get_or_create(utilisateur=request.user)
        panier_produit, created = PanierProduit.objects.get_or_create(
            panier=panier, 
            variante_produit=variante,
            defaults={'quantite': 0}
        )

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

    if action == 'augmenter':
        panier_produit.quantite += 1
        panier_produit.save()
    elif action == 'diminuer':
        if panier_produit.quantite > 1:
            panier_produit.quantite -= 1
            panier_produit.save()
        else:
            panier_produit.delete()
    return redirect('affichage_panier')


def payment_success(request):
    return render(request, 'projet/payment_success.html')

def checkout(request):
    panier= get_object_or_404(Panier, utilisateur=request.user)
    panier_produits=PanierProduit.objects.filter(panier=panier)

    if not panier_produits.exists():
        return redirect('panier')
    
    total = 0

    for panier_produit in panier_produits:
        total += (
            panier_produit.variante_produit.prix*panier_produit.quantite

        )

    if request.user.is_authenticated:
        # checkout comme utilisateur enregistré
        shipping_user= AdresseCommande.objects.filter(user__id= request.user.id).first()
        shipping_form = ShippingForm(request.POST or None, instance= shipping_user)
        return render(request, 'projet/checkout.html', {'panier': panier, 'panier_produits': panier_produits,'total': total,'shipping_form':shipping_form})
    
    


def facturation_info(request):
     panier= get_object_or_404(Panier, utilisateur=request.user)
     panier_produits=PanierProduit.objects.filter(panier=panier)

     shipping_form = request.POST

     return render (request, 'projet/facturation.info_html',{'panier': panier, 'panier_produits': panier_produits})
    
        
   

