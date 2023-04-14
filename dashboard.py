
from data_processor import dataprocessor
import plot_maker
from constants import DESCRIPTION_URL_DICTIONARY
import pandas as pd
from datetime import datetime, date, timedelta
from dash import Dash,dcc, html, Input, Output, no_update
from US_time import ComputeUSTime


app = Dash(__name__)
server = app.server

app.layout = html.Div([
    html.H2(children= "Interactive U.S. Weather Description", style={'textAlign':'center'}),
    html.H3(children= "Nov. 2012-Oct. 2017", style={'textAlign':'center'}),
    html.P('Displays weather data for cities across the US at selected dates or times.',style={'textAlign':'center'}),
    html.Div(
    html.Ul([html.Li('Arrow direction: wind direction'),
            html.Li('Arrow size: wind speed'),
            html.Li('Arrow color: temperature'),
            html.Li('Calendar: select central day'),
            html.Li('Radio items: hourly data or daily averages'),
            html.Li('Slider: given chosen day, select hour or day in vicinity'),
            html.Li('Hover: view temperature, weather description with picture, and wind speed for city')],
            style={'display': 'inline-block', 'textAlign':'left'}
            ),
            style={'textAlign': "center"}
            ),
    # Calendar and radio items
    html.Div([dcc.DatePickerSingle(id='date-picker-single',
                                   min_date_allowed=date(2012, 11, 1),
                                   max_date_allowed=date(2017, 10, 31),
                                   initial_visible_month=date(2015, 8, 5),
                                   date=date(2015, 8, 25),
                                   style={'float': 'left', 'margin': 'auto'}
                                   ),

              dcc.RadioItems(options=[{'label': 'per hour', 'value': 'hourly'},
                                      {'label': 'daily average', 'value': 'daily_average'}
                                      ],
                             value='hourly',
                             id='data_type',
                             style={'float': 'left', 'margin': 'auto'},
                             )],
             className='row'),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    # Hour slider
    html.Div(id='slider_container', children=[dcc.Slider(0, 23, 1, id='time-select',
                                                         marks={
                                                             val: ComputeUSTime(val).compute_US_time() for val in range(24)},
                                                         value=12)]),
    # Day slider
    html.Div(id='slider_container_days',
             children=[
                 html.Div([
                     html.P(children= 'day(s)', style={'float': 'right','fontSize': 14,'margin-top':'-15px'}),
                     html.P(children= 'day(s)',style={'float': 'left','fontSize': 14,'margin-top':'-15px'})],
                     className='row'),
                 dcc.Slider(-15, 15, 1, id='date-select',value=0,included=False),
             ],
             ),
    # Graph
    dcc.Graph(id='plot', clear_on_unhover=True),
    # Hover
    dcc.Tooltip(id="graph-tooltip")
])


# Updates which slider is visible based on radio items choice
@app.callback(
    Output('slider_container', 'style'),
    Input('data_type', 'value'))
def set_cities_options(option):
    if option == 'hourly':
        return {'display': 'block'}
    else:
        return {'display': 'none'}


@app.callback(
    Output('slider_container_days', 'style'),
    Output('date-select','marks'),
    Input('data_type', 'value'),
    Input('date-picker-single', 'date'))
def update_date_day_slider(option,date):
    date = '2015-08-25' if date == None else date
    if option != 'hourly':
        marks = {val: ({'label':f'{val:+}'} if val !=0 else {'label': date, 'style': {'color': '#f50','fontSize': 16,'margin-top':'-35px'}}) for val in range(-15,16)}
        return {'display': 'block'}, marks
    else:
        return {'display': 'none'}, None


# Updates the graph based on date or time choice
@app.callback(
    Output('plot', 'figure'),
    Input('date-picker-single', 'date'),
    Input('time-select', 'value'),
    Input('date-select', 'value'),
    Input('data_type', 'value')
)
def update_figure(date, time, date_delta, datatype):
    date = '2015-08-25' if date == None else date
    if datatype == 'hourly':
        datetime_datetime = datetime.fromisoformat(
            date) + timedelta(hours=time)
        datetime_datetime = pd.to_datetime(datetime_datetime)
    else:
        datetime_datetime = datetime.fromisoformat(date).date() + timedelta(days=date_delta)



    data_in_time = dataprocessor.get_organized_wind_data_in_time(
        datetime_datetime, datatype)
    fig = plot_maker.PlotMaker(data_in_time).plot_maker()
    fig.update_traces(hoverinfo="none", hovertemplate=None)
    return fig


# Updates hover
@app.callback(
    Output("graph-tooltip", "show"),
    Output("graph-tooltip", "bbox"),
    Output("graph-tooltip", "children"),
    Input('plot', "hoverData"),
    Input('date-picker-single', 'date'),
    Input('time-select', 'value'),
    Input('data_type', 'value')
)
def update_hover(hoverData, date, time, datatype):
    date = '2015-08-25' if date == None else date
    if hoverData is None:
        return False, no_update, no_update

    pt_lat = hoverData["points"][0]['lat']
    pt_lon = hoverData["points"][0]['lon']
    bbox = hoverData["points"][0]["bbox"]

    if datatype == 'hourly':
        datetime_datetime = datetime.fromisoformat(
            date) + timedelta(hours=time)
        datetime_datetime = pd.to_datetime(datetime_datetime)
    else:
        datetime_datetime = datetime.fromisoformat(date).date()
    city, temp, desc, speed = dataprocessor.get_hover_data_in_time(
        pt_lat, pt_lon, datetime_datetime, datatype)
    img_src = DESCRIPTION_URL_DICTIONARY[desc]

    if len(desc) > 300:
        desc = desc[:100] + '...'

    children = [
        html.Div([
            html.Img(src=img_src, style={"width": "100%"}),
            html.H2(f"{city}", style={"color": "darkblue",
                    "overflow-wrap": "break-word"}),
            html.P(f"{temp:.1f}"u'\N{DEGREE SIGN}F'),
            html.P(f'{desc}'),
            html.P(f"{speed:.1f} m/s"),
        ], style={'width': '200px', 'white-space': 'normal'})
    ]

    return True, bbox, children

if __name__ == '__main__':
    app.run_server(debug=True)
