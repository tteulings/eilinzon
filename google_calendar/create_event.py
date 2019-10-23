from datetime import datetime, timedelta
from google_calendar.cal_setup import get_calendar_service


def create_event(start, end, description):
       # creates one hour event tomorrow 10 AM IST

    print(start)
    service = get_calendar_service()

    start = datetime.strptime(start, "%Y-%m-%d").isoformat()
    end = datetime.strptime(end, "%Y-%m-%d").isoformat()

    # tomorrow = datetime(d.year, d.month, d.day, 10)+timedelta(days=1)
    # start = tomorrow.isoformat()
    # end = (tomorrow + timedelta(hours=1)).isoformat()

    event_result = service.events().insert(calendarId='eilinzon@gmail.com',
                                           body={
                                               "summary": f"REQUEsT: {description}",
                                               "description": 'Made by website',
                                               "start": {"dateTime": start, "timeZone": 'Europe/Amsterdam'},
                                               "end": {"dateTime": end, "timeZone": 'Europe/Amsterdam'},
                                           }
                                           ).execute()

    print(event_result)

if __name__ == '__main__':
    create_event(0,0,"Test")