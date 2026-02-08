# Given a set of DICOM images, create a folder structure like so:
# study_uid/series_uid/instance_uid/img.dcm

from idc_index.index import IDCClient
from google.cloud import bigquery
import os

idc_client = IDCClient()
base_path = os.path.dirname(os.path.abspath(__file__))
key_path = os.path.normpath(os.path.join(base_path, './keys/ServiceKey_GoogleCloud.json'))
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = key_path

# mr_selection_pd = idc_client.index[idc_client.index['Modality'] == "MR"]
# print(mr_selection_pd[['SeriesInstanceUID', 'sopInstanceUID']][0:10])

# https://github.com/ImagingDataCommons/IDC-Tutorials/blob/master/notebooks/getting_started/part2_searching_basics.ipynb
# 2.25.313341334478452297130753903545138796630

client = bigquery.Client()

query = """
SELECT SOPInstanceUID, Modality, SeriesDescription
FROM `bigquery-public-data.idc_current.dicom_all`
WHERE Modality IN ('CT', 'MR', 'PT', 'CR', 'DX', 'MG', 'US', 'XA', 'NM')
AND SOPClassUID NOT LIKE '%SR%'  -- Exclude Structured Reports
AND SOPClassUID NOT LIKE '%PR%'  -- Exclude Presentation States
AND SOPClassUID NOT LIKE '%RTSTRUCT%'  -- Exclude RT Structure Sets
AND SOPClassUID NOT LIKE '%RTPLAN%'  -- Exclude RT Plans
AND SOPClassUID NOT LIKE '%KO%'  -- Exclude Key Objects
AND NumberOfFrames IS NOT NULL  -- Has frame data
AND gcs_url IS NOT NULL
LIMIT 5
"""
query_job = client.query(query)

for row in query_job:
    print(row.SOPInstanceUID)