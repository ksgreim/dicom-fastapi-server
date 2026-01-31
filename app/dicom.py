from pydicom import dcmread, examples
import numpy as np
from PIL import Image

class Dicom:

    def __init__(self, filepath: str):
        self.ds = dcmread(filepath)
        
    def get_UIDS(self):
        study_uid = self.ds.StudyInstanceUID
        series_uid = self.ds.SeriesInstanceUID
        instance_uid = self.ds.SOPInstanceUID
        return (study_uid, series_uid, instance_uid)


if __name__ == "__main__":
    path = "imgdisplay_testcases/mlut_18.dcm"
    ds = dcmread(path)
    name = ds.PatientName
    study_date = ds.StudyDate
    modality = ds.Modality

    #print(f"Patient's Name: {name}\nStudy Date: {study_date}\nModality: {modality}")
    print(f"Study UID: {ds.StudyInstanceUID}\nSeries UID: {ds.SeriesInstanceUID}\nInstance UID: {ds.SOPInstanceUID}")
    pixel_array = ds.pixel_array
    pixel_min = np.min(pixel_array)
    pixel_max = np.max(pixel_array)
    if pixel_min == pixel_max:
        pixel_array = np.zeros_like(pixel_array)
    else:
        pixel_array = (pixel_array - pixel_min) / (pixel_max - pixel_min) * 255
    pixel_array = pixel_array.astype(np.uint8)

    image = Image.fromarray(pixel_array)
    # image.save("/home/ksgre/repos/dicom-fastapi-server/images/test.png")

# https://www.kaggle.com/code/orvile/dicom-to-png