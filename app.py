import pandas as pd
import datetime
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

from plot_generation import (get_data, day_vs_depart_plot, travel_plot, geomap_flight_by_date_plot)
#1) Congig
depart_city = 'Dallas-Fort Worth'
destin_city = 'Chicago'
from_date = pd.to_datetime('2019-12-01')
to_date = pd.to_datetime('2020-01-31')
df = get_data(directory='data.csv') #Impoer data



fig1 = day_vs_depart_plot(df, depart_city , destin_city, from_date, to_date, display_by = 'date')
fig2 = geomap_flight_by_date_plot(df, from_date, to_date)
fig3 = travel_plot(df, depart_city, from_date, to_date)

#2) Component

depart_dropdown = dcc.Dropdown(options = [{'label': i, 'value': i} for i in df['Origin City'].unique()],
                                value = depart_city,
                                clearable = False,
                               id='depart_dropdown',
                              )

arrive_dropdown = dcc.Dropdown(options = [{'label': i, 'value': i} for i in df['Destination City'].unique()],
                                value = destin_city,
                                clearable = False,
                               id='arrive_dropdown',
                              )

date_picker = dcc.DatePickerRange(min_date_allowed = datetime.date(2019, 1, 1),
                                    max_date_allowed = datetime.date(2021, 1, 31),
                                    start_date = from_date,
                                    end_date = to_date,
                                  id='date_picker',
                            )
time_filter_radio=dcc.RadioItems(options=[{'label': 'Date', 'value': 'date'},
                                        {'label': 'Hour', 'value': 'hour'},
                                        {'label': 'Date of Month', 'value': 'day of month'},
                                        {'label': 'Month', 'value': 'month'},
                                        {'label': 'Year', 'value': 'year'},
                                    ],
                                value='date',
                                labelStyle={'display': 'inline-block'},
                                 id='time_filter_radio',
                                )

graph_1 = dcc.Graph(figure = fig1, id='graph_1')
graph_2 = dcc.Graph(figure = fig2, id='graph_2')
graph_3 = dcc.Graph(figure = fig3, id='graph_3')

###### 3) Layout #######
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server ######## Deployment !!!!!!!!

app.layout = html.Div([
    html.H3(children='AA Flights Analysis', style = {'text-align': 'center'}),

    html.Div([ html.Div(depart_dropdown, style = {'display': 'inline-block', 'width' : '30%'}),
                html.Div(arrive_dropdown, style = {'display': 'inline-block', 'width' : '30%'}),
             ],style={'display': 'block', 'margin-left': 'auto', 'margin-right': 'auto', 'text-align': 'center'}),

    html.Div(date_picker,style={'display': 'block', 'margin-left': 'auto', 'margin-right': 'auto', 'text-align': 'center'}),

    html.Div(graph_1),
    html.Div(time_filter_radio, style={'display': 'block', 'margin-left': 'auto', 'margin-right': 'auto', 'text-align': 'center', 'marginTop': '20'}),
    html.Div([ html.Div(graph_3, style = {'display': 'inline-block', 'width' : '49%'}),
                html.Div(graph_2, style = {'display': 'inline-block', 'width' : '49%'}),
             ])
])

#####  4) Callback function #####
#Graph 1
@app.callback(Output('graph_1', 'figure'),
              [Input('date_picker', 'start_date'), Input('date_picker', 'end_date'),
              Input('depart_dropdown', 'value'),Input('arrive_dropdown', 'value'), Input('time_filter_radio', 'value')
              ])
def update_graph_1(start_date, end_date, depart_city, arrive_city, time_filter):
    fig = day_vs_depart_plot(df, depart_city=depart_city , destin_city=arrive_city, from_date=start_date, to_date=end_date, display_by = time_filter)
    return fig

#Graph 2
@app.callback(Output('graph_2', 'figure'),
              [Input('date_picker', 'start_date'), Input('date_picker', 'end_date'),])
def update_graph_2(start_date, end_date):
    fig = geomap_flight_by_date_plot(df, from_date = start_date, to_date = end_date)
    return fig

#Graph 3
@app.callback(Output('graph_3', 'figure'),
              [Input('depart_dropdown', 'value'), Input('date_picker', 'start_date'), Input('date_picker', 'end_date'),])
def update_graph_3(depart_city, start_date, end_date):
    fig = travel_plot(df, depart_city=depart_city, from_date=start_date, to_date=end_date)
    return fig

if __name__ == '__main__':
    app.run_server() ######## Deployment !!!!!!!!
    # app.run_server(debug=False,host = '127.0.0.1') #For offline use
