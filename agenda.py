#!/usr/bin/env python3
import httplib2
import os

import datetime
import argparse
import json

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage


# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/calendar-python-quickstart.json
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Calendar API Python Quickstart'
SCOPES = ['https://www.googleapis.com/auth/calendar', 'https://www.googleapis.com/auth/calendar.readonly']

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
                                   'calendar-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if parser:
            credentials = tools.run_flow(flow, store, parser)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def swiss_format_from_datetime(date, sep='à'):
    return datetime.datetime.strptime(date, '%Y-%m-%dT%H:%M:%S').strftime('%a %d %b %Y {} %H:%M'.format(sep))


def main(nb):
    """Shows basic usage of the Google Calendar API.

    Creates a Google Calendar API service object and outputs a list of the next
    10 events on the user's calendar.
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)

    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    print('Getting the upcoming 10 events')
    eventsResult = service.events().list(
        calendarId='primary', timeMin=now, maxResults=10, singleEvents=True,
        orderBy='startTime').execute()
    events = eventsResult.get('items', [])

    today_event = False
    if not events:
        print('No upcoming events found.')
    for event in events:
        date = ""
        start, is_datetime = (event['start']['dateTime'], True) if 'dateTime' in event['start'].keys() else (event['start']['date'], False)
        if is_datetime:
            date = start.split('+')[0]
            date = swiss_format_from_datetime(date, 'de')
            date += ' à ' + swiss_format_from_datetime(event['end']['dateTime'].split('+')[0])[-5:]

            if start.split('T')[0]  ==  str(datetime.date.today()) and not today_event:
                today_event = True 
                print("*********************************************")
                print("Aujourd'hui:")
            elif start.split('T')[0]  !=  str(datetime.date.today()) and today_event:
                print("*********************************************")
                today_event = False
            else:
                print("---------------------------------------------")

            print(date) 
            print("  * " + event['summary'])

def make_reservation(summary, date, start_time, end_time):
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)

    start = datetime.datetime.strptime(date + " " + start_time, '%d.%m.%Y %H:%M').isoformat()
    end = datetime.datetime.strptime(date + " " + end_time, '%d.%m.%Y %H:%M').isoformat()

    #start = datetime.datetime(2015, 10, 4, 12, 00, 00).isoformat()
    #end = datetime.datetime(2015, 10, 4, 15, 00, 00).isoformat()
    event = {'summary': summary, 'start': {'dateTime': start, 'timeZone': 'Europe/Zurich'}, 'end': {'dateTime': end, 'timeZone': 'Europe/Zurich'}}
    print(event)
    event = service.events().insert(calendarId='jcavat@gmail.com', body=event).execute()
    print(event['status'])

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Affiche mon agenda')
    parser.add_argument('nb_events', metavar='N', type=int, nargs='?', default=20,
                       help="Nombre d'événements à afficher")
    parser.add_argument('-a', nargs=4, help='Insérer un événemets (Exemple: -a "mon événement" 10.10.2015 12:00 13:00)')

    args = parser.parse_args()
    print(args)
    if vars(args)['a'] is not None:
        make_reservation(*vars(args)['a'])
    else:
        main(vars(args)['nb_events'])
