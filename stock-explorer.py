# Importing the Required Libraries
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import yfinance as yf
from datetime import date
from dateutil.relativedelta import relativedelta
import functools


@functools.lru_cache(maxsize=128)
def fetch_stock_data(ticker, start_time, end_time = date.today()):
    '''
        Fetches the Stock Historical Data for the Ticker Symbol between the Time Periods from Yahoo Finance
        Inputs : 
            ticker - Yahoo Finance Stock Ticker Symbol
            start_time - Start Date for fetching the Historical Data
            end_time - End Date for fetching the Historical Data
        Outputs :
            DataFrame - Historical Data
    '''
    print(f"Fetching the Stock Data for {ticker} from {start_time} to {end_time}")
    tickerData = yf.Ticker(ticker)
    ticker_history_df = tickerData.history(period='1d', start=start_time, end=end_time)
    return ticker_history_df


def get_delta_data(time_period):
    '''
        Gets the Date from the Current Date based on the time period
        Inputs :
            time_period - How long lookback period
        Outputs :
            date - Old Date from the Current Date
    '''

    print("timepriod is - ", time_period)

    today_date = date.today()

    if time_period == "1Y":
        start_time = today_date + relativedelta(months= -12)
    elif time_period == "6M":
        start_time = today_date + relativedelta(months = -6)
    elif time_period == "3M":
        start_time = today_date + relativedelta(months = -3)
    else:
        start_time = today_date + relativedelta(months= -1)

    return start_time


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.COSMO])
server = app.server


app.layout = dbc.Container([
    # Heading
    dbc.Row(html.H1("Stock Explorer"), justify='center'),

    # Inputs - Ticker and Time Period
    dbc.Row([
        dbc.Col(dbc.Input(id="ticker", debounce=True, placeholder="Enter a Stock Ticker...", type="text"), width=5, align='center'),
        dbc.Col(dbc.RadioItems(options = [
            {"label": "1Y", "value": "1Y"},
            {"label": "6M", "value": "6M"},
            {"label": "3M", "value": "3M"},
            {"label": "1M", "value": "1M"},
        ], value="1Y", inline=True, id="time_period"))
    ], style={'margin-top': '30px'}, justify='center'),

    # Graph 
    dbc.Row([
        dbc.Col(dbc.Spinner(color="primary", children = dcc.Graph(id="graph")))

    ])
], style={'margin-top': '100px'})


@app.callback(
    Output(component_id="graph", component_property="figure"),
    [Input(component_id="ticker", component_property="value"),
    Input(component_id="time_period", component_property="value")]
)
def plot_graph(ticker_symbol, time_period):

    # Default Stock Data to Display
    if(ticker_symbol is None):
        ticker_symbol = "^NSEI"


    start_date = get_delta_data(time_period)
    history_df = fetch_stock_data(ticker_symbol, start_date, date.today())

    line_chart = px.line(history_df.Close, title=f"{ticker_symbol} Price Movement")

    return line_chart




if __name__ == '__main__':
    app.run_server()

