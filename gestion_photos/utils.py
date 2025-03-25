import os
import cv2
import segno
import shutil

def recadrer_visage(photo_path, cascade_path):
    """
    Recadre la photo pour ne garder que le visage détecté.
    :param photo_path: Chemin du fichier photo à traiter.
    :param cascade_path: Chemin du fichier cascade Haar pour la détection des visages.
    :return: L'image recadrée (visage) ou une erreur.
    """
    try:
        # Charger l'image
        image = cv2.imread(photo_path)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Charger le modèle de détection des visages
        face_cascade = cv2.CascadeClassifier(cascade_path)

        # Détecter les visages
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(50, 50))

        if len(faces) == 0:
            return None, "Aucun visage détecté."

        # Prendre le premier visage détecté
        x, y, w, h = faces[0]
        cropped_face = image[y:y+h, x:x+w]

        return cropped_face, None

    except Exception as e:
        return None, f"Erreur lors du recadrage : {str(e)}"

def generer_qr_code_segno(data, output_path):
    """
    Génère un QR Code à partir des données fournies et le sauvegarde en tant qu'image PNG.
    :param data: Les données à inclure dans le QR Code (par exemple : "Nom: Dupont, Prénom: Jean").
    :param output_path: Chemin du fichier où sauvegarder l'image PNG du QR Code.
    """
    qr = segno.make(data)
    qr.save(output_path, scale=10)

def renommer_fichier_photo(photo_path, nom, prenom, output_directory):
    """
    Renomme un fichier photo avec le nom et prénom du sujet/élève.
    :param photo_path: Chemin du fichier photo d'origine.
    :param nom: Nom du sujet/élève.
    :param prenom: Prénom du sujet/élève.
    :param output_directory: Répertoire où sauvegarder le fichier renommé.
    :return: Chemin complet du fichier renommé.
    """
    # Créer le dossier de sortie s'il n'existe pas
    os.makedirs(output_directory, exist_ok=True)

    # Déterminer le nouveau nom de fichier
    new_filename = f"{prenom}_{nom}.jpg"
    output_path = os.path.join(output_directory, new_filename)

    # Copier et renommer le fichier
    shutil.copy(photo_path, output_path)

    return output_path