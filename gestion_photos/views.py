import os
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Photo
from .forms import PhotoUploadForm
import numpy as np
import cv2
def index(request):
    return render(request, 'gestion_photos/index.html')

def liste_photos(request):
    photos = Photo.objects.all()
    return render(request, 'gestion_photos/liste_photos.html', {'photos': photos})

# Charge le classificateur pour la détection des visages (Haar Cascade fourni par OpenCV)
cascade_path = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
face_cascade = cv2.CascadeClassifier(cascade_path)

def traiter_image(request):
    if request.method == 'POST' and request.FILES.get('image'):
        image_upload = request.FILES['image']

        # Lire l'image avec OpenCV
        np_img = np.frombuffer(image_upload.read(), np.uint8)
        img = cv2.imdecode(np_img, cv2.IMREAD_COLOR)

        # Détection et recadrage des visages
        gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray_img, scaleFactor=1.1, minNeighbors=5, minSize=(50, 50))

        if len(faces) > 0:
            # Prend le premier visage détecté
            (x, y, w, h) = faces[0]
            cropped_img = img[y:y + h, x:x + w]

            # Sauvegarder l'image recadrée dans le système de fichiers
            processed_filename = f"face_{image_upload.name}"
            processed_path = os.path.join(settings.MEDIA_ROOT, 'processed', processed_filename)

            # Crée le dossier 'processed' s'il n'existe pas
            os.makedirs(os.path.dirname(processed_path), exist_ok=True)

            # Sauvegarde le fichier recadré
            cv2.imwrite(processed_path, cropped_img)

            # Génère l'URL pour afficher l'image
            processed_url = f"{settings.MEDIA_URL}processed/{processed_filename}"

            # Retourne la page résultat avec l'image recadrée
            return render(request, 'resultat.html', {'image_url': processed_url})

        else:
            # Aucun visage détecté
            return render(request, 'resultat.html', {'error': "Aucun visage détecté dans l'image."})

    return render(request, 'upload.html')

def liste_images_traitees(request):
    processed_dir = os.path.join(settings.MEDIA_ROOT, 'processed')
    processed_files = []

    # Vérifie que le dossier existe
    if os.path.exists(processed_dir):
        processed_files = [
            f"{settings.MEDIA_URL}processed/{filename}"
            for filename in os.listdir(processed_dir)
            if filename.endswith(('.png', '.jpg', '.jpeg'))
        ]

    return render(request, 'gestion_photos/liste_images_traitees.html', {'images': processed_files})

def success(request):
    return HttpResponse("Photo téléchargée avec succès!")

def upload_photo(request):
    if request.method == 'POST':
        form = PhotoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()  # Sauvegarde l'image et ses données dans la base de données
            return redirect('success')  # Redirige vers une page de succès
    else:
        form = PhotoUploadForm()

    return render(request, 'gestion_photos/upload.html', {'form': form})