import datetime
from google_calendar.cal_setup import get_calendar_service


def list_events(cred="credentials.json", amount=10):
    service = get_calendar_service(cred)
    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
    events_result = service.events().list(
        calendarId='primary', timeMin=now,
        maxResults=amount, singleEvents=True,
        orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event['summary'])

    return events

if __name__ == '__main__':
    list_events()
