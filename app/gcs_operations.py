from datetime import timedelta
import os
from google.cloud import storage, bigquery
from PIL import Image
from io import BytesIO

base_path = os.path.dirname(os.path.abspath(__file__))
key_path = os.path.normpath(os.path.join(base_path, './keys/ServiceKey_GoogleCloud.json'))
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = key_path

storage_client = storage.Client()

bucket_name = "bucket_dicom-fastapi-server"

def upload_to_bucket(blob_name, file_path, bucket_name):
    try:
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(blob_name)
        blob.upload_from_filename(file_path)
        return True
    except Exception as e:
        print(e)
        return False

def download_from_bucket(blob_name, file_path, bucket_name):
    try:
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(blob_name)
        with open(file_path, 'wb') as f:
            storage_client.download_blob_to_file(blob, f)
        return True
    except Exception as e:
        print(e)
        return False
    
def transfer_instance_to_bucket(sop_instance_uid, bucket_name):
    bq_client = bigquery.Client()
    query = f"""
        SELECT gcs_url 
        FROM `bigquery-public-data.idc_current.dicom_all` 
        WHERE SOPInstanceUID = '{sop_instance_uid}'
    """
    query_job = bq_client.query(query)
    results = list(query_job.result())
    if not results:
        print("SOPInstanceUID not found.")
        return
    
    gcs_url = results[0].gcs_url
    print(f"Found path: {gcs_url}")

    path_parts = gcs_url.replace("gs://", "").split("/")
    source_bucket_name = path_parts[0]
    source_blob_name = "/".join(path_parts[1:])

    source_bucket = storage_client.bucket(source_bucket_name)
    source_blob = source_bucket.blob(source_blob_name)
    dest_bucket = storage_client.bucket(bucket_name)
    dest_blob_name = f"{sop_instance_uid}.dcm"
    source_bucket.copy_blob(source_blob, dest_bucket, dest_blob_name)
    print(f"Success! Instance {sop_instance_uid} copied to: gs://{bucket_name}/{dest_blob_name}")
    return

def get_idc_location(sop_instance_uid) -> tuple[str | None, str | None]:
    bq_client = bigquery.Client()
    query = f"""
        SELECT gcs_url 
        FROM `bigquery-public-data.idc_current.dicom_all` 
        WHERE SOPInstanceUID = '{sop_instance_uid}'
    """
    query_job = bq_client.query(query)
    results = list(query_job.result())
    if not results:
        print("SOPInstanceUID not found.")
        return (None, None)
    
    gcs_url = results[0].gcs_url
    print(f"Found path: {gcs_url}")

    path_parts = gcs_url.replace("gs://", "").split("/")
    source_bucket_name = path_parts[0]
    source_blob_name = "/".join(path_parts[1:])
    return (source_bucket_name, source_blob_name)

def exists_in_bucket(blob_name, bucket_name) -> bool:
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    return blob.exists()

def get_signed_url(blob_name, bucket_name):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    
    # Generate a URL that's valid for 15 minutes
    url = blob.generate_signed_url(
        version="v4",
        expiration=timedelta(minutes=15),
        method="GET"
    )
    return url

def upload_from_pixel_array(pixel_array, blob_name, bucket_name):
    img = Image.fromarray(pixel_array)
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    blob.upload_from_file(buffer, content_type="image/png")

def get_bytes(blob_name, bucket_name):
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    dicom_bytes = blob.download_as_bytes()
    return dicom_bytes

if __name__ == "__main__":
    #upload_to_bucket("testFolder/testBlob", "/home/ksgre/repos/dicom-fastapi-server/imgdisplay_testcases/cplx_p01.dcm", "bucket_dicom-fastapi-server")
    #download_from_bucket("testBlob", os.path.join(os.getcwd(), 'test.dcm'), "bucket_dicom-fastapi-server")
    # transfer_instance_to_bucket("1.2.826.0.1.3680043.10.511.3.91885874683499094577536681620493114", "bucket_dicom-fastapi-server")
    print(exists_in_bucket("1.2.826.0.1.3680043.10.511.3.91885874683499094577536681620493114.dcm", "bucket_dicom-fastapi-server"))
