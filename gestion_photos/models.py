from django.db import models

class Photo(models.Model):
    titre = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='photos/')  # Stocke les images dans le dossier "media/photos/"
    date_creation = models.DateTimeField(auto_now_add=True)

