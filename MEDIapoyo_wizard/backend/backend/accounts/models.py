
# accounts/models.py
from django.db import models

class CustomUser(models.Model):
    # Champs pour le modèle d'utilisateur
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)

    def __str__(self):
        return self.username