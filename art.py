import sys
import logging
import os
import random
import json
import argparse

sys.path.append('../')

from samsungtvws import SamsungTVWS

# Add command line argument parsing
parser = argparse.ArgumentParser(description='Upload images to Samsung TV.')
parser.add_argument('--upload-all', action='store_true', help='Upload all images at once')
parser.add_argument('--debug', action='store_true', help='Enable debug mode to check if TV is reachable')
args = parser.parse_args()

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

# Check if TV is reachable in debug mode
if args.debug:
		try:
				logging.info('Checking if the TV can be reached.')
				info = tv.rest_device_info()
				logging.info('If you do not see an error, your TV could be reached.')
				sys.exit()
		except Exception as e:
				logging.error('Could not reach the TV: ' + str(e))
				sys.exit()

# Checks if the TV supports art mode
art_mode = tv.art().supported()

if art_mode == True:
		# Retrieve information about the currently selected art
		current_art = tv.art().get_current()

		# Get a list of JPG/PNG files in the folder, and searches recursively if you want to use subdirectories
		files = [os.path.join(root, f) for root, dirs, files in os.walk(folder_path) for f in files if f.endswith( ('.jpg', '.jpeg', '.png') )]

		if args.upload_all:
				logging.info('Bulk uploading all photos. This may take a while...')

				# Remove the filenames of images that have already been uploaded
				files = list(set(files) - set([f['file'] for f in uploaded_files]))
				files_to_upload = files
				
		else:
				if len(files) == 0:
						logging.info('No new images to upload.')
				else:
						logging.info('Choosing random image.')
						files_to_upload = [random.choice(files)]

		for file in files_to_upload:
				# Read the contents of the file
				with open(file, 'rb') as f:
						data = f.read()

				# Upload the file to the TV and select it as the current art, or select it using the remote filename if it has already been uploaded
				remote_filename = None
				for uploaded_file in uploaded_files:
						if uploaded_file['file'] == file:
								remote_filename = uploaded_file['remote_filename']
								logging.info('Image already uploaded.')
								break
				
				if remote_filename is None:
						logging.info('Uploading new image: ' + str(file))

						try:
							if file.endswith(('.jpg','.jpeg')):
									remote_filename = tv.art().upload(data, file_type='JPEG', matte="none")
							elif file.endswith('.png'):
									remote_filename = tv.art().upload(data, file_type='PNG', matte="none")
						except Exception as e:
							logging.error('There was an error: ' + str(e))
							sys.exit()
						
						# If upload is successful 
						if remote_filename: 
							# Add the filename to the list of uploaded filenames
							uploaded_files.append({'file': file, 'remote_filename': remote_filename})

						if not args.upload_all:
							# Select the uploaded image using the remote file name
							tv.art().select_image(remote_filename, show=False)

				else:
						if not args.upload_all:
								# Select the image using the remote file name only if not in 'upload-all' mode
								logging.info('Setting existing image, skipping upload')
								tv.art().select_image(remote_filename, show=True)

				# Save the list of uploaded filenames to the file
				with open(upload_list_path, 'w') as f:
						json.dump(uploaded_files, f)
else:
		logging.warning('Your TV does not support art mode.')
