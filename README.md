# dicom-fastapi-server

<p>FastAPI backend server to fetch and process DICOM images.</p>

## General Requirements (initial prototype)

<ul>
    <li>Create an API endpoint which will process requests for DICOM images. Adhere to <a href="https://www.dicomstandard.org/using/dicomweb/retrieve-wado-rs-and-wado-uri">WADO-RS specification</a></li>
    <li>Requests will contain study ID, series ID, and instance ID</li>
    <li>Return a .png format</li>
    <li>Use GDCM library to process DICOM images</li>
    <li>Containerize with Docker and deploy using Google Cloud Run</li>
    <li>Images to be stored in Google Cloud Storage</li>
</ul>

## Future Enhancements

<ul>
    <li>Backend will process DICOM image and return pixels to client</li>
    <li>Authenticate client for access to DICOM image data</li>
    <li>Use DCMTK/nanobind libraries for image processing</li>
</ul>

## Links:
<ul>
    <li><a href="https://learn.canceridc.dev/portal/proxy-policy">Imaging Data Commons (IDC) Proxy Policy</a></li>
    <li><a href="https://docs.cloud.google.com/storage/docs/authentication#client-libs">Authenticate to Cloud Storage (see "Client libraries or third-party tools")</a></li>
    <li><a href="https://www.youtube.com/watch?v=pEbL_TT9cHg">Using Google Cloud Storage API in Python</a></li>
</ul>

Compress pixels using HTJ2K: https://jpeg.org/jpeg2000/htj2k.html (GDCM and/or python package (DCMTK) may have capability to do this)
Use process pool
processes cant access memory of another process whereas threads can be accessing the same memory 
processes slower to startup cant communicate
size process pool to number of cores in cpu

next steps:
- pivot to GDCM
- setup orthanc
- figure out how to stream the bytes to the client
- create folders for each SOP instance UID - frames will be individual files inside