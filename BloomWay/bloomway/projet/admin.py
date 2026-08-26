from django.contrib import admin
from django.contrib.auth.admin import Group
from .models import Produit, Variante_produit, User, Panier, PanierProduit, Order, OrderItem, Categorie, AdresseCommande
# Register your models here.

admin.site.unregister(Group)

class UserAdmin(admin.ModelAdmin):
    model = User

    fields = ["username"]

# register User with custom UserAdmin
admin.site.register(User, UserAdmin)

admin.site.register(Produit)
admin.site.register(Variante_produit)
admin.site.register(Panier)
admin.site.register(PanierProduit)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Categorie)
admin.site.register(AdresseCommande)

# créer un orderitem inline
class OrderItemInline(admin.StackedInline): 
    model = OrderItem
    extra = 0


# etendre l'admin de Order pour inclure les OrderItem
class OrderAdmin(admin.ModelAdmin):
    model = Order
    readonly_fields = ["date_commande"]
    fields = ["user", "nom_entier", "email", "address", "montant_payé","date_commande", "envoyé", "date_envoie"]
    inlines = [OrderItemInline]


admin.site.unregister(Order)
admin.site.register(Order, OrderAdmin)