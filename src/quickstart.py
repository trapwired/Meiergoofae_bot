from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']


def getCalendarEntries():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    result = 'Don\'t forget: \n'
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    # print('Getting the upcoming 10 events')
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                        maxResults=10, singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])
    # print(events)
    

    if not events:
        result += 'No upcoming events found.'
    
    events_today = list()
    events_tomorrow = list()
    events_2days = list()

    for event in events:
        start_str = event['start'].get('dateTime', event['start'].get('date'))
        whole_day = False
        if len(start_str) < 11:
            # event takes whole day
            format = '%Y-%m-%d'
            start :datetime.datetime = datetime.datetime.strptime(start_str, format)
            whole_day = True
        else:
            format = '%Y-%m-%dT%H:%M:%S+01:00'
            start :datetime.datetime = datetime.datetime.strptime(start_str, format)
        now_time = datetime.datetime.now()
        difference = start - now_time
        if start.day == now_time.day:
            if not whole_day:
                events_today.append(f"{start.hour}:{str(start.minute).zfill(2)} {event['summary']}")
        if start.day == now_time.day+1:
            if whole_day:
                events_tomorrow.append(f"{event['summary']}")
            else:    
                events_tomorrow.append(f"{start.hour}:{str(start.minute).zfill(2)} {event['summary']}")
        if start.day == now_time.day+2:
            if whole_day:
                events_2days.append(f"{event['summary']}")
            else:    
                events_2days.append(f"{start.hour}:{str(start.minute).zfill(2)} {event['summary']}")
        # result += start + ' ' + event['summary'] + '\n'
    if events_today:
        result += '--Today--\n'
        result += '\n\t'.join(events_today)
        result += '\n'
    if events_tomorrow:
        result += '--Tomorrow:--\n'
        result += '\n\t'.join(events_tomorrow)
        result += '\n'
    if events_2days:
        result += '--Day after Tomorrow:--\n'
        result += '\n\t'.join(events_2days)
    # print(result)
    if not events_today and not events_tomorrow and not events_2days:
        return ''
    return result

if __name__ == '__main__':
    # main()
    getCalendarEntries()
