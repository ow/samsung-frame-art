import os
import requests
import logging
import argparse
from datetime import datetime

# Unsplash API-Endpunkt für zufällige Fotos
UNSPLASH_API_URL = 'https://api.unsplash.com/photos/random/'

# Verzeichnis zum Speichern der heruntergeladenen Bilder
IMAGES_DIRECTORY = 'images'

# Increase debug level
logging.basicConfig(level=logging.INFO)

def download_random_artworks(num_images):
    unsplash_api_key = os.getenv('UNSPLASH_API_KEY')
    if not unsplash_api_key:
        print('Error: UNSPLASH_API_KEY is not set.')
        return

    try:
        for _ in range(num_images):
            # Führe die API-Anfrage durch
            response = requests.get(UNSPLASH_API_URL, params={'client_id': unsplash_api_key, 'orientation':'landscape'})
            response.raise_for_status()  # Wirf eine Ausnahme bei einem Fehlerstatuscode

            # Extrahiere die URL des Fotos aus der Antwort
            photo_url = response.json()['urls']['regular']

            # Stelle sicher, dass das Verzeichnis existiert
            os.makedirs(IMAGES_DIRECTORY, exist_ok=True)

            # Generiere einen eindeutigen Dateinamen basierend auf dem aktuellen Zeitstempel
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            file_name = os.path.join(IMAGES_DIRECTORY, f'downloaded_artwork_{timestamp}.jpg')

            # Lade das Foto herunter und speichere es lokal
            response = requests.get(photo_url)
            response.raise_for_status()

            with open(file_name, 'wb') as f:
                f.write(response.content)

            logging.info(f'Bild {_ + 1} erfolgreich heruntergeladen und als {file_name} gespeichert.')

    except requests.exceptions.RequestException as e:
        logging.error(f'Fehler beim Herunterladen der Bilder: {e}')

if __name__ == "__main__":
    # Füge einen Befehlszeilenargument-Parser hinzu
    parser = argparse.ArgumentParser(description='Unsplash Image Downloader')
    parser.add_argument('--num_images', type=int, default=1, help='Anzahl der herunterzuladenden Bilder')

    # Parse die Befehlszeilenargumente
    args = parser.parse_args()

    # Rufe die Funktion mit der angegebenen Anzahl der Bilder auf
    download_random_artworks(args.num_images)
