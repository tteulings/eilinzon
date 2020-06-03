from google_calendar import list_events, create_event
from datetime import date, datetime, timedelta


def get_events(time_delta = 110):
    coming_events = list_events.list_events(amount=3)
    
    ending_event = None
    starting_event = None
    
    for event in coming_events:
        start_date = datetime.strptime(event["start"]["date"], "%Y-%m-%d")
        end_date = datetime.strptime(event["end"]["date"], "%Y-%m-%d")

        now = datetime.now()

        if start_date >= now >= (start_date - timedelta(hours=time_delta)):
            print(
                f"Start date within {time_delta} hours for visit: {event['summary']}")

            starting_event = event
        
        if (end_date - timedelta(hours=time_delta) >= now >= (end_date - timedelta(hours=time_delta+24))):
            print(
                f"End date within {time_delta+24} and {time_delta} hours for visit: {event['summary']}")

            ending_event = event


    return ending_event, starting_event