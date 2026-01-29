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