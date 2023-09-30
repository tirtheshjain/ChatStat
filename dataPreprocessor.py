import re
import pandas as pd

def preprocess(data):
    pattern = '\d{1,2}/\d{1,2}/\d{1,2},\s\d{1,2}:\d{2}\s[APM]{2}\s-\s'

    user_messages = re.split(pattern, data)[1:]
    dates_list = re.findall(pattern, data)

    modified_dates = []

    for date_string in dates_list:
        # Split the string by comma and space
        parts = date_string.split(", ")
        
        if len(parts) == 2:
            date_part, time_part = parts
            time_part = time_part.rstrip(" - ")  # Remove the trailing space and hyphen
            modified_date = f"{date_part} {time_part}"
            modified_dates.append(modified_date)

    datetime_list = pd.to_datetime(modified_dates)

    users = []
    messages = []
    for message in user_messages:
        match = re.match('([^:]+):\s(.+)', message)
        if match:
            username, message_content = match.groups()
            users.append(username)
            messages.append(message_content)
        else:
            users.append('group_notification')
            messages.append(message)

    df = pd.DataFrame({'user': users, 'datetime': datetime_list})

    df['only_date'] = df['datetime'].dt.date
    df['year'] = df['datetime'].dt.year
    df['month_num'] = df['datetime'].dt.month
    df['month'] = df['datetime'].dt.month_name()
    df['day'] = df['datetime'].dt.day
    df['day_name'] = df['datetime'].dt.day_name()
    df['hour'] = df['datetime'].dt.hour
    df['minute'] = df['datetime'].dt.minute

    period = []
    for hour in df[['day_name', 'hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))

    df['period'] = period

    return df
