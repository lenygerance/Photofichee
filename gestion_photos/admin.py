from django.contrib import admin
from .models import Photo

# Enregistre le modèle Photo
@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ('titre', 'description', 'image')  # La liste  des Colonnes visibles dans la liste
    search_fields = ('titre',)  # Ajoute une barre de recherche sur le titre
