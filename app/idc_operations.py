# Given a set of DICOM images, create a folder structure like so:
# study_uid/series_uid/instance_uid/img.dcm

from collections import defaultdict
from idc_index.index import IDCClient
from google.cloud import bigquery
import os

idc_client = IDCClient()
base_path = os.path.dirname(os.path.abspath(__file__))
key_path = os.path.normpath(os.path.join(base_path, './keys/ServiceKey_GoogleCloud.json'))
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = key_path
client = bigquery.Client()

# Finds all series and instances under a given study
def get_metadata(study_instance_uid: str) -> dict:
    query = f"""
    SELECT 
        SOPInstanceUID, 
        SeriesInstanceUID, 
        SeriesDescription, 
        InstanceNumber
    FROM 
        bigquery-public-data.idc_current.dicom_all
    WHERE 
        StudyInstanceUID = '{study_instance_uid}'
    """
    try:
        query_job = client.query(query)
    except Exception as e:
        return {"error": f"Query failed: {str(e)}"}
    metadata = defaultdict(list)
    for row in query_job:
        metadata[row.SeriesInstanceUID].append(row.SOPInstanceUID)
    print(metadata)
    return metadata
    



if __name__ == "__main__":

    query = """
    WITH ranked AS (
    SELECT SOPInstanceUID, Modality, SeriesDescription, StudyInstanceUID,
           ROW_NUMBER() OVER (PARTITION BY Modality ORDER BY RAND()) as rn
    FROM `bigquery-public-data.idc_current.dicom_all`
    WHERE Modality IN ('CT', 'MR', 'PT', 'CR', 'DX', 'US', 'XA', 'NM')
    AND SOPClassUID NOT LIKE '%SR%'
    AND SOPClassUID NOT LIKE '%PR%'
    AND SOPClassUID NOT LIKE '%RTSTRUCT%'
    AND SOPClassUID NOT LIKE '%RTPLAN%'
    AND SOPClassUID NOT LIKE '%KO%'
    AND NumberOfFrames IS NOT NULL
    AND gcs_url IS NOT NULL
    )
    SELECT SOPInstanceUID, Modality, SeriesDescription, StudyInstanceUID
    FROM ranked
    WHERE rn = 1
    """
    query_job = client.query(query)

    for row in query_job:
        print(row.SOPInstanceUID, row.StudyInstanceUID, row.Modality)

    print("Available columns in IDC Index:")
    print(idc_client.index.columns.tolist())