# DICOM_Preprocessing

The scripts uploaded to this repository allow for the processing of a large number of DICOM files.

Organize_DICOM_Files.py allows you to organize a folder of DICOM images to the desired format using information stored in DICOM metadata.

DICOM_White_List.py allows the user to select and limit the metadata included in each DICOM image. You could also take the opportunity to modify or add metadata tags to each DICOM image.

Both scripts may require the user to input additional metadata tag names. These tag names must be in keyword format recognized by the pydicom library.

See below for some additional metadata tags that you could use:

'AccessionNumber', 'AcquisitionNumber', 'B1rms', 'BitsAllocated', 'BitsStored', 'CodeValue', 'Columns', 'ContentDate', 'ContentTime', 'DataCollectionDiameter', 'dBdt', 'EchoTime', 'EchoTrainLength', 'FlipAngle', 'FrameOfReferenceUID', 'HighBit', 'ImageOrientationPatient', 'ImagePositionPatient', 'ImageType', 'ImagingFrequency', 'InstanceCreationDate', 'InstanceCreationTime', 'InstanceNumber', 'InversionTime','LargestImagePixelValue', 'LossyImageCompression', 'MagneticFieldStrength', 'Manufacturer', 'Modality', 'NumberOfAverages', 'NumberOfPhaseEncodingSteps', 'NumberOfStudyRelatedInstances', 'NumberOfTemporalPositions','PatientID', 'PatientIdentityRemoved', 'PatientPosition', "PatientAge", "PatientBirthDate", "PatientName", "PatientSex", 'PercentPhaseFieldOfView', 'PercentSampling', 'PhotometricInterpretation', 'PixelBandwidth', 'PixelData', 'PixelPaddingValue', 'PixelRepresentation', 'PixelSpacing', 'PositionReferenceIndicator', 'ReconstructionDiameter', 'RepetitionTime', 'RescaleIntercept', 'RescaleSlope', 'RescaleType', 'RotationDirection', 'Rows', 'SamplesPerPixel', 'SAR', 'ScanOptions', 'SeriesDate', 'SeriesDescription', 'SeriesInstanceUID', 'SeriesNumber', 'SliceLocation', 'SliceThickness', 'SmallestImagePixelValue','SOPClassUID', 'SOPInstanceUID', 'SpacingBetweenSlices', 'SpecificCharacterSet', 'StudyDate', 'StudyDescription', 'StudyID', 'StudyInstanceUID', 'StudyTime', 'TemporalPositionIdentifier', 'WindowCenter', 'WindowWidth'
