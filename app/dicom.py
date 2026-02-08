from pydicom import dcmread, examples
import numpy as np
from io import BytesIO


def get_uint8_pixel_array(dicom_bytes, slice_index = None):
    ds = dcmread(BytesIO(dicom_bytes))
    pixel_array = ds.pixel_array
    pixel_array = np.squeeze(pixel_array)

    if pixel_array.ndim == 3:
        if slice_index is None:
            slice_index = pixel_array.shape[0] // 2
        pixel_array = pixel_array[slice_index, :, :]

    pixel_min = np.min(pixel_array)
    pixel_max = np.max(pixel_array)

    if pixel_min == pixel_max:
        pixel_array = np.zeros_like(pixel_array)
    else:
        pixel_array = (pixel_array - pixel_min) / (pixel_max - pixel_min) * 255
    pixel_array = pixel_array.astype(np.uint8)
    print(f"Shape after processing: {pixel_array.shape}")
    return pixel_array


# https://www.kaggle.com/code/orvile/dicom-to-png