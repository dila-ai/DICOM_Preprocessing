"""
White List V3.0 - October 1, 2020
Author: Hui-Ming Lin, DILA.ai at St. Michael's Hospital

THIS SCRIPT IS NOT A REPLACEMENT FOR THE RSNA ANONYMIZER (https://github.com/johnperry/DicomAnonymizerTool).
THIS SCRIPT SHOULD BE RUN ON THE OUTPUT OF RSNA ANONYMIZER.

This script will modify each DICOM file in a folder to a given standardized DICOM metadata tag inclusion list. 

"""

################################################# CHANGE THESE FIELDS ###########################################################

# Provide the source_dir where all the DICOM files are located, and the dest_dir where the white listed DICOM files will be copied to
source_dir = r''
dest_dir = r''

# List all the DICOM tags in keyword format that you wish to include in the output DICOM files. 
DICOM_Tags_List = ['BitsAllocated', 'BitsStored', 'Columns', 'ConvolutionKernel', 'Exposure', 'FrameOfReferenceUID', 
                   'GantryDetectorTilt', 'HighBit', 'ImageOrientationPatient', 'ImagePositionPatient', 'ImageType', 
                   'InstanceNumber', 'KVP', 'Modality', 'PatientID', 'PatientPosition', 'PhotometricInterpretation', 
                   'PixelData', 'PixelRepresentation', 'PixelSpacing', 'RescaleIntercept', 'RescaleSlope', 'RotationDirection', 
                   'Rows', 'SOPClassUID', 'SOPInstanceUID', 'SOPInstanceUID', 'SamplesPerPixel', 'SeriesInstanceUID', 
                   'SeriesNumber', 'SliceThickness', 'SpecificCharacterSet', 'StudyDescription', 'StudyInstanceUID', 
                   'TableHeight', 'WindowCenter', 'WindowWidth', 'XRayTubeCurrent']

# - If you included metadata tag of Date and Time nature, you could choose to leave it as is (date_time_reformat = False), 
#   or set it as blank (date_time_reformat= 'blank').
date_time_reformat = False

# - Use the following to either add metadata fields that was not present in the original DICOM or modify a specific metadata to a value
# - For example, if you want to change the Modality to MR on all DICOM, you would add "modality":"MR".
# - You could also choose to change some metadata tags to reflect the value of a different tag, you can specify this by adding "tag/"
#   prefix before the metadata tag you use to change it to.
# - For example, you could change the Patient ID to the Patient's Name. To do this, you will enter 'PatientID':'tag/PatientName'.

metadata_fields_to_add_or_change = {'PatientIdentityRemoved': 'Yes', 'Modality': 'MR', 'PatientID': 'tag/PatientName'}

#################################################################################################################################

import pydicom, os, tempfile, pandas as pd, shutil
from tqdm import tqdm 
from pydicom.dataset import Dataset, FileDataset
from pydicom.datadict import tag_for_keyword, dictionary_VR
from pydicom.dataelem import DataElement

# Get the paths of all DICOM images in the given source_dir.
print ('Initializing: Getting all DICOM containing folders...')
folders = []
for (dirpath, dirnames, filenames) in os.walk(source_dir):
    # Ensures each image is a DICOM file.
    folders += [dirpath for _file in filenames if _file.endswith('.dcm')]
folders = list(set(folders))


error_log, error_row = pd.DataFrame(columns = ['Path', 'Error_description']), 0


print('White listing DICOM...')
for folder in tqdm(folders):
    # Create the destination folder in the same format as the source_dir.
    destination_folder_path = os.path.join(dest_dir, os.path.relpath(folder, source_dir))
    if not os.path.exists(destination_folder_path):
        os.makedirs(destination_folder_path)
        
    images = os.listdir(folder)
    try:
        for image in images:
            
            # Define the image path and the destination path that the image will be saved to.
            file_path = os.path.join(folder, image)
            destination_path = os.path.join(destination_folder_path, image)
            
            dicom_file = pydicom.dcmread(file_path)
            file_meta = Dataset()
            
            # Needed for Felipe's environment.
            # file_meta.TransferSyntaxUID = dicom_file.file_meta.TransferSyntaxUID.
            file_meta.TransferSyntaxUID = pydicom.uid.ImplicitVRLittleEndian
            
            filename_little_endian = tempfile.NamedTemporaryFile(suffix='.dcm').name
            dicom_novo = FileDataset(filename_little_endian, {}, file_meta=file_meta, preamble=b"\0" * 128)
            
            # Add all the metadata tags listed in DICOM_Tags_List.
            for tag in DICOM_Tags_List:
                # If there is an error in reading the tag, this message will be displayed in CSV.
                error_message = tag + ' tag does not exist'
                if tag in dicom_file:
                    dicom_novo.add(dicom_file[tag])
                    
            # If you have any metadata tags that are date or time, and date_time_reformat is set to 'blank', 
            # these tags will be blank.
            if date_time_reformat == 'blank':
                for tag in DICOM_Tags_List:
                    if tag in dicom_novo:
                        if 'date' in tag.lower() or 'time' in tag.lower():
                            # If there is any problem redefining the date/time tag, this message will be displayed in CSV.
                            error_message = tag + ' date value cannot be changed'
                            dicom_novo[tag].value = ''
            
            for tag_name in metadata_fields_to_add_or_change:
                new_value = metadata_fields_to_add_or_change[tag_name]
                # This error message will be displayed if the metadata field could not be changed.
                error_message = 'error in assigning value to ' + tag_name
                # Grabs the tag value that you wish to use to modify your desired metadata tag, specified with the prefix 'tag/'.
                if 'tag/' in metadata_fields_to_add_or_change[tag_name]:
                    new_value = dicom_file[metadata_fields_to_add_or_change[tag_name][4:]].value
                if tag_name in dicom_novo:
                    dicom_novo[tag_name].value = new_value
                else:
                    # Creating a new tag and adding it if this tag does not currently exist.
                    new_tag = tag_for_keyword(tag_name)
                    new_VR = dictionary_VR(new_tag)
                    data_element = DataElement(new_tag, new_VR, new_value)
                    dicom_novo[new_tag] = data_element
            
            # Save the DICOM file to the appropriate destination location.
            dicom_novo.save_as(destination_path)
                    
    except:
        # Remove the folder that could not be white listed as to mitigate further confusion.
        shutil.rmtree(destination_folder_path)
        
        # Records the image path that caused the error, along with the error itself.
        error_log.loc[error_row] = [str(file_path), str(error_message)]
        error_row += 1
        error_log.to_csv(os.path.join(dest_dir, 'white_list_error.csv'), index=False)

if error_row > 0:
    print('Please check white_list_error.csv')
