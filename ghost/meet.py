import meetup.api
from datetime import datetime, timedelta
key = '39742216187936612d1055305074549'


def grouping(name):
    print(name)
    client = meetup.api.Client(key)

    name = name.replace(" ","-")
    group_info = client.GetGroup({'urlname': name})

    timer = group_info.next_event['time']
    
    tot = datetime.fromtimestamp(timer/1000.0)
    msg = tot.strftime("%Y-%m-%d %H:%M")
    

    result = {
        'Name': group_info.name,
        'Organizer': group_info.organizer['name'],
        'City': group_info.city,
        'Upcoming Event': {
            'Event Name': group_info.next_event['name'],
            'RSVP': str(group_info.next_event['yes_rsvp_count']),
            'Time': msg
        },
        'Link': str(group_info.link)
    }
    #print(result)
    return result

#x = "GDG Ranchi"
#zz = grouping(x)
#print(zz["Upcoming Event"]["RSVP"])