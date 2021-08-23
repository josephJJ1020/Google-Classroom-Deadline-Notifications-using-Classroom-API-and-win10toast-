from __future__ import print_function
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

scopes = ['https://www.googleapis.com/auth/classroom.courses' ]

def get_courses():
    global courseID
    cred=None
    if os.path.exists('token.json'):
        cred=Credentials.from_authorized_user_file('token.json', scopes)
    if not cred or not cred.valid:
        if cred and cred.expired and cred.refresh_token:
            cred.refresh(Request())
        else:
            flow=InstalledAppFlow.from_client_secrets_file('credentials.json',scopes)
            cred=flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(cred.to_json())

    service = build('classroom', 'v1', credentials=cred)
    results = service.courses().list().execute()
    courses = results.get('courses')

    for course in courses:
        print("Course: ", course['name'], "Course ID: ",  course['id'])

if __name__=='__main__':
    get_courses()