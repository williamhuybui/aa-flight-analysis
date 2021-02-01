import requests
import json
import pandas as pd
import datetime

def query_flight_date(date):
    """
    Input: YYYY-MM-DD (str) .Example: '2020-01-01'
    Return: All flights info on that date (json)
    """

    root = 'http://localhost:3030/'
    parameter = f'flights?date={date}'
    query = root+parameter
    page = requests.get(query)
    return page.json()

def get_csv_from_json(json_data):
    df = {}

    for row in json_data:
        df.setdefault('Flight Number', []).append(row['flightNumber'])

        df.setdefault('Origin Code', []).append(row['origin']['code'])
        df.setdefault('Origin City', []).append(row['origin']['city'])
        df.setdefault('Origin Timezone', []).append(row['origin']['timezone'])
        df.setdefault('Origin Latitude', []).append(row['origin']['location']['latitude'])
        df.setdefault('Origin Longitude', []).append(row['origin']['location']['longitude'])

        df.setdefault('Destination Code', []).append(row['destination']['code'])
        df.setdefault('Destination City', []).append(row['destination']['city'])
        df.setdefault('Destination Timezone', []).append(row['destination']['timezone'])
        df.setdefault('Destination Latitude', []).append(row['destination']['location']['latitude'])
        df.setdefault('Destination Longitude', []).append(row['destination']['location']['longitude'])

        df.setdefault('Distance', []).append(row['distance'])
        df.setdefault('Duration (min)', []).append(row['duration']['hours']*60 + row['duration']['minutes'])
        df.setdefault('Departure Time', []).append(row['departureTime'])
        df.setdefault('Arrival Time', []).append(row['arrivalTime'])

        df.setdefault('Aircraft Model', []).append(row['aircraft']['model'])
        df.setdefault('Aircraft Passenger Capacity', []).append(row['aircraft']['passengerCapacity']['total'])
        df.setdefault('Aircraft Speed', []).append(row['aircraft']['speed'])

    return pd.DataFrame(df)

def get_csv_from_date(date):

    json_data = query_flight_date(date)
    df = get_csv_from_json(json_data)

    #Data manipulation
    df['Origin Longitude']=df['Origin Longitude']*(-1) #They have wrong Longitude
    df['Destination Longitude']=df['Destination Longitude']*(-1)
    df['Flight Code'] = df['Origin Code'] +'→'+ df['Destination Code']
    return df

def main(starting_time='', ending_time=''):
    """
    Example: main(starting_time='2018-01-01', ending_time='2021-01-31')
    """
    df=pd.DataFrame({})
    starting_time = pd.to_datetime(starting_time)
    ending_time = pd.to_datetime(ending_time)
    day_interval = (ending_time-starting_time).days

    for num_day in range(day_interval+1):
        current_date = starting_time +  datetime.timedelta(days=num_day)
        current_date_str = str(current_date)[:10]
        temp = get_csv_from_date(current_date_str)
        df = df.append(temp)

    df = df.reset_index(drop=True)
    return df

#Example :
# df = main(starting_time='2018-01-01', ending_time='2021-01-31')
# df.to_csv('data.csv', index = False)
