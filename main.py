import datetime
from apiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
import pickle
from datetime import timedelta

scopes = ['https://www.googleapis.com/auth/calendar']
# flow = InstalledAppFlow.from_client_secrets_file('client_secret.json', scopes=scopes)
# credential = flow.run_console()
# pickle.dump(credential, open('token.pkl', 'wb'))
credentials = pickle.load(open('token.pkl', 'rb'))
service = build('calendar', 'v3', credentials=credentials)
#result = service.calendarList().list().execute()
#print(result)
now = datetime.datetime.utcnow().isoformat() + 'Z'# Получение текущего времени

events_result = service.events().list(calendarId='oc3elh5mfajsut5ni69u25v99o@group.calendar.google.com',
                                      timeMin=now,
                                      maxResults=10,
                                      singleEvents=True,
                                      orderBy='startTime').execute()
events = events_result.get('items', [])
print(events)
for i in events:
    print("Name: ", i['summary'])
    print("Time start: ", i['start']['dateTime'])
    print("Time end: ", i['end']['dateTime'])