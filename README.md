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

## Notes for self:
<p>Compress pixels using HTJ2K: https://jpeg.org/jpeg2000/htj2k.html (GDCM and/or python package (DCMTK) may have capability to do this). Window-leveling is adjusting brightness of pixels (since these pixels are 16-bits)</p>
<p>Good example study: 1.2.840.113654.2.55.216102864161139465882876146004265885005</p>

## Next Steps:
<ul>
    <li>pivot to GDCM</li>
    <li>setup orthanc</li>
    <li>figure out how to stream the bytes to the client</li>
    <li>create folders for each SOP instance UID - frames will be individual files inside</li>
    <li>Server side rendering? Hard for browser to window-level. Keep cache of pixels at default level. if user looks to window-level (drags cursor on browser), we pull raw image pixels into RAM on server, do window-level operation and send the pixels back to client. So have an endpoint for a certain image at a certain window-level. Keep objects in RAM (can use Redis) so when user moves cursor again, we can quickly get data. </li>
    <li>TCP-IP - every switch that a packet travels through rechecks the checksum to ensure it's accurate. HTTP3: sits on top of UDP. FastAPI does not support http3 so we put a perimeter server in front of it (sits on the same network). Caddy is a HTTP3 server we could use. (look up video for setting up Caddy with FastAPI and Uvicorn in Docker)</li>
    <li>First start off by using arrow keys to navigate through images. Need an endpoint that gets the metadeta for a study to get the info regarding the instances and series that correspond to it. Have a dropdown for different series in each study, and then list the images below (arrow keys will traverse between images). Use Cine to measure performance (have buttons to start CINE and a report for the fps). The Cine just plays the stack of images like a movie</li>
</ul>