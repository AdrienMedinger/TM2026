from django.db import models

class produit(models.Model) :
    nom = models.CharField(max_length=256)
    description = models.TextField()
    categorie = models.CharField(max_length=256)
    image_principale = models.ImageField(upload_to='produits/')
    dispponibilité = models.BooleanField(default=True)
    date_création = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.nom
    
class variante_produit(models.Model) :
    produit = models.ForeignKey(produit, on_delete=models.CASCADE, related_name='variantes')
    taille = models.CharField(max_length=64)
    couleur = models.CharField(max_length=64)
    prix = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    sku = models.CharField(max_length=64, unique=True)
    def __str__(self):
        return f"{self.produit.nom} - {self.taille} - {self.couleeur} - {self.prix}Fr - {self.stock} en stock"
