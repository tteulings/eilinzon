from datetime import datetime, timedelta
from google_calendar.cal_setup import get_calendar_service


def create_event(start, end, description):
    service = get_calendar_service()

    start = datetime.strptime(start, "%d-%m-%Y")
    end = datetime.strptime(end, "%d-%m-%Y")
    end = (end + timedelta(hours=23, minutes=59))


    event_result = service.events().insert(calendarId='eilinzon@gmail.com',
                                           body={
                                               "summary": f"REQUEST: {description}",
                                               "description": 'Made by website',
                                               "start": {"dateTime": start.isoformat(), "timeZone": 'Europe/Amsterdam'},
                                               "end": {"dateTime": end.isoformat(), "timeZone": 'Europe/Amsterdam'},
                                           }
                                           ).execute()

if __name__ == '__main__':
    create_event(0,0,"Test")