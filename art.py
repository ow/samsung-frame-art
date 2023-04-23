import sys
import logging
import os
import random
import json

sys.path.append('../')

from samsungtvws import SamsungTVWS

# Set the path to the folder containing the images
folder_path = './images/'

# Set the path to the file that will store the list of uploaded filenames
upload_list_path = './uploaded_files.json'

# Load the list of uploaded filenames from the file
if os.path.isfile(upload_list_path):
		with open(upload_list_path, 'r') as f:
				uploaded_files = json.load(f)
else:
		uploaded_files = []

# Increase debug level
logging.basicConfig(level=logging.INFO)

# Set your TVs local IP address. Highly recommend using a static IP address for your TV.
tv = SamsungTVWS('192.168.0.9')

# Checks if the TV supports art mode
art_mode = tv.art().supported()

if art_mode == True:
	# Retrieve information about the currently selected art
	info = tv.art().get_current()
	logging.info(info)

	# Get a list of JPEG files in the folder
	files = [f for f in os.listdir(folder_path) if f.endswith('.jpg') or f.endswith('.png')]

	# Remove the filenames of images that have already been uploaded
	files = list(set(files) - set([f['file'] for f in uploaded_files]))

	if len(files) == 0:
			logging.warning('No new images to upload.')
	else:
			# Select a random file from the list of JPEG files
			file = random.choice(files)
			
			#Test the image is not uploaded again by hard-coding image name
			#file = '0x342fad2ec1f71e948ded12832727175ce05cc0faf5999fa6dfa6e0e156fb1c93.png'

			# Read the contents of the file
			with open(os.path.join(folder_path, file), 'rb') as f:
					data = f.read()

			# Upload the file to the TV and select it as the current art, or select it using the remote filename if it has already been uploaded
			remote_filename = None
			for uploaded_file in uploaded_files:
					if uploaded_file['file'] == file:
							remote_filename = uploaded_file['remote_filename']
							logging.warning('Image already uploaded.')
							break
			if remote_filename is None:
					logging.warning('Uploading new image')

					if file.endswith('.jpg'):
						remote_filename = tv.art().upload(data, file_type='JPEG', matte="none")
					elif file.endswith('.png'):
						remote_filename = tv.art().upload(data, file_type='PNG', matte="none")

					# Select the uploaded image using the remote file name
					tv.art().select_image(remote_filename, show=True)

					# Add the filename to the list of uploaded filenames
					uploaded_files.append({'file': file, 'remote_filename': remote_filename})
			else:
					logging.warning('Setting existing image')
					# Select the existing image using the saved remote file name from the TV
					tv.art().select_image(remote_filename, show=True)

			# Save the list of uploaded filenames to the file
			with open(upload_list_path, 'w') as f:
					json.dump(uploaded_files, f)
else:
	logging.warning('Your TV does not support art mode.')
