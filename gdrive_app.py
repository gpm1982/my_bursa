import streamlit as st
import os

from pydrive.auth import GoogleAuth, ServiceAccountCredentials
from pydrive.drive import GoogleDrive
from apiclient.http import MediaFileUpload

title = 'Google Drive API Test'
st.set_page_config(page_title=title, layout='wide')
st.title(title)

json_dict = {
  "type": "service_account",
  "project_id": st.secrets["GDRIVE_PROJID"],
  "private_key_id": st.secrets["GDRIVE_PKID"],
  "private_key": st.secrets["GDRIVE_PKEY"],
  "client_email": st.secrets["GDRIVE_CLIENT_EMAIL"],
  "client_id": st.secrets["GDRIVE_CLIENT_ID"],
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/my-bursa-streamlit%40tensile-octagon-311403.iam.gserviceaccount.com"
}

gauth = GoogleAuth()
scope = ['https://www.googleapis.com/auth/drive']
gauth.credentials = ServiceAccountCredentials.from_json_keyfile_dict(json_dict, scope)
drive = GoogleDrive(gauth)

# Paginate file lists by specifying number of max results
for file_list in drive.ListFile({'q': 'trashed=false', 'maxResults': 10}):
  st.text('Received %s files from Files.list()' % len(file_list)) # <= 10
  for file1 in file_list:
    st.text('title: %s, id: %s, fileSize: %s' % (file1['title'], file1['id'], file1['fileSize']))