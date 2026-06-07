from django import forms 

class loginForm(forms.Form):
    username = forms.CharField(label='Nom d utilisateur', max_length=64)
    password = forms.CharField(label='Mot de passe', widget=forms.PasswordInput, max_length=64)
