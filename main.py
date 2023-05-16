import yfinance as yf
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import datetime

# Define the list of top 10 IT company stocks
top_stocks = ["AAPL", "MSFT", "AMZN", "GOOGL", "META", "TSLA", "NVDA", "INTC", "ADBE", "CSCO"]

# Create the Dash application
app = dash.Dash(__name__)
app.title = "Stock Visualization"

# Define the layout of the application
app.layout = html.Div(children=[
    html.H1('Stock Visualization Dashboard'),
    html.H4('Please select a stock'),
    dcc.Dropdown(
        id="stock-dropdown",
        options=[{'label': stock, 'value': stock} for stock in top_stocks],
        value=top_stocks[0]  # Set the initial value to the first stock in the list
    ),
    html.Div(id="output-graph")
])


# Define the callback function for updating the graph based on the selected stock
@app.callback(
    Output(component_id="output-graph", component_property="children"),
    [Input(component_id="stock-dropdown", component_property="value")]
)
def update_graph(stock):
    # Retrieve stock data using yfinance
    stock_data = yf.Ticker(stock)
    df = stock_data.history(period="1d", start="2010-01-01", end=datetime.datetime.now())

    # Create the graph figure
    graph_figure = {
        'data': [{'x': df.index, 'y': df.Close, 'type': 'line', 'name': stock}],
        'layout': {'title': stock}
    }

    # Create and return the graph component
    return dcc.Graph(id="stock-graph", figure=graph_figure)


if __name__ == "__main__":
    app.run_server(debug=True)
