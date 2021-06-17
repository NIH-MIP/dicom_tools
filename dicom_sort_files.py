import SimpleITK as sitk
import shutil
import os
from tkinter.filedialog import askdirectory


class convertDicom:
    def __init__(self):
        self.save_location = r'/path/to/wherever'

    def parseData(self):
        #initialize key file
        file_location = askdirectory()
        # if not os.path.isfile(file_location):
        #     raise IOError("File not found: {}".format(file_location))
        print('converting files for ' + file_location)
        save_dir = file_location+'_sorted'
        print('files will be saved in ' +save_dir)
        self.dicom_to_nifti(dcm_dir=file_location,save_dir=save_dir)


    def dicom_to_nifti(self, dcm_dir, save_dir):
        #print(save_dir)
        reader = sitk.ImageSeriesReader()
        for subdir in [x[0] for x in os.walk(dcm_dir)]:
            #print(subdir)
            serieslist = reader.GetGDCMSeriesIDs(subdir)
            if len(serieslist) > 0:
                for series in serieslist:
                    dicom_names = reader.GetGDCMSeriesFileNames(subdir,series)
                    reader.SetFileNames(dicom_names)
                    # image = reader.Execute()
                    print('found ' + str(len(dicom_names)) + ' dicom files in ' + subdir)
                    for file in dicom_names:
                        freader = sitk.ImageFileReader()
                        freader.SetFileName(file)
                        freader.ReadImageInformation()
                        series_name = freader.GetMetaData('0008|103e')
                        series_name = str.replace(series_name, '/', '-')
                        series_name = str.replace(series_name, ' ', '')
                        series_num = freader.GetMetaData('0020|0011')
                        study_date = freader.GetMetaData('0008|0020')
                        modality = freader.GetMetaData('0008|0060')
                        mod_dir = modality + '_' + study_date
                        sub_dir = series_num + '__' + series_name
                        if not os.path.exists(os.path.join(save_dir)):
                            os.mkdir(os.path.join(save_dir))
                        if not os.path.exists(os.path.join(save_dir, mod_dir)):
                            os.mkdir(os.path.join(save_dir, mod_dir))
                        if not os.path.exists(os.path.join(save_dir, mod_dir, sub_dir)):
                            os.mkdir(os.path.join(save_dir, mod_dir, sub_dir))
                        shutil.copyfile(file, os.path.join(save_dir, mod_dir, sub_dir, os.path.split(file)[1]))

if __name__ == '__main__':
    c = convertDicom()
    c.parseData()