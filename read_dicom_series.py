import os
import sys
from datetime import date, datetime
import pydicom
from pydicom.uid import generate_uid
import SimpleITK as sitk
import numpy as np



def main(argv):
    # example usage: python read_dicom_series /path/to/dicom/folder /path/to/nifti-output.nii.gz

    if len(argv) < 3:
        print(f"Usage: {argv[0]} refDICOMPath outputPathName", file=sys.stderr)
        exit(1)

    refPath = argv[1]
    niiImg = argv[2]

    # read original dicom
    reader = sitk.ImageSeriesReader()
    dicom_names = reader.GetGDCMSeriesFileNames(refPath)
    reader.SetFileNames(dicom_names)
    image = reader.Execute()
    sitk.WriteImage(image,niiImg)



if __name__ == "__main__":
    main(sys.argv)
