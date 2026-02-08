from typing import Annotated
from fastapi import FastAPI, Path, Query
from fastapi.responses import FileResponse
from . import dicom as dcm
from idc_index.index import IDCClient
from . import gcs_operations as gcs

app = FastAPI()
idc_client = IDCClient()

BUCKET_NAME = "bucket_dicom-fastapi-server"

@app.get("/idc/{sop_instance_uid}")
async def get_png(sop_instance_uid: Annotated[str, Path()], slice_index: Annotated[int | None, Query()] = None):
    # First check if requested instance .png exists in Google Cloud Storage.
    # If it does, return from there
    # If it does not exist in GCS, retrieve from Imaging Data Commons (IDC) Proxy
    # Then, process pixels to .png and upload to both client and GCS
    if not gcs.exists_in_bucket(f"{sop_instance_uid}.png", BUCKET_NAME):
        idc_bucket, idc_blob = gcs.get_idc_location(sop_instance_uid)
        if idc_bucket == None or idc_blob == None:
            return {"url": "SOP Instance UID not found"}
        dicom_bytes = gcs.get_bytes(idc_blob, idc_bucket)
        pixel_array = dcm.get_uint8_pixel_array(dicom_bytes)
        gcs.upload_from_pixel_array(pixel_array, f"{sop_instance_uid}.png", BUCKET_NAME)
    signed_url = gcs.get_signed_url(f"{sop_instance_uid}.png", BUCKET_NAME)
    return {"url": signed_url}