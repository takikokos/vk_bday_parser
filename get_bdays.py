import vk


def gen_bday_event(first_name, last_name, bday):
    format_str = 'BEGIN:VEVENT\n'\
        'SUMMARY:Birthday\n'\
        'DTSTART;VALUE=DATE-TIME:{year}{month}{day}T100000Z\n'\
        'DTEND;VALUE=DATE-TIME:{year}{month}{day}T200000Z\n'\
        'DTSTAMP;VALUE=DATE-TIME:{year}{month}{day}T120000Z\n'\
        'RRULE:FREQ=YEARLY;UNTIL=20380119T000000\n'\
        'DESCRIPTION:Birthday of {name} {last_name}. Born at {year} (1900 = no idea when :) )\n'\
        'BEGIN:VALARM\n'\
        'TRIGGER:-PT1440M\n'\
        'ACTION:DISPLAY\n'\
        'DESCRIPTION:Reminder\n'\
        'END:VALARM\n'\
        'END:VEVENT\n'
    splited = bday.split('.')
    if len(splited) == 2: 
        splited.append('1900')
        print(f"{first_name}, {last_name} doesn't have year set")
    day, month, year = splited
    if len(day) == 1: day = '0' + day 
    if len(month) == 1: month = '0' + month 
    return format_str.format(year=year, month=month, day=day, name=first_name, last_name=last_name)

# set user_id to your's id
user_id = 1
# access_token (Сервисный ключ доступа) of app registered at https://vk.com/dev/standalone
access_token = ''
api_version = '5.124'

session = vk.Session(access_token=access_token)
api = vk.API(session, v=api_version)
friends = api.friends.get(user_id=user_id, fields='bdate')

birthdays = []
s = 0
for f in friends['items']:
    if f.get('bdate', None) is not None:
        birthdays.append([f['first_name'], f['last_name'], f.get('bdate')])
    else:
        s += 1

print(f"Couldn't parse {s} out of {s + len(birthdays)} birthdays")

with open('export_bdays_from_vk.ics', 'w') as out:
    out.write('BEGIN:VCALENDAR\n')
    out.write('VERSION:2.0\n')
    out.write('PRODID:-//get_bdays.py//EN\n')

    for b in birthdays:
        out.write(gen_bday_event(*b))

    out.write('END:VCALENDAR\n')

