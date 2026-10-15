from django.http import HttpResponse
from django.shortcuts import render
from . import forms
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.conf import settings 
from .models import Produit, Variante_produit, User, Panier, PanierProduit, Categorie, AdresseCommande, Order, OrderItem
from .forms import ShippingForm, PaiementForm
from django.contrib import messages
from django.db import transaction
from django.db.models import F
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.http import require_POST
from django.core.mail import send_mail










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
    produits = Produit.objects.prefetch_related('variantes').all()

    if query:
        produits = produits.filter(nom__icontains=query)



    variante_produit=Variante_produit.objects.all()



    categories = Categorie.objects.all()
   

   

    context = {
        'produits': produits.distinct(),
        'categories': categories,
        'variantes_produit': variante_produit,
        'query': query,
    }

    
     
    return render(request, 'projet/affichage_produit.html', context)


def detail(request, Produit_id=None):
    produit = get_object_or_404(Produit, id=Produit_id)

    # toutes les variantes du produit
    variantes= Variante_produit.objects.filter(produit=produit)

    # première variante pas défaut 
    variante= variantes.first()

    # taille selectiionnée par l'utilisateur
    taille_selectionnee = request.GET.get('variante')
    
    # si l'utilisateur choisi une taille
    variante_id = request.GET.get('variante')
    if variante_id:
        variante_choisie = variantes.filter(id=variante_id).first()

        if variante_choisie:
            variante=variante_choisie 

    context = {
        'produit': produit,
        'variantes': variantes,
        'variante':variante,
        'variantes_id':variante_id,
        'taille_selectionnee':taille_selectionnee,
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

@login_required
def affichage_panier(request):
    mon_panier, created = Panier.objects.get_or_create(utilisateur=request.user)

    mon_panier1 = PanierProduit.objects.filter(panier=mon_panier)

    total = 0
    for item in mon_panier1:
        total += item.variante_produit.prix * item.quantite
    return render(request, 'projet/panier.html', {'panier': mon_panier, 'total': total, 'mon_panier1': mon_panier1})

def panier_et_total(user):
    panier, created = Panier.objects.get_or_create(utilisateur=user)
    items = PanierProduit.objects.filter(panier=panier).select_related('variante_produit')
    total = sum(item.variante_produit.prix * item.quantite for item in items)
    return panier, items, total

@login_required
def ajouter_au_panier(request, variante_produit_id):
    if request.method == 'POST':
        variante = get_object_or_404(Variante_produit, id=variante_produit_id)
        panier, created = Panier.objects.get_or_create(utilisateur=request.user)
        panier_produit, created = PanierProduit.objects.get_or_create(
            panier=panier, 
            variante_produit=variante,
            defaults={'quantite': 0}
        )

        if panier_produit.quantite >= variante.stock:
            messages.error(request, f"Le produit {variante.produit.nom} n'a pas assez de stock.")
        else:
            panier_produit.quantite += 1
            panier_produit.save()
    return redirect('affichage_panier')

@login_required
def supprimer_du_panier(request, variante_produit_id):
    variante = get_object_or_404(Variante_produit, id=variante_produit_id)
    panier = get_object_or_404(Panier, utilisateur=request.user)
    panier_produit = get_object_or_404(PanierProduit, panier=panier, variante_produit=variante)
    panier_produit.delete()
    return redirect('affichage_panier')

@login_required
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

@login_required
def checkout(request):
    panier, items, total = panier_et_total(request.user)
   
    if not items.exists():
        messages.info(request, " votre panier est vide. ")
        return redirect('affichage_panier')

    adresse = AdresseCommande.objects.filter(user=request.user).first()
    shipping_form = ShippingForm(request.POST or None, instance=adresse)

   
    return render(request, 'projet/checkout.html', {'panier': panier, 'panier_produits': items,'total': total,'shipping_form':shipping_form})
    
    

@login_required
def facturation_info(request):
    if request.method != "POST":
        return redirect("checkout")

    panier, items, total = panier_et_total(request.user)
    if not items.exists():
        messages.info(request, "Votre panier est vide.")
        return redirect('affichage_panier')

    adresse = AdresseCommande.objects.filter(user=request.user).first()
    shipping_form = ShippingForm(request.POST or None, instance=adresse)

    if not shipping_form.is_valid():
        messages.error(request, "Veuillez remplir correctement le formulaire de livraison.")
        return render(request, 'projet/checkout.html', {'panier': panier, 'panier_produits': items,'total': total,'shipping_form':shipping_form})


    shipping_info = shipping_form.save(commit=False)
    shipping_info.user = request.user
    shipping_info.save()

    
    # créer une session pour stocker les informations de livraison
    request.session['ma_livraison'] = {
        'nom_entier': shipping_info.nom_entier,
        'email': shipping_info.email,
        'adresse': shipping_info.adresse,
        'ville': shipping_info.ville,
        'code_postal': shipping_info.code_postal,
        'pays': shipping_info.pays,
    }

  
    return render (request, 'projet/facturation_info.html',{'panier': panier, 'panier_produits': items,'total':total,'shipping_info': shipping_info, 'paiement_form': PaiementForm()})

    
def paiement (request):
    if request.method != "POST":
        return redirect("checkout")
    shipping_id = request.POST.get("shipping_id")

    shipping_info = get_object_or_404(AdresseCommande,id = shipping_id,user = request.user)
            
    
    return render(request,'projet/paiement.html', {"shipping_info" : shipping_info})
@login_required
@require_POST
def process_order(request):
    if request.method != "POST":
        return redirect("facturation_info")
    
    panier, items, total = panier_et_total(request.user)

    livraison = request.session.get('ma_livraison')

    if not livraison or not items.exists():
        messages.error(request, "Votre panier est vide ou les informations de livraison sont manquantes.")
        return redirect('checkout')

    adresses_txt = f"{livraison['adresse']}\n{livraison['ville']}\n{livraison['code_postal']}\n{livraison['pays']}"

    with transaction.atomic():  # soit tout est créer soit rien
        # vérifier le stock (vérouillé pour eviter deux achats simultanés du même produit)
        for item in items:
            variante = Variante_produit.objects.select_for_update().get(id=item.variante_produit.id)
            if variante.stock < item.quantite:
                messages.error(request, f"Le produit {variante.produit.nom} n'a pas assez de stock.")
                return redirect('affichage_panier')


        # créer la commande

        order = Order.objects.create(
            user=request.user,
            nom_entier=livraison['nom_entier'],
            email=livraison['email'],
            address=adresses_txt,
            montant_payé=total,
            payé=True,  # marquer comme payé
        )

        # baisser le stock à chaque commande 

        for item in items:
            variante =item.variante_produit
            OrderItem.objects.create(
                order=order,
                produit=variante.produit,
                variante_produit=variante,
                user=request.user,
                price=variante.prix,
                quantité=item.quantite,
            )
            Variante_produit.objects.filter(pk=variante.pk).update(stock=F('stock') - item.quantite)

        # vider le panier après la commande
        items.delete()


        send_mail(
            subject=f" confirmation de votre commande numéro {order.id}",
            message=f"Bonjour {order.nom_entier},\n\nMerci pour votre commande.",
            from_email="boutique@bloomway.ch",
            recipient_list=[order.email]
        )



    request.session.pop('ma_livraison', None)  # supprimer les informations de livraison de la session
    messages.success(request, "Votre commande a été traitée avec succès.")
    return redirect('ma_commande', pk=order.id)

@login_required
def mes_commandes(request):
    total = panier_et_total(request.user)
    orders = Order.objects.filter(user=request.user).order_by('-date_commande')
    return render(request, 'projet/mes_commandes.html', {'orders': orders, 'total': total})

@login_required
def ma_commande(request,pk):
    order = get_object_or_404(Order, id=pk, user=request.user)
    items = order.items.select_related('produit', 'variante_produit')
    total = sum(item.price * item.quantité for item in items)

    return render(request, 'projet/ma_commande.html', {'order': order, 'order_items': items, 'total': total})





# --------- tout ce qui est pour les admin -----------------


@staff_member_required
def pas_envoye_dashboard(request):

    if request.method == 'POST':
       order = get_object_or_404(Order, id=request.POST.get('order_id'))
       order.envoyé = True
       order.save()    # save() et pas update() pour que cela remplisse date_envoie
       messages.success(request, f"La commande {order.id} a été marquée comme envoyée.")

    orders = Order.objects.filter(envoyé=False).order_by('-date_commande')
    return render(request, 'projet/pas_envoye_dashboard.html', {'orders': orders})


@staff_member_required
def envoye_dashboard(request):

    if request.method == 'POST':
       order = get_object_or_404(Order, id=request.POST.get('order_id'))
       order.envoyé = False
       order.save()    # save() et pas update() pour que cela remplisse date_envoie
       messages.success(request, f"La commande {order.id} a été marquée comme non envoyée.")

    orders = Order.objects.filter(envoyé=True).order_by('-date_commande')
    return render(request, 'projet/envoye_dashboard.html', {'orders': orders})


@staff_member_required
def commande(request, pk):
    order = get_object_or_404(Order, id=pk)
    items = order.items.select_related('produit', 'variante_produit')
    total = panier_et_total(request.user)
    return render(request, 'projet/commande.html', {'order': order, 'order_items': items, 'total': total})
    











