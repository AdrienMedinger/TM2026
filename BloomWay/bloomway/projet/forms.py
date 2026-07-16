from django import forms 
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from .models import AdresseCommande

class loginForm(forms.Form):
    username = forms.CharField(label='Nom d utilisateur', max_length=64)
    password = forms.CharField(label='Mot de passe', widget=forms.PasswordInput, max_length=64)

class signupForm(UserCreationForm):
    class Meta (UserCreationForm.Meta):
        model = get_user_model()
        fields = ['username', 'email', 'first_name', 'last_name', 'role', 'photo_de_profil', 'adresse'] 


class ShippingForm(forms.ModelForm):
    class Meta:
        model= AdresseCommande
        fields= [
            "nom_entier",
            "adresse",
            "ville",
            "code_postal",
            "pays", 
            "stripe_id", 
   
        ]
   