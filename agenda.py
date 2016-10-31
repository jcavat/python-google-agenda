#!/usr/bin/env python3
import httplib2
import os

from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools
import locale
import datetime
import argparse
from oauth2client.client import SignedJwtAssertionCredentials
import json

SCOPES = ['https://www.googleapis.com/auth/calendar.readonly','https://www.googleapis.com/auth/calendar']
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Calendar API Python Quickstart'


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

    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatability with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def swiss_format_from_datetime(date, sep='à'):
    return datetime.datetime.strptime(date, '%Y-%m-%dT%H:%M:%S').strftime('%a %d %b %Y {} %H:%M'.format(sep))

def main(nb):
    """Shows basic usage of the Google Calendar API.

    Creates a Google Calendar API service object and outputs a list of the next
    events on the user's calendar.
    """


    nb_events = nb

    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())


    service = discovery.build('calendar', 'v3', http=http)

    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    print('Les {} prochains événements'.format(nb_events))
    eventsResult = service.events().list(
        calendarId='primary', timeMin=now, maxResults=nb_events, singleEvents=True,
        orderBy='startTime').execute()
    events = eventsResult.get('items', [])

    if not events:
        print('Aucun événement')

    locale.setlocale(locale.LC_ALL, '')

    today_event = False
    for event in events:

        start, is_datetime = (event['start']['dateTime'], True) if 'dateTime' in event['start'].keys() else (event['start']['date'], False)
        date = ""
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

    def get_auth_service():
        client_email = '1059111794351-aj0au7hbk0gb07iv9f388s1memppmgnp@developer.gserviceaccount.com'
        with open("keys.json") as f:
            private_key = bytes(json.load(f)['private_key'], 'utf-8')

        credentials_verify = SignedJwtAssertionCredentials(client_email, private_key,
            scope=['https://www.googleapis.com/auth/calendar', 'https://www.googleapis.com/auth/calendar.readonly'])
        http_sv = credentials_verify.authorize(httplib2.Http())
        return discovery.build('calendar', 'v3', http=http_sv)

    service = get_auth_service()

    start = datetime.datetime.strptime(date + " " + start_time, '%d.%m.%Y %H:%M').isoformat()
    end = datetime.datetime.strptime(date + " " + end_time, '%d.%m.%Y %H:%M').isoformat()

    #start = datetime.datetime(2015, 10, 4, 12, 00, 00).isoformat()
    #end = datetime.datetime(2015, 10, 4, 15, 00, 00).isoformat()
    event = {'summary': summary, 'start': {'dateTime': start, 'timeZone': 'Europe/Zurich'}, 'end': {'dateTime': end, 'timeZone': 'Europe/Zurich'}}
    event = service.events().insert(calendarId='jcavat@gmail.com', body=event).execute()
    print(event['status'])

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Affiche mon agenda')
    parser.add_argument('nb_events', metavar='N', type=int, nargs='?', default=20,
                       help="Nombre d'événements à afficher")
    parser.add_argument('-a', nargs=4, help='Insérer un événemets (Exemple: -a "mon événement" 10.10.2015 12:00 13:00)')

    args = parser.parse_args()
    if vars(args)['a'] is not None:
        make_reservation(*vars(args)['a'])
    else:
        main(vars(args)['nb_events'])


