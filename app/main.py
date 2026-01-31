from typing import Annotated
from fastapi import FastAPI, Path, Query
from fastapi.responses import FileResponse
from .dicom import Dicom

app = FastAPI()

@app.get("/dicom/metadata/{filename}")
async def get_metadata(filename: Annotated[str, Path()]):
    dcm = Dicom("./imgdisplay_testcases/" + filename)
    studyUID, seriesUID, instanceUID = dcm.get_UIDS()
    return {"Study UID:": studyUID,
            "Series UID": seriesUID,
            "Instance UID": instanceUID}