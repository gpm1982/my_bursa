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
  "project_id": "tensile-octagon-311403",
  "private_key_id": "3fe16d4a1ba4969677ad67e1ca13509ba8125064",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQC/V9blcMrSPimc\noPSAHd2p3VUeWe/diB+Ay+za3kia4aeLDBP1+/G8qBxnM4GHUDYRNpdlyHDaKg7m\nH4olyhWZjEprnz2fOmTvYCCesbtTpOTLdW9jiu23IBnCENcRLeiqfp5NGd+13llY\nMppK/KRa/IoskQJnLsDFoDv8GqZNObQMFa3UbjOJHm/QiRWaI0dzjNmpPCSWR6KF\nMjQiHgMTht1JOx2sZzCDWNBhtGTzPxQKToNaW4/Thb28AhbLhrDjoM3bCJFwbhaE\nbC84/xkwy2wBJkyUQovrJUsDkJFmCWjWdMgtgjVTc+jk7kBu8PXPhnBoZThi0Ixf\nvoaGx3EzAgMBAAECggEAT9piOi24z0YXCqFXeJI+PFI84CZLhun0r8UrK2pB5bVP\nvSVEvU8wYvnLpLwnjeeJMOTWCSm+AyYzQpGeD0hHfGXCdyilSGrPzeCRrHjjAzTZ\nMRno6yODMn4IkeeCQc6lf2XJPccTCCzrn3W605mdI8WqCpBX7uThmXhWIE+k4Kv/\n3cWH4nG0nszRex67iAoKg1USJf+ZjeXXk5Dw/TooefQn0nHsMnLX6YPb3A3XYZfY\n5G5WAPY+UljoN9SpHdcvqRG3lF2pmHgOMxHMijRMGvcerNoO//92TwZWmvNtur5q\n/5n/h6oJWZuAN6PikJlLU1j3TfoKzNPo+jD6DMrd+QKBgQDlx0c5NkU8DzLsjXDg\nvKxHie7E0ZoJYNSEkVJL/JZf0hZkhzISPNlWXoiiTt0KzJNHlxOr4/swAAx6rk75\nulYQI41Ph8XjPp+DJXlWiI71bat4APq1s4BW82J6UgfEpPz2C5tC6fil1MNaQThe\nrAv88r1s6nx7Jv+h4zGOlBbq+QKBgQDVLbdkHv/OPHQec3g3DFDF5VzUGnhxzXh+\nmsbgsvxazb5/ocTqsOtLR3YXZStwJvy4bmN7t8NPsEmSfnvbgCGC9bSMlZoJlrvw\nObD15tNhb/MxQd2hq2Nt+sOg2Obw1c7DjzZvkN05euQTfS3ewvdH646ktpg2delW\nhLaGSr+8iwKBgQCafugLtsrMfCewV9W6tgFcRIjve0MH5TxfOlrMTrRJDzgRNbnb\n+1/iq8NQ5pfHKBArBZCrdamx94ZsgoEFdl1hkpX0EIVkqvmTs4GnRkBhEvFEydvI\nij3TuOfQ+RDSDmErilhFoI2X6rvDFrExLpsM46Wr8unp4CnnjpwGktnp+QKBgAUu\nhEupuTwRGh13Xw+ve/MjfRsmvZC+ltQ0/OqPTzUB1USS8Q9nV4DP7t3otqKWQARX\nopFqSRQRy+gErQwL1ESzpjzYkhLzmAPh0xxXDQJMT1P+Lt30JYmR09mADDUEbW8x\ndvhFRCtWgl665zeH86zK2//C9HY2bYKN3UXsYTa7AoGANubrVBRBGoY9QpfMPiNv\nTLkK12VIDcsAwjWNQk33aGNQJe/ozKMuT8g+pI9VmRGd99dZ10XXNc5vaANnik2g\nOOEzTRB6ZT9UCw34FhsVs5IsXGdpfKTmj6TmCF3GUWGMD34FtDYfCD+w94vauPvN\nNo01s5aDwNrJdkgOTPPc7AY=\n-----END PRIVATE KEY-----\n",
  "client_email": "my-bursa-streamlit@tensile-octagon-311403.iam.gserviceaccount.com",
  "client_id": "115823248792858730320",
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