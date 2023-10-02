import pandas as pd
import simpy
from Framework.Battery import Battery
import random
dataset = pd.read_csv("dataset_one_day.csv", index_col=0, parse_dates=True)

import numpy as np
from Framework.Node import Node
from Framework.EnergyProfile import EnergyProfile
from Framework.LoRaParameters import LoRaParameters
from Framework.Gateway import Gateway
from Framework.AirInterface import AirInterface
from Framework import PropagationModel
from Framework.SNRModel import SNRModel
from Framework.Location import Location
from Simulations.GlobalConfig import *

tx_power_mW = {2: 91.8, 5: 95.9, 8: 101.6, 11: 120.8, 14: 146.5}
rx_measurements = {'pre_mW': 8.2, 'pre_ms': 3.4, 'rx_lna_on_mW': 39,
                   'rx_lna_off_mW': 34,
                   'post_mW': 8.3, 'post_ms': 10.7}

start_time = 0
day = 2
endtime = day * 24*60*60*1000



node_distance_1 = 100000
node_distance_2 = 10
payload_size1 = 5   #random.choice(range(5, 56, 5))
payload_size2 = 55  #random.choice(range(5, 56, 5))
adr = False
battery_scaling=10
_sf = 7    #np.random.choice(LoRaParameters.SPREADING_FACTORS)  #[12, 11, 10, 9, 8, 7]

n_sim = f"p1:{payload_size1}_p2:{payload_size2}_adr:{adr}_b:{battery_scaling}_d1:{node_distance_1}_d2:{node_distance_2}_SF:{_sf}"

node_location1 = Location(x=node_distance_1,y=node_distance_1,indoor=False)
node_location2 = Location(x=node_distance_2,y=node_distance_2,indoor=False)
gateway_location = Location(x=0,y=0,indoor=False)

env = simpy.Environment(start_time)


lora_param = LoRaParameters(freq=np.random.choice(LoRaParameters.DEFAULT_CHANNELS),
                            sf=_sf,
                            bw=125, cr=5, crc_enabled=1, de_enabled=0, header_implicit_mode=0, tp=14)

gateway = Gateway(env, gateway_location, max_snr_adr=True, avg_snr_adr=False)
air_interface = AirInterface(gateway, PropagationModel.LogShadow(std=7.9), SNRModel(), env)

node1 = Node(1, EnergyProfile(5.7e-3, 15, tx_power_mW, rx_power=rx_measurements, low_battery_power=5.7e-9), Battery(solar_data = dataset, env=env, power_scaling=battery_scaling), lora_param, sleep_time=((8 * payload_size1) / transmission_rate_bit_per_ms), 
            process_time=5,
            adr=adr,
            location=node_location1,
            base_station=gateway, env=env, payload_size=payload_size1, air_interface=air_interface,
            confirmed_messages=True, n_sim=n_sim)

node2 = Node(2, EnergyProfile(5.7e-3, 15, tx_power_mW, rx_power=rx_measurements, low_battery_power=5.7e-9), Battery(solar_data = dataset, env=env, power_scaling=battery_scaling), lora_param, sleep_time=((8 * payload_size2) / transmission_rate_bit_per_ms),
            process_time=5,
            adr=adr,
            location=node_location2,
            base_station=gateway, env=env, payload_size=payload_size2, air_interface=air_interface,
            confirmed_messages=True, n_sim=n_sim)

env.process(node2.run())
env.process(node1.run())
env.run(until=endtime)
# node1.plot()