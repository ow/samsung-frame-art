# Samsung Frame Art Mode++
![TV with some art on it ](https://i.imgur.com/BunHdwb.jpeg)

I love the Samsung Frame TV—which is designed to look like art when it's off—but I got tired of paying a monthly fee for the official art. I also found uploading images to it manually to be tedious, especially when using a very large set of images, like those from Google's Earth View image library. 

This Python script allows you to change your Samsung Frame's art based on a folder of images on your computer. The script picks an image from folder on your computer, then sends it to your TV and sets it as the active image automatically—it also does its best to try not repeatedly upload the same photo to your TV. 

You can use this script with a folder of thousands of images to have your Samsung Frame TV change art constantly, for free. All you need is your own images!

## Using the script

- Install the required [Python library](https://github.com/xchwarze/samsung-tv-ws-api) that accesses the Samsung TV API by running: `pip3 install "git+https://github.com/xchwarze/samsung-tv-ws-api.git#egg=samsungtvws[async,encrypted]"`
- Set a static IP for your TV, then change `tv = SamsungTVWS('192.168.0.9')` in `art.py` to your own IP address
- Create a folder of images you want to upload at `./images`
- Run the script for the first time: `python3 art.py`
- Accept the permissions request using your Samsung TV remote
- Run the script again and enjoy your art! Anytime you want the image to change, run the script again.

If you have a Raspberry Pi or other computer that is always on, you could set up a cronjob to change it on a regular rotation! To do this, you just need to: 

- Create a Bash file like `art.sh` then put something like this in it:
`cd /Users/your-username/samsung-frame-art && /Library/Frameworks/Python.framework/Versions/3.9/bin/python3 /Users/your-username/samsung-frame-art/art.sh`
- Make sure it's executable: `chmod +x art.sh`
- Add a cron job with `crontab -e` that runs regularly. I do mine every 12 hours, so it looks like this: `0 */12 * * * /Users/your-username/samsung-frame-art/art.sh`

### Need images?
I wanted to do this with the [Google Earth View images](https://earth.google.com/web/data=CiQSIhIgYWJiZTA3ZGNkODM3MTFlNmIzMmFhNWViMDBhYjQ5ZmM), which are lovely and of which there are many thousands of images. I can't distribute these, but you can learn how to [download these here](https://www.gtricks.com/earth/download-all-google-earth-view-wallpapers/)—they work really well with this library.

### Caveats

- Because Samsung TVs don't let you check if a file was already uploaded, every time the file is uploaded to the TV the script saves the filename and remote file ID in `uploaded_files.json` — if you run the script again and the file is already on the TV, the script will ensure it's not duplicated repeatedly on the TV.
- Only works with JPG and PNG files
- Needs to be manually run every time you want to upload/change photos. This works great if you can set a cron job to run at the frequency you want the photos changed. 
- Don't blame me if your TV breaks, this was just a project for myself
- I have no idea how many images is the maximum on these TVs. I've used this about 1000 times so far and my 2022 Samsung Frame still seems to accept images.

### To-Do

- This project does not do anything with the aspect ratio of images. It only really handles landscape and does not fit them to the display; I'd like to figure out how to auto-resize or crop these before uploading.