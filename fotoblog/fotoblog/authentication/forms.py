from django import forms 

class loginform (forms.form) :
    username = forms.CharField(max_length=63,label= "nom d'utilisateur")
    password = forms.CharField(max_length=63, widget= forms.PasswordInput, label= "mot de passe")