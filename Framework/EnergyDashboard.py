from Simulations.GlobalConfig import *
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import paho.mqtt.client as mqtt
import json
import datetime

battery_data = {}
prev_topic = None

def on_message(client, userdata, message):
    data = json.loads(message.payload.decode())
    time = datetime.datetime.utcfromtimestamp(data['time']).strftime('%Y-%m-%d %H:%M:%S')
    battery_level = data['battery_level']
    node_id = int(message.topic.split('/')[1])
    if node_id not in battery_data:
        battery_data[node_id] = []
    battery_data[node_id].append((time, battery_level))


def connection(id=None):
    client = mqtt.Client(id)
    broker_address = "localhost"
    broker_port = 1883
    client.connect(broker_address, broker_port, 60)
    return client

mqtt_client = connection()
mqtt_client.on_message = on_message
for i in range(1, num_locations + 1):
    mqtt_client.subscribe(f"node/{i}/battery")
mqtt_client.loop_start()

app = dash.Dash(__name__)

app.layout = html.Div([
    html.Label("Select Node ID:"),
    dcc.Dropdown(
        id='node-dropdown', 
        options=[{'label': str(i), 'value': i} for i in range(1, num_locations + 1)],
        value=None
    ),
    dcc.Graph(id='battery-graph', figure={'layout': {'title': 'Battery Level Over Time'}}),
    dcc.Interval(id='interval-component', interval=1*1000, n_intervals=0)
])

@app.callback(
    [Output('battery-graph', 'figure')],
    [Input('interval-component', 'n_intervals'), Input('node-dropdown', 'value')]
)


def update_graphs(n, node_id):
    data = battery_data.get(node_id, [])
    # print(f"Data for node {node_id} is: {data}")
    if data:
        times, battery_levels = zip(*data)
        battery_figure = {
            'data': [{'x': times, 'y': battery_levels, 'type': 'line', 'name': 'Battery Level'}],
            'layout': {'title': 'Battery Level Over Time'}
        }
    else:
        battery_figure = {'data': [], 'layout': {'title': 'Battery Level Over Time'}}
    
    return [battery_figure]



if __name__ == '__main__':
    app.run_server(debug=True)
