"""
URL configuration for bloomway project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
import projet.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', projet.views.login_page, name='login'),
    path('logout/', projet.views.logout_page, name='logout'),
    path('home/', projet.views.home, name='home'),
    path('signup/', projet.views.signup_page, name='signup'),
    path('filtre_produit/', projet.views.filtre_produit, name='filtre_produit'),
    path('panier/', projet.views.affichage_panier, name='affichage_panier'),
    path('panier/modifier/<int:variante_produit_id>/<str:action>/', projet.views.modifier_quantite_panier, name='modifier_quantite_panier'),
    path('panier/ajouter/<int:variante_produit_id>/', projet.views.ajouter_au_panier, name='ajouter_au_panier'),
    path('panier/supprimer/<int:variante_produit_id>/', projet.views.supprimer_du_panier, name='supprimer_du_panier'),
]
