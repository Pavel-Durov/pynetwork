"""
Google Api wrapper, handles authentication (based on client_secret.json) and file management
"""

import os
import sys
import shelve
import httplib2 
import fsutil
import logging
from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from apiclient.http import MediaFileUpload

class GoogleDriveApi:
    """Google Api wrapper class"""

    #Allows access to the Application Data folder
    APP_FOLDER_SCOPE = 'https://www.googleapis.com/auth/drive.appfolder'
    #Full, permissive scope to access all of a user's files, excluding the Application Data folder.
    GOD_MODE_DRIVE_SCOPE = 'https://www.googleapis.com/auth/drive'

    CLIENT_SECRET_FILE = 'secrets/client.secret.json'
    APPLICATION_NAME = 'pyNetCheck'
    CREDENTIAL_JSON = APPLICATION_NAME + ".json"

    APPLICATION_ROOT_FOLDER_ID = None
    APPLICATION_ROOT_FOLDER_ID_KEY = "APPLICATION_ROOT_FOLDER_ID"
    SHELVE_FILE = ".cache"

    #mime types
    PLAIN_TEXT_MIME = 'text/plain'
    HTML_MIME = 'text/html'
    JSON_MIME = 'application/json'
    DIR_MIME = 'application/vnd.google-apps.folder'

    def __init__(self):
        """Initialize GoogleDriveApi class, manages authentication and file management"""
        credentials = self.__get_credentials()
        http = credentials.authorize(httplib2.Http())
        self.__drive_service = discovery.build('drive', 'v3', http=http)

        shelve_path = os.path.dirname(os.path.abspath(__file__)) + self.SHELVE_FILE
        self.__shelve = shelve.open(shelve_path)
        self.__recheck_root_dir()

    def __recheck_root_dir(self):
        key_list = self.__shelve.keys()
        if not self.APPLICATION_ROOT_FOLDER_ID_KEY in key_list:
            self.__create_root_folder()
        else:
            self.APPLICATION_ROOT_FOLDER_ID = self.__shelve[self.APPLICATION_ROOT_FOLDER_ID_KEY]

    def __create_root_folder(self):
        file_metadata = {
            'name' : self.APPLICATION_NAME,
            'mimeType' : self.DIR_MIME
        }
        files = self.__drive_service.files()
        file = files.create(body=file_metadata,fields='id').execute()
        self.__shelve[self.APPLICATION_ROOT_FOLDER_ID_KEY] = file.get('id')

    def __get_credentials(self):
        home_dir = os.path.expanduser('~')
        credential_dir = os.path.join(home_dir, '.credentials')
        if not os.path.exists(credential_dir):
            os.makedirs(credential_dir)
        credential_path = os.path.join(credential_dir, self.CREDENTIAL_JSON)
        store = Storage(credential_path)
        credentials = store.get()

        if not credentials or credentials.invalid:
            flow = client.flow_from_clientsecrets(self.CLIENT_SECRET_FILE, self.GOD_MODE_DRIVE_SCOPE)
            flow.user_agent = self.APPLICATION_NAME
            credentials = tools.run_flow(flow, store)

            logging.getLogger("PYNETWORK").info('Storing credentials to ' + credential_path)

        return credentials

    def upload_html_file(self, cloud_file_name, file_path):
        """Uploads html file to Google Drive"""
        self.__upload_file(cloud_file_name, file_path, self.HTML_MIME)

    def upload_json_file(self, cloud_file_name, file_path):
        """Uploads json file to Google Drive"""
        self.__upload_file(cloud_file_name, file_path, self.JSON_MIME)

    def __upload_file(self, cloud_file_name, file_path, file_mime):
        file_metadata = {
            'name' : cloud_file_name,
            'parents': [self.APPLICATION_ROOT_FOLDER_ID]
        }

        media = MediaFileUpload(file_path, mimetype=file_mime, resumable=True)
        file = self.__drive_service.files().create(body=file_metadata,
                                            media_body=media,
                                            fields='id').execute()

        logging.getLogger("PYNETWORK").info('File uploaded file ID: %s' % file.get('id'))

if __name__ == "__main__":
    GoogleDriveApi()