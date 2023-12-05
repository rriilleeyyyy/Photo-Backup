#!/usr/bin/python3
"""
  !! IMPORTANT !!
  !! READ THIS !!

  In order to run this script you need python3 and pip3 installed.
  You also need some additional python modules. Please run
    sudo pip3 install httplib2 oauth2client
    sudo pip3 install --upgrade google-api-python-client

  To authenticate in Goolge follow the instructions at
  https://developers.google.com/drive/v3/web/quickstart/python
  A client_secret.json file needs to placed in the same directory
  with this script. The link above contains the instruction on
  how to obtain this file. Once you complete these steps run
    python3 this_script.py --noauth_local_webserver
  and follow the instructions

  On subsequent runs you can execute
    python3 this_script.py | column -t -x -s '|'
  for nicer formating
  Most of the code is copy-pasted from Google's
  official docs, I only made minor modifications.
"""
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

try:
    import argparse

    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/drive-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/drive.metadata.readonly'
CLIENT_SECRET_FILE = 'credentials.json'
APPLICATION_NAME = 'Drive API Python Quickstart'


def get_credentials():
    """Gets valid user credentials from storage.
    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.
    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'drive-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else:  # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials


def main():
    """
    Creates a Google Drive API service object and outputs the names and IDs
    for up to 1000 files.
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('drive', 'v3', http=http)

    results = service.files().list(
        pageSize=10, fields="nextPageToken, files(name, md5Checksum, size)").execute()
    items = results.get('files', [])
    if not items:
        print('No files found.')
    else:
        print('Files:')
        for item in items:
            # uncomment the line below to list only the files which have a checksum assigned
            # if 'md5Checksum' in item:
            name = item['name']
            checksum = item.get('md5Checksum', 'no checksum')
            size = item.get('size', '-')
            print('{1} | {2} bytes | {0}'.format(name, checksum, size))


if __name__ == '__main__':
    main()