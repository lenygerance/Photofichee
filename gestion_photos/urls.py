from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # Page d'accueil
    path('liste/', views.liste_photos, name='liste_photos'),
    path('upload/', views.upload_photo, name='upload_photo'),  # Pour le formulaire de base
    path('traiter_image/', views.traiter_image, name='traiter_image'),  # Pour le formulaire de traitement
    path('success/', views.success, name='success'),  # Vue de succès après l'upload
    path('images-traitees/', views.liste_images_traitees, name='liste_images_traitees'),
]
