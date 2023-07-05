import base64
import json
import os
from urllib.request import urlopen
from urllib.parse import urljoin
from shlex import quote

REMOTE_URL = "https://www.gstatic.com/prettyearth/"
REMOTE_IDS_PATH = "ids.json"
LOCAL_PATH = "images"

def download_wallpapers():
    create_wallpapers_path()

    print(":: Downloading Google Maps wallpapers.")
    downloaded = 0

    for wallpaper_id in get_wallpaper_ids():
        if downloaded == int(os.environ.get("MAX_DOWNLOADS", 10)):
            break

        wallpaper_path = get_wallpaper_path(wallpaper_id)
        if os.path.exists(wallpaper_path):
            print("Wallpaper exists: " + wallpaper_id)
            continue

        print("Wallpaper download: " + wallpaper_id)
        downloaded += 1
        wallpaper_info = get_wallpaper_info(wallpaper_id)
        location = ", ".join(wallpaper_info["geocode"].values())
        if "Russia" in location:
            continue

        wallpaper_bytes = get_wallpaper_bytes(wallpaper_info["dataUri"])
        download_wallpaper(wallpaper_path, wallpaper_bytes)

        convert_cmd = " ".join((
            "convert",
            wallpaper_path,
            "-background transparent",
            "-fill white",
            "-font DejaVu-Sans",
            "-size 600x100",
            "-pointsize 32",
            "-gravity southeast",
            "-stroke black -strokewidth 3 -annotate +25+25 {}".format(quote(location)),
            "-stroke none -annotate +25+25 {}".format(quote(location)),
            wallpaper_path,
        ))
        os.system(convert_cmd)


def create_wallpapers_path():
    wallpapers_path = get_wallpapers_path()

    if not os.path.exists(wallpapers_path):
        os.makedirs(wallpapers_path)


def get_wallpapers_path():
    wallpapers_path = os.path.dirname(os.path.realpath(__file__))

    return os.path.abspath(os.path.join(wallpapers_path, LOCAL_PATH))


def get_wallpaper_ids():
    with open(get_wallpaper_ids_path()) as wallpaper_ids_file:
        return json.load(wallpaper_ids_file)


def get_wallpaper_ids_path():
    return os.path.join(os.path.dirname(__file__), REMOTE_IDS_PATH)


def get_wallpaper_info(wallpaper_id):
    wallpaper_info_url = get_wallpaper_info_url(wallpaper_id)

    return json.load(urlopen(wallpaper_info_url))


def get_wallpaper_info_url(wallpaper_id):
    return urljoin(REMOTE_URL, "{id}.json".format(id=wallpaper_id))


def get_wallpaper_path(wallpaper_id):
    wallpapers_path = get_wallpapers_path()
    wallpaper_filename = "{id}.jpg".format(id=wallpaper_id)

    return os.path.join(wallpapers_path, wallpaper_filename)


def get_wallpaper_bytes(wallpaper_info):
    bytes_start_position = wallpaper_info.index(",") + 1

    return base64.b64decode(wallpaper_info[bytes_start_position:])


def download_wallpaper(wallpaper_path, wallpaper_bytes):
    with open(wallpaper_path, "wb") as wallpaper_file:
        wallpaper_file.write(wallpaper_bytes)


if __name__ == "__main__":
    download_wallpapers()
