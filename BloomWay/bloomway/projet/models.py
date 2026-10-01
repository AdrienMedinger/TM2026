from django.db import models
from django.contrib.auth.models import AbstractUser, User 
import datetime 
from django.db.models.signals import post_save, pre_save 
from django.dispatch import receiver




class Categorie(models.Model):
    categorie = models.CharField(max_length=100)
    description_image = models.TextField(blank=True, null=True)
    image_principale = models.ImageField(upload_to='categories/', blank=True, null=True)

    def __str__(self):
        return self.categorie

class Produit(models.Model) :
    nom = models.CharField(max_length=256)
    description = models.TextField()
    categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE, related_name='produits',null=True, blank=True)
    image_principale = models.ImageField(upload_to='produits/', blank=True,null=True)
    image_secondaire = models.ImageField(upload_to='produits/', blank=True,null=True)
    image_globale = models.ImageField(upload_to='produits/', blank=True,null=True)
    dispponibilité = models.BooleanField(default=True)
    date_création = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.nom
    


    
class Variante_produit(models.Model) :
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE, related_name='variantes')
    taille = models.CharField(max_length=64)
    couleur = models.CharField(max_length=64)
    prix = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    sku = models.CharField(max_length=64, unique=True)
    def __str__(self):
        return f"{self.produit.nom} - {self.taille} - {self.couleur} - {self.prix}Fr - {self.stock} en stock"

class User(AbstractUser):

    créateur ='créateur'
    utilisateur = 'utilisateur'
    Role_CHOICES = [
        (créateur, 'Créateur'),
        (utilisateur, 'Utilisateur'),
    ]
    role = models.CharField(max_length=20, choices=Role_CHOICES, default=utilisateur)
    photo_de_profil = models.ImageField(upload_to='users/', null=True, blank= True)
    adresse = models.CharField(max_length=256, null=True, blank=True)
    def __str__(self):
        return f"{self.username} - {self.role}"


class Panier(models.Model):
    utilisateur = models.OneToOneField(User, on_delete=models.CASCADE, related_name='panier')
    produit = models.ManyToManyField(Variante_produit, through='PanierProduit')
    date_création = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"Panier de {self.utilisateur.username}"
    
class PanierProduit(models.Model):
    panier = models.ForeignKey(Panier, on_delete=models.CASCADE)
    variante_produit = models.ForeignKey(Variante_produit, on_delete=models.CASCADE)
    quantite = models.PositiveIntegerField(default=1)
    class Meta:
        unique_together = ('panier', 'variante_produit')

        


class AdresseCommande(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='adresses_commande')

    nom_entier = models.CharField(max_length=255,default="")
    email = models.EmailField(max_length=255)
    adresse = models.CharField(max_length=255)
    ville = models.CharField(max_length=100)
    code_postal = models.CharField(max_length=20)
    pays = models.CharField(max_length=100)
    stripe_id = models.CharField(max_length=255, blank=True,null=True)
   

    def __str__(self):
        return f" AdresseCommande - {str(self.id)} "
    

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders',blank=True, null=True)

    nom_entier = models.CharField(max_length=255,default="")
    email = models.EmailField(max_length=255)
    address = models.TextField(max_length=10000)
    montant_payé = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    date_commande = models.DateTimeField(auto_now_add=True)

    payé = models.BooleanField(default=False)  # False = pas payé, True = payé
    envoyé = models.BooleanField(default=False)  # False = pas envoyé, True = envoyé 
    date_envoie = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"Order - {str(self.id)}"

# auto ajouter la date d'envoi lorsque l'order est marqué comme envoyé
@receiver(pre_save, sender=Order)
def set_date_envoie(sender, instance, **kwargs):
   if instance.pk:
       now = datetime.datetime.now()
       obj=sender._default_manager.get(pk=instance.pk)
       if instance.envoyé and not obj.envoyé:
              instance.date_envoie = now




class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    produit = models.ForeignKey(Produit, on_delete=models.SET_NULL, null=True) # SET_NUL pour ne pas perdre l'historique des commandes si le produit est supprimé
    variante_produit = models.ForeignKey(Variante_produit, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantité = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"OrderItem - {str(self.id)}"