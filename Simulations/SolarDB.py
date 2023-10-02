import pandas as pd
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

# InfluxDB settings
token = "M0lj1uTaCHTJjLKh_QTRlOSb70JG08KHRLcv-D3eFT19k79F1TkajiDAHrslZUBjwUSflaSS4-3TdsiVYBHE5g=="
org = "Baikuntha"
bucket = "Solar"
client = InfluxDBClient(url="http://localhost:8086", token=token)
write_api = client.write_api(write_options=SYNCHRONOUS)

# Read CSV into a DataFrame
df = pd.read_csv("annotated_dataset.csv")

# Iterate over DataFrame rows and write data to InfluxDB
for _, row in df.iterrows():
    point = Point("solar_data") \
        .field("I_in", row["I_in"]) \
        .field("V_in", row["V_in"]) \
        .time(row["datetime"], WritePrecision.S) # Assuming the datetime in your CSV is in seconds precision
    write_api.write(bucket, org, point)

# Close the client
write_api.__del__()
