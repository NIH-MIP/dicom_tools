import os
import sys
from datetime import date, datetime
import pydicom
from pydicom.uid import generate_uid
import SimpleITK as sitk
import numpy as np

# Copy over relevant information to a new DICOM Dataset for RTStruct
# dicom names is list containing full path to all DICOMs from original series
# mask arr is numpy array of segmentation mask
def WriteDicom(dicom_names,mask_arr,outputPath):
    if mask_arr.dtype != np.uint16:
        mask_arr=mask_arr.astype("uint16")
    if not os.path.exists(outputPath):
        os.mkdir(outputPath)
    ds_list = [pydicom.read_file(filename) for filename in dicom_names]
    ds_list.sort(key=lambda x: int(x.InstanceNumber))
    # we will set the segmentation series number to "0"
    new_series_num = 0
    # we will set the series description to the following:
    new_series_desc = "WP Segmentation - NVIDIA Clara"
    #generate new series UID
    new_series_uid = generate_uid()
    #we will also reset instance time
    now = datetime.now()
    for ds_slice in ds_list:
        image_slice = mask_arr[int(ds_slice.InstanceNumber)-1, :, :]
        ds_slice.PixelData = image_slice.tobytes()
        ds_slice.SeriesNumber = new_series_num
        ds_slice.SeriesDescription = new_series_desc
        ds_slice.SeriesInstanceUID = new_series_uid
        ds_slice.InstanceCreationDate = now.strftime("%Y%m%d")
        ds_slice.InstanceCreationTime = now.strftime("%H%M%S")
        ds_slice.SOPInstanceUID = generate_uid()
        ds_slice.save_as(os.path.join(outputPath,str(ds_slice.InstanceNumber)+'.dcm'))

    return

def NV_fix(image,niiImg):
    mask = sitk.ReadImage(niiImg)
    img_array = sitk.GetArrayFromImage(image)
    binary_mask = sitk.GetArrayFromImage(mask)
    mask_arr = np.empty(img_array.shape)
    mask_arr += binary_mask
    return mask_arr

def main(argv):
    # example usage: python write_dicom_series /path/to/dicom/folder /path/to/nifti-output.nii.gz /path/to/write/dicom/folder

    if len(argv) < 4:
        print(f"Usage: {argv[0]} refDICOMPath niftiMask outputDICOMPath", file=sys.stderr)
        exit(1)

    refPath = argv[1]
    niiImg = argv[2]
    outputPath = argv[3]

    # read original dicom
    reader = sitk.ImageSeriesReader()
    dicom_names = reader.GetGDCMSeriesFileNames(refPath)
    reader.SetFileNames(dicom_names)
    image = reader.Execute()

    # NVIDIA pipeline does not place output in correct heading format, we need to fix it
    mask_arr = NV_fix(image,niiImg)

    # now we can write the DICOM
    WriteDicom(dicom_names, mask_arr, outputPath)



if __name__ == "__main__":
    main(sys.argv)
