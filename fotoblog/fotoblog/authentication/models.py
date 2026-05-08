from django.db import models

# Create your models here.


from django .contrib.auth.models import AbstractUser

class user(AbstractUser) :

    creator = "creator"
    subscriber = "subscriber"

    role_choices = (
       ( creator,"creator"),
       (subscriber,"subscriber"),
    )

    profile_picture = models.ImageField(verbose_name = "photo de profil")
    role = models.CharField(max_length=30, choices=role_choices, verbose_name="Rôle")