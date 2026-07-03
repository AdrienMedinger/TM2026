from django.contrib import admin
from django.contrib.auth.admin import Group
from .models import Produit, Variante_produit, User, Panier, PanierProduit, Order, OrderItem
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