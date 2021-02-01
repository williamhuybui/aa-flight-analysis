import pandas as pd
import datetime
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px

############ Get data ###########
def get_data(directory='data.csv'):
    df = pd.read_csv(directory)
    df['Departure Time'] = pd.to_datetime(df['Departure Time'].apply(lambda x: str(x)[:-6]), format = '%Y-%m-%d %H:%M:%S')
    df['Arrival Time'] = pd.to_datetime(df['Arrival Time'].apply(lambda x: str(x)[:-6]), format = '%Y-%m-%d %H:%M:%S')
    return df

############ Datetime and number of Flights ##############
def get_day_vs_depart_data(df, depart_city, destin_city,  from_date, to_date):
    """
    Filter data base on city points and date range
    """
    df=df.copy()
    from_date = pd.to_datetime(from_date)
    to_date = pd.to_datetime(to_date)
    cond_1 = (df['Origin City']==depart_city) & (df['Destination City']==destin_city)
    cond_2 = (df['Departure Time']>=from_date) & (df['Departure Time']<=to_date)
    df= df[cond_1 & cond_2]
    return df.reset_index(drop=True)

def day_vs_depart_plot(df, depart_city, destin_city, from_date, to_date, display_by = 'hour'):
    """
    Return day vs depart plot based on the resolution desired (display_by includes: date, hour, day of month, month, year)
    """
    temp = get_day_vs_depart_data(df, depart_city, destin_city,  from_date, to_date)

    if display_by == 'date':
        temp['Departure Date'] = temp['Departure Time'].dt.date
        graph_data = temp.groupby(by = 'Departure Date', as_index=False).count()[['Departure Date','Flight Number']]
        graph_data['Average Duration'] = temp.groupby(by = 'Departure Date', as_index=False).mean()['Duration (min)']

        data= [go.Bar(x=graph_data['Departure Date'], y=graph_data['Flight Number'], name='Number of flights'),
               go.Scatter(x=graph_data['Departure Date'], y=graph_data['Average Duration'], yaxis="y2", name='Flight Duration (min)')
              ]

    if display_by == 'hour':
        temp['Departure Hour'] = [ f'0{i}:00' if len(str(i)) != 2 else  f'{i}:00' for i in temp['Departure Time'].dt.hour]
        graph_data = temp.groupby(by = 'Departure Hour', as_index=False).count()[['Departure Hour','Flight Number']]
        graph_data['Average Duration'] = temp.groupby(by = 'Departure Hour', as_index=False).mean()['Duration (min)']

        data= [go.Bar(x=graph_data['Departure Hour'], y=graph_data['Flight Number'], name='Number of flights'),
               go.Scatter(x=graph_data['Departure Hour'], y=graph_data['Average Duration'], yaxis="y2", name='Flight Duration (min)')
              ]

    elif display_by == 'day of month':
        temp['Departure Day'] = temp['Departure Time'].dt.day
        graph_data = temp.groupby(by = 'Departure Day', as_index=False).count()[['Departure Day','Flight Number']]
        graph_data['Average Duration'] = temp.groupby(by = 'Departure Day', as_index=False).mean()['Duration (min)']

        data= [go.Bar(x=graph_data['Departure Day'], y=graph_data['Flight Number'], name='Number of flights'),
               go.Scatter(x=graph_data['Departure Day'], y=graph_data['Average Duration'], yaxis="y2", name='Flight Duration (min)')
              ]

    elif display_by == 'month':
        temp['Departure Month'] = [datetime.datetime.strptime(str(i), "%m").strftime("%b") for i in temp['Departure Time'].dt.month]
        graph_data = temp.groupby(by = 'Departure Month', as_index=False).count()[['Departure Month','Flight Number']]
        graph_data['Average Duration'] = temp.groupby(by = 'Departure Month', as_index=False).mean()['Duration (min)']

        data= [go.Bar(x=graph_data['Departure Month'], y=graph_data['Flight Number'], name='Number of flights'),
               go.Scatter(x=graph_data['Departure Month'], y=graph_data['Average Duration'], yaxis="y2", name='Flight Duration (min)')
              ]

    elif display_by == 'year':
        temp['Departure Year'] = temp['Departure Time'].dt.year
        graph_data = temp.groupby(by = 'Departure Year', as_index=False).count()[['Departure Year','Flight Number']]
        graph_data['Average Duration'] = temp.groupby(by = 'Departure Year', as_index=False).mean()['Duration (min)']

        data= [go.Bar(x=graph_data['Departure Year'], y=graph_data['Flight Number'], name='Number of flights'),
               go.Scatter(x=graph_data['Departure Year'], y=graph_data['Average Duration'], yaxis="y2", name='Flight Duration (min)')
              ]

    layout = go.Layout(title=f'Number of Flights from {depart_city} to {destin_city} and Flight Duration by {display_by.upper()}',
                   yaxis=dict(title='Number of depart flights'),
                   yaxis2=dict(title='Average Duration (min)',
                               overlaying='y',
                               side='right'))

    fig = go.Figure(data=data, layout=layout)
    return fig

############ Where people travel ##############
def travel_plot(df, depart_city, from_date, to_date):
    """
    Return plot of destination vs number of flights from a given city with a given range
    """
    temp = df[(df['Departure Time']>=from_date) & (df['Departure Time']<=to_date)]
    temp = temp[temp['Origin City']==depart_city]
    temp['Departure Date'] = temp['Departure Time'].dt.date
    temp = temp.groupby(['Destination City', 'Departure Date'], as_index = False).count()
    temp['Number of Flights'] = temp["Flight Number"]

    fig = px.bar(temp, x="Departure Date", y='Number of Flights', color="Destination City",
                 title = f'Where people travel from {depart_city}', hover_data=['Number of Flights', "Departure Date"], barmode = 'stack')
    return fig

############ GEO MAP ##############
def geomap_flight_data(date):
    """
    Return data based on date
    """
    df=get_csv_from_date(date)
    count_dict = df.groupby("Flight Code").count()['Flight Number'].to_dict()
    df = df.drop_duplicates(subset = ['Flight Code']).reset_index(drop=True)
    df['No. flights'] = df['Flight Code'].map(count_dict)
    df['Color'] = sns.color_palette("hls", len(df))
    return df

def geomap_flight_by_date_plot(df, from_date, to_date):
    """
    Return a geo plot that has all the flight within a range
    """
    from_date = pd.to_datetime(from_date)
    to_date = pd.to_datetime(to_date)
    airport_df = df[(df['Departure Time']>=from_date) & (df['Departure Time']<=to_date)]

    #Data engineer
    arrival_count = airport_df.groupby('Destination Code').count()['Flight Number'].to_dict()
    depart_count = airport_df.groupby('Origin Code').count()['Flight Number'].to_dict()
    airport_df = airport_df.groupby(['Origin City', 'Destination City'], as_index=False).first()[['Origin Code','Origin City', 'Origin Latitude', 'Origin Longitude',
                                                                            'Destination Latitude', 'Destination Longitude']]
    airport_df['No. Arrivals'] = airport_df['Origin Code'].map(arrival_count)
    airport_df['No. Departs'] = airport_df['Origin Code'].map(depart_count)
    airport_df=airport_df.reset_index(drop=True)

    fig = go.Figure()

    #Arrival
    fig.add_trace(go.Scattergeo(locationmode = 'USA-states',
                                lon = airport_df['Origin Longitude'],
                                lat = airport_df['Origin Latitude'],
                                hoverinfo = 'text',
                                text = airport_df[['Origin City', 'No. Arrivals']],
                                marker_symbol = 'square',
                                name="Total Arrival Flights",
                                marker = dict(
                                    size = airport_df['No. Arrivals']*15/airport_df['No. Arrivals'].max(),
                                    color = 'maroon',
                                    opacity = 0.5
                                )))

    #Departure
    fig.add_trace(go.Scattergeo(locationmode = 'USA-states',
                                lon = airport_df['Origin Longitude'],
                                lat = airport_df['Origin Latitude'],
                                hoverinfo = 'text',
                                name="Total Depart Flights",
                                text = airport_df[['Origin City', 'No. Departs']],
                                mode = 'markers',
                                marker = dict(
                                    size = airport_df['No. Departs']*15/airport_df['No. Departs'].max(),
                                    color = 'green'

                                )))

    for i in range(len(airport_df)):
        fig.add_trace(
            go.Scattergeo(
                locationmode = 'USA-states',
                lon = [airport_df['Origin Longitude'][i], airport_df['Destination Longitude'][i]],
                lat = [airport_df['Origin Latitude'][i], airport_df['Destination Latitude'][i]],
                mode = 'lines',
                line = dict(width = 1,color = 'red'),
                hoverinfo='skip',
                opacity = airport_df['No. Departs'][i]/airport_df['No. Departs'][i].max(),
                showlegend = False
            )
        )

        fig.update_layout(
            title_text = f'Number of American Airline Flights From {str(from_date)[:10]} to {str(to_date)[:10]}',
            showlegend = True,
            geo = dict(
                scope='north america',
                projection_type = 'azimuthal equal area',
                showland = True),
            xaxis={'title': 'x-axis','fixedrange':True},
            yaxis={'title': 'y-axis','fixedrange':True}
        )
    fig.update_geos(fitbounds="locations")
    fig.update_layout(legend=dict(
                        yanchor="top",
                        y=0.99,
                        xanchor="left",
                        x=0.01
                    ))
    return fig
