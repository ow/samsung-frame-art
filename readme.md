# Samsung Frame Art Mode++
![TV with some art on it ](https://i.imgur.com/BunHdwb.jpeg)

I love the Samsung Frame TV—which is designed to look like art when it's off—but I got tired of paying a monthly fee for the official art. I also found uploading images to it manually to be tedious, especially when using a very large set of images, like those from Google's Earth View image library. 

This Python script allows you to change your Samsung Frame's art based on a folder of images on your computer. The script picks an image from folder on your computer, then sends it to your TV and sets it as the active image automatically—it also does its best to try not repeatedly upload the same photo to your TV. 

You can use this script with a folder of thousands of images to have your Samsung Frame TV change art constantly, for free. All you need is your own images!

You can choose between a 'randomizer' mode that changes the image each time the script is run, or a bulk upload mode that puts all of your images on the TV at once and use the internal slideshow mode to have them shuffle.

## Using the script
*Note: I have tested this with the 2020 and 2021 Samsung Frame TVs, which I own. I am not sure if it works with other TVs yet—let me know if it works on your TV if it isn't listed here. There is a rumor that the 2022 Frame TVs no longer allow art mode to work with the API—if you try this with a 2022 Frame TV and it works (or doesn't) let me know; I probably can't help but it would be good for others to know.*

- Install the required [Python library](https://github.com/xchwarze/samsung-tv-ws-api) that accesses the Samsung TV API by running: `pip3 install "git+https://github.com/xchwarze/samsung-tv-ws-api.git#egg=samsungtvws[async,encrypted]"`
- Set a static IP for your TV, then change `tv = SamsungTVWS('192.168.0.9')` in `art.py` to your own IP address
- Create a folder of images you want to upload at `./images`
- Run the script for the first time: `python3 art.py`
- Accept the permissions request using your Samsung TV remote
- Choose the mode you want to use below

### Randomly change art mode
This is the mode I originally built this for, where a Raspberry Pi or something on your network runs the script and chooses a random image each time it runs. I prefer this mode because it allows me to just keep adding images and eventually they'll show up as art.

- Run the script with a simple `python3 art.py`

*To get images to change on a schedule:* If you have a Raspberry Pi or other computer that is always on, you could set up a cronjob to change it on a regular rotation! I do this on a Mac Mini, so these are the steps I used for that: 

- Create a Bash file like `art.sh` then put something like this in it:
`cd /Users/your-username/samsung-frame-art && /Library/Frameworks/Python.framework/Versions/3.9/bin/python3 /Users/your-username/samsung-frame-art/art.py`
- Make sure it's executable: `chmod +x art.sh`
- Add a cron job with `crontab -e` that runs regularly. I do mine every 12 hours, so it looks like this: `0 */12 * * * /Users/your-username/samsung-frame-art/art.sh`

### Bulk upload mode
This mode uploads _all of the photos_ in the `/images` directory to your TV—which is great if you'd rather just use the TV's internal slideshow mode. Once you've uploaded all of your photos, just go to 'my images' on your TV and choose the shuffle icon. Each time you run this script in bulk mode, as long as you have kept the `uploaded_files.json` intact, it'll check for anything new and sling that to your TV.

*Warning: uploading a lot of images may take a long time.*

To run bulk upload mode: `python3 art.py --upload-all`

### Need images?

1. I originally wanted to do this with the [Google Earth View images](https://earth.google.com/web/data=CiQSIhIgYWJiZTA3ZGNkODM3MTFlNmIzMmFhNWViMDBhYjQ5ZmM), which are lovely and of which there are many thousands of images. I can't distribute those, but you can learn how to [download these here](https://www.gtricks.com/earth/download-all-google-earth-view-wallpapers/)—they work really well with this library.
2. mmargauxx [made an amazing version of this](https://github.com/mmargauxx/frametv) that allows you directly download images from the Rijsmuseum's API, then run the art changer :) 

### Troubleshooting
1. Check if you added the IP address of your TV in `art.py`! 
2. If it doesn't work, check your TV responds by going to your TV's URL in the browser: `http://YOUR_IP_HERE:8001/api/v2/` — if you get a response that's a big messy blob of data, your TV is definitely reachable.
3. If the script locks up it's likely you haven't accepted the permissions request on your TV. If you did accept the permissions, you can check if the script can reach your TV by running:
`python3 art.py --debug` 

If you don't get an error running in debug mode, something else is going on and you should file an issue!

### Caveats

- Because Samsung TVs don't let you check if a file was already uploaded, every time the file is uploaded to the TV the script saves the filename and remote file ID in `uploaded_files.json` — if you run the script again and the file is already on the TV, the script will ensure it's not duplicated repeatedly on the TV.
- Only works with JPG and PNG files
- Needs to be manually run every time you want to upload/change photos. This works great if you can set a cron job to run at the frequency you want the photos changed. 
- Don't blame me if your TV breaks, this was just a project for myself
- I have no idea how many images is the maximum on these TVs. I've used this about 1000 times so far and my 2022 Samsung Frame still seems to accept images.

### To-Do

- This project does not do anything with the aspect ratio of images. It only really handles landscape and does not fit them to the display; I'd like to figure out how to auto-resize or crop these before uploading.
- It would be cool to build a website UI version of this to manage it locally
