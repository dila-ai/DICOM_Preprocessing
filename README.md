# DICOM_Preprocessing

The codes uploaded to this repository allows for the processing of large number of DICOM images.
You will need to give some inputs to the code that are enclosed in the lines of "#".

1) Organize_DICOM_Files.py allows you to organize an entire folder full of DICOM to the format you desire using metadata tags of each DICOM images.

2) DICOM_White_List.py allows the user to select and limit the metadata included in each DICOM image. You could also take the opportunity to modify or add metadata tags to each DICOM image.

Both codes may require the user to input additional metadata tag names. These tag names must be in keyword format recognized by the pydicom library.
See below for some additional metadata tags that you could use:

'AccessionNumber', 'AcquisitionNumber', 'B1rms', 'BitsAllocated', 'BitsStored', 'CodeValue', 'Columns', 'ContentDate', 'ContentTime', 'DataCollectionDiameter', 'dBdt', 'EchoTime', 'EchoTrainLength', 'FlipAngle', 'FrameOfReferenceUID', 'HighBit', 'ImageOrientationPatient', 'ImagePositionPatient', 'ImageType', 'ImagingFrequency', 'InstanceCreationDate', 'InstanceCreationTime', 'InstanceNumber', 'InversionTime','LargestImagePixelValue', 'LossyImageCompression', 'MagneticFieldStrength', 'Manufacturer', 'Modality', 'NumberOfAverages', 'NumberOfPhaseEncodingSteps', 'NumberOfStudyRelatedInstances', 'NumberOfTemporalPositions','PatientID', 'PatientIdentityRemoved', 'PatientPosition', "PatientAge", "PatientBirthDate", "PatientName", "PatientSex", 'PercentPhaseFieldOfView', 'PercentSampling', 'PhotometricInterpretation', 'PixelBandwidth', 'PixelData', 'PixelPaddingValue', 'PixelRepresentation', 'PixelSpacing', 'PositionReferenceIndicator', 'ReconstructionDiameter', 'RepetitionTime', 'RescaleIntercept', 'RescaleSlope', 'RescaleType', 'RotationDirection', 'Rows', 'SamplesPerPixel', 'SAR', 'ScanOptions', 'SeriesDate', 'SeriesDescription', 'SeriesInstanceUID', 'SeriesNumber', 'SliceLocation', 'SliceThickness', 'SmallestImagePixelValue','SOPClassUID', 'SOPInstanceUID', 'SpacingBetweenSlices', 'SpecificCharacterSet', 'StudyDate', 'StudyDescription', 'StudyID', 'StudyInstanceUID', 'StudyTime', 'TemporalPositionIdentifier', 'WindowCenter', 'WindowWidth'
