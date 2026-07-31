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
            
        ]


class PaiementForm(forms.Form):
    carte_nom = forms.CharField(label="", widget= forms.TextInput(attrs={'class':'form-control', 'placeholder':'nom de la carte'}),required=True)
    carte_numéro = forms.CharField(label="", widget= forms.TextInput(attrs={'class':'form-control', 'placeholder':'numéro de la carte'}),required=True)
    carte_date_dexpiration = forms.CharField(label="", widget= forms.TextInput(attrs={'class':'form-control', 'placeholder':'date dexpiration de la carte'}),required=True)
    carte_cvv = forms.CharField(label="", widget= forms.TextInput(attrs={'class':'form-control', 'placeholder':'cvv code'}),required=True)
    carte_adresse = forms.CharField(label="", widget= forms.TextInput(attrs={'class':'form-control', 'placeholder':'adresse de paiement'}),required=True)
    carte_ville = forms.CharField(label="", widget= forms.TextInput(attrs={'class':'form-control', 'placeholder':'ville de paiement'}),required=True)
    carte_code_postal = forms.CharField(label="", widget= forms.TextInput(attrs={'class':'form-control', 'placeholder':'code postale'}),required=True)
    carte_pays = forms.CharField(label="", widget= forms.TextInput(attrs={'class':'form-control', 'placeholder':'pays de paiement'}),required=True)

