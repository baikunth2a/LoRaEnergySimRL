from Simulations.GlobalConfig import *
import paho.mqtt.client as mqtt
import json
import datetime


from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

# You can generate a Token from the "Tokens Tab" in the UI
token = "M0lj1uTaCHTJjLKh_QTRlOSb70JG08KHRLcv-D3eFT19k79F1TkajiDAHrslZUBjwUSflaSS4-3TdsiVYBHE5g=="
org = "Baikuntha"
bucket = "Thesis"

influxclient = InfluxDBClient(url="http://localhost:8086", token=token)
write_api = influxclient.write_api(write_options=SYNCHRONOUS)

def on_message(client, userdata, message):
    data = json.loads(message.payload.decode())
    point = Point("battery_check_new").tag("node_id", data['node_id']).field("battery_level", float(data['battery_level'])).time(datetime.datetime.fromisoformat(data['time']), WritePrecision.MS)
    write_api.write(bucket, org, point)

mqtt_client = mqtt.Client()
mqtt_client.on_message = on_message
mqtt_client.connect("localhost", 1883, 60)
mqtt_client.subscribe("battery")
mqtt_client.loop_forever()