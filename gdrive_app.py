import os
import json
import streamlit as st

from pydrive.auth import GoogleAuth, ServiceAccountCredentials
from pydrive.drive import GoogleDrive
from apiclient.http import MediaFileUpload

title = 'Google Drive API Test'
st.set_page_config(page_title=title, layout='wide')
st.title(title)

key_dict = json.loads(st.secrets["gdrive_key"])

gauth = GoogleAuth()
scope = ['https://www.googleapis.com/auth/drive']
gauth.credentials = ServiceAccountCredentials.from_json_keyfile_dict(key_dict, scope)
drive = GoogleDrive(gauth)

# Paginate file lists by specifying number of max results
for file_list in drive.ListFile({'q': 'trashed=false', 'maxResults': 10}):
  st.text('Received %s files from Files.list()' % len(file_list)) # <= 10
  for file1 in file_list:
    st.text('title: %s, id: %s, fileSize: %s' % (file1['title'], file1['id'], file1['fileSize']))