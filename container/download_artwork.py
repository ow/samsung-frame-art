import requests
import os

# Setze deinen Unsplash API-Schlüssel hier
UNSPLASH_API_KEY = ''

# Unsplash API-Endpunkt für zufällige Fotos
UNSPLASH_API_URL = 'https://api.unsplash.com/photos/random'

# Verzeichnis zum Speichern der heruntergeladenen Bilder
IMAGES_DIRECTORY = 'images'

def download_random_artwork():
    try:
        # Führe die API-Anfrage durch
        response = requests.get(UNSPLASH_API_URL, params={'client_id': UNSPLASH_API_KEY})
        response.raise_for_status()  # Wirf eine Ausnahme bei einem Fehlerstatuscode

        # Extrahiere die URL des Fotos aus der Antwort
        photo_url = response.json()['urls']['regular']

        # Lade das Foto herunter und speichere es lokal
        response = requests.get(photo_url)
        response.raise_for_status()

        # Stelle sicher, dass das Verzeichnis existiert
        os.makedirs(IMAGES_DIRECTORY, exist_ok=True)

        # Extrahiere den Dateinamen aus der Bild-URL
        file_name = os.path.join(IMAGES_DIRECTORY, 'downloaded_artwork.jpg')

        # Schreibe die Bild-Bytes direkt in die Datei
        with open(file_name, 'wb') as f:
            f.write(response.content)

        print(f'Foto erfolgreich heruntergeladen und als {file_name} gespeichert.')

    except requests.exceptions.RequestException as e:
        print(f'Fehler beim Herunterladen des Fotos: {e}')

if __name__ == "__main__":
    download_random_artwork()
