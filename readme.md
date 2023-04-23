# Samsung Frame Art Mode with your own folder of photos

I found uploading images to the Samsung Frame manually to be tedious, especially when using a very large set of images, like those from Google's Earth View image library. This Python script randomly picks an image from folder on your computer, then sends it to your TV and sets it as the active image automatically. 

Because Samsung TVs don't let you check if a file was already uploaded, every time the file is uploaded to the TV the script saves the filename and remote file ID in `uploaded_files.json` — if you run the script again and the file is already on the TV, the script will ensure it's not duplicated repeatedly on the TV.

## Using the script

- Install the required [Python library](https://github.com/xchwarze/samsung-tv-ws-api) that accesses the Samsung TV API by running: `pip3 install "git+https://github.com/xchwarze/samsung-tv-ws-api.git#egg=samsungtvws[async,encrypted]"`
- Set a static IP for your TV, then change `tv = SamsungTVWS('192.168.0.9')` in `art.py` to your own IP address
- Create a folder of images you want to upload at `/images`
- Run the script for the first time: `python3 art.py`
- Accept the permissions request using your Samsung TV remote
- Run the script again and enjoy your art!

### Need images?
I wanted to do this with the [Google Earth View images](https://earth.google.com/web/data=CiQSIhIgYWJiZTA3ZGNkODM3MTFlNmIzMmFhNWViMDBhYjQ5ZmM), which are lovely and of which there are many thousands of images. I can't distribute these, but you can learn how to [download these here](https://www.gtricks.com/earth/download-all-google-earth-view-wallpapers/)—they work really well with this library.

### Caveats

- Only works with JPG and PNG files
- Needs to be manually run every time you want to upload/change photos. This works great if you can set a cron job to run at the frequency you want the photos changed. 
- Don't blame me if your TV breaks, this was just a project for myself