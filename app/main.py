from typing import Annotated
from fastapi import FastAPI, Path, Query
from fastapi.responses import Response
from . import dicom as dcm
from idc_index.index import IDCClient
from . import gcs_operations as gcs
import io
from . import idc_operations as idc
import asyncio

app = FastAPI()
idc_client = IDCClient()

BUCKET_NAME = "bucket_dicom-fastapi-server"

@app.get("/idc/{sop_instance_uid}")
async def get_png(sop_instance_uid: Annotated[str, Path()], slice_index: Annotated[int | None, Query()] = None):
    # First check if requested instance .png exists in Google Cloud Storage.
    # If it does, return from there
    # If it does not exist in GCS, retrieve from Imaging Data Commons (IDC) Proxy
    # Then, process pixels to .png and upload to both client and GCS
    loop = asyncio.get_event_loop()
    
    exists = await loop.run_in_executor(None, gcs.exists_in_bucket, f"{sop_instance_uid}.png", BUCKET_NAME)
    
    if not exists:
        idc_bucket, idc_blob = await loop.run_in_executor(None, gcs.get_idc_location, sop_instance_uid)
        if idc_bucket is None:
            return {"url": "SOP Instance UID not found"}
        dicom_bytes = await loop.run_in_executor(None, gcs.get_bytes, idc_blob, idc_bucket)
        pixel_array = await loop.run_in_executor(None, dcm.get_uint8_pixel_array, dicom_bytes, slice_index)
        png_bytes = gcs.pixel_array_to_png_bytes(pixel_array)
        await loop.run_in_executor(None, gcs.upload_png_bytes, png_bytes, f"{sop_instance_uid}.png", BUCKET_NAME)
        return Response(content=png_bytes, media_type="image/png")

    png_bytes = await loop.run_in_executor(None, gcs.get_bytes, f"{sop_instance_uid}.png", BUCKET_NAME)
    return Response(content=png_bytes, media_type="image/png")

@app.get("/api/studies/{study_instance_uid}")
async def get_study_metadata(study_instance_uid: Annotated[str, Path()]):
    metadata = idc.get_metadata(study_instance_uid)
    series_list = []
    for series in metadata.keys():
        instances = []
        for instance in metadata[series]:
            instances.append({
                "id": instance,
                "sopInstanceUid": instance,
                "pngUrl": f"/idc/{instance}"
            })
        series_list.append({
            "id": series,
            "seriesDescription": series,
            "instances": instances
        })
    return {"id": study_instance_uid, "series": series_list}