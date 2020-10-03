"""
Organize_DICOM_files V2.0 - October 1, 2020
Author: Hui-Ming Lin, DILA.ai at St. Michael's Hospital

This script will take a folder containing DICOM images and organize them based on each image's metadata.
It will create a copy of each DICOM image to preserve your original files in case any problem occurs.
      
"""

################################################# CHANGE THESE FIELDS ###########################################################

# Provide the path to the source directory containing all the DICOM images to be organized,
# and the destination directory where the organized DICOM images will be stored.
source_folder = r''
destination_folder = r''

# Give the metadata tags in the order you wish the DICOM to be organized.
# For example, if you want your path to be "Patient ID/Series Description/image", then put ['PatientID', 'SeriesDescription'].
path_structure = ['StudyInstanceUID', 'SeriesInstanceUID']

# If you wish to change the DICOM image filename, you can specify the metadata tag you wish to change it to.
# For example, if you want to rename the filename to the instance number, set filename_change = 'InstanceNumber'.
# Please ensure that the chosen metadata tag for this field is unique for every image in the path_structure you specified.
# If you wish to keep the filename as is, set filename_change = False. 
filename_change = False

#################################################################################################################################

import pydicom as dicom, os, shutil, pandas as pd, re
from tqdm import tqdm

# Get the paths of all DICOM images in the given source_file.
print ('Initializing: Getting DICOM image paths...')
images = []
for (dirpath, dirnames, filenames) in os.walk(source_folder):
    # Ensures each image is a DICOM file.
    images += [os.path.join(dirpath, _file) for _file in filenames if _file.endswith('.dcm')]

error, error_row = pd.DataFrame(columns = ['image_path', 'error_message']), 0

print ('Organizing images...')
for image in tqdm(images):
    des_path = destination_folder
    filename = os.path.basename(image)
    dicom_file = dicom.read_file(image)

    try:
        for item in path_structure:
            # If the tag does not exist, this will be the error written to the CSV.
            error_message = 'tag ' + str(item) + ' does not exist'
            
            tag_value = str(dicom_file.data_element(item).value)
            
            # Strips any special characters to ensure the path name does not contain forbidden characters
            # your operating system may not accept.
            tag_value = re.sub('[^0-9a-zA-Z._]', '_', tag_value)
            
            # Ensures your metadata tag is not an empty string.
            if tag_value == '':
                error_message = 'tag ' + str(item) + ' is either not found or is blank'
                raise AssertionError
            
            des_path = os.path.join(des_path, tag_value)
        
        if not os.path.exists(des_path):
            os.makedirs(des_path)
        
        # If you chose to rename your filename, the name will be replaced by the specified metadata tag.
        if filename_change:
            filename = str(dicom_file.data_element(filename_change).value) + '.dcm'
        
        # Ensures that the file you are now saving does not already exist (such as when
        # two DICOM files in a case contains the same Instance Number).
        if os.path.exists(os.path.join(des_path, filename)):
            error_message = str(os.path.join(des_path, filename)) + ' already exists'
            raise AssertionError
        
        # Copies the DICOM image to the appropriate destination path.
        shutil.copyfile(image, os.path.join(des_path, filename))
    except:
        # If any metadata tag either does not exist or is empty, the metadata_error folder will be created
        # and the DICOM image will be copied to "metadata_errors" folder for your convenience. 
        parent_folder = os.path.dirname(destination_folder)
        if not os.path.exists(os.path.join(parent_folder, 'metadata_errors')):
            os.makedirs(os.path.join(parent_folder, 'metadata_errors'))
        shutil.copyfile(image, os.path.join(parent_folder, 'metadata_errors', filename))
        
        # Write to a CSV file the image path and the issue so you could investigate.
        error.loc[error_row] = [str(image), str(error_message)]
        error_row += 1
        error.to_csv(os.path.join(parent_folder, 'error_log.csv'), index=False)

if error_row > 0:
    print('Please check error file!')
