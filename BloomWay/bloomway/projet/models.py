from django.db import models
from django.contrib.auth.models import AbstractUser, User 
import datetime 

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

        
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders',blank=True, null=True)

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    address = models.CharField(max_length=255, default='', blank=True)
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)
    strip_id = models.CharField(max_length=255, blank=True,)

    status = models.BooleanField(default=False)  # False = not shipped, True = shipped

    class Meta:
        ordering = ('-created_at',)
        indexes =[
            models.Index(fields=['-created_at']),       
        ]
    def __str__(self):
        return f'Order {self.id}'
    
    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())
    

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE, related_name='order_items')
    variante_produit = models.ForeignKey(Variante_produit, on_delete=models.CASCADE, related_name='order_items')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'Ligne {self.id} de la commande {self.order.id}'

    def get_cost(self):
        return self.price * self.quantity
