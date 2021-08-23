from __future__ import print_function
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import datetime
from win10toast_persist import ToastNotifier

"""
NOTE: Usage of this file is for one subject only. Can be duplicated for multiple subjects.
"""

scopes = ['https://www.googleapis.com/auth/classroom.courses',
          'https://www.googleapis.com/auth/classroom.coursework.me', ]

def get_deadlines():
    now = datetime.date.today() #Date today
    count_subject = 0 #Number of courseworks that have a deadline in selected subject
    courseid = 105521920000 #Example courseId only. Replace with course ID of selected subject from the get_courseID.py file

    #Authentication
    cred=None
    if os.path.exists('../token.json'):
        cred=Credentials.from_authorized_user_file('../token.json', scopes)
    if not cred or not cred.valid:
        if cred and cred.expired and cred.refresh_token:
            cred.refresh(Request())
        else:
            flow=InstalledAppFlow.from_client_secrets_file('../credentials.json', scopes)
            cred=flow.run_local_server(port=0)
        with open('../token.json', 'w') as token:
            token.write(cred.to_json())

    #Building the Classroom API Service
    service = build('classroom', 'v1', credentials=cred)
    results2 = service.courses().courseWork().list(courseId=courseid).execute()
    assignments = results2.get('courseWork', [])
    due_list = []

    #Getting the deadlines
    for assignment in assignments:
        if 'dueDate' in assignment:
            due = datetime.date(assignment['dueDate']['year'], assignment['dueDate']['month'],
                                assignment['dueDate']['day'])
            if due > now: #If deadline is still yet to come,
                count_subject += 1 #Increments count_subject variable by 1
                t = due.strftime('%B %d') #Transforms datetime object into a string with Month-Day format
                due_list.append(t) #Adds the deadline string into a list

    #Show toast notification
    if not count_subject:
        notif = ToastNotifier()
        notif.show_toast(
            title='You have ' + str(count_subject) + ' assignments near the due date for Capstone.',
            msg='You no deadlines near the due date.',
            icon_path='Google_Classroom.ico',
            duration=None )
    #Delete the above condition if you only want upcoming deadlines to pop up

    if count_subject > 1:
        notif1 = ToastNotifier()
        notif1.show_toast(
                    title='You have ' + str(count_subject) + ' assignments near the due date for Capstone.',
                    msg='You have deadlines on ' + ", ".join(due_list) + ".",
                    icon_path='Google_Classroom.ico',
                    duration=None, )
    if count_subject == 1:
        notif2 = ToastNotifier()
        notif2.show_toast(
                    title='You have ' + str(count_subject) + ' assignments near the due date for Capstone.',
                    msg='You have a deadline on ' + ",".join(due_list) + ".",
                    icon_path='Google_Classroom.ico',
                    duration=None)