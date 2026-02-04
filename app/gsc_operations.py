import os
from google.cloud import storage

base_path = os.path.dirname(os.path.abspath(__file__))
key_path = os.path.normpath(os.path.join(base_path, '../keys/ServiceKey_GoogleCloud.json'))
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = key_path

storage_client = storage.Client()

bucket_name = "bucket_dicom-fastapi-server"

# Upload Files
def upload_to_bucket(blob_name, file_path, bucket_name):
    try:
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(blob_name)
        blob.upload_from_filename(file_path)
        return True
    except Exception as e:
        print(e)
        return False

# upload_to_bucket("testFolder/testBlob", "/home/ksgre/repos/dicom-fastapi-server/imgdisplay_testcases/cplx_p01.dcm", "bucket_dicom-fastapi-server")

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
    
download_from_bucket("testBlob", os.path.join(os.getcwd(), 'test.dcm'), "bucket_dicom-fastapi-server")