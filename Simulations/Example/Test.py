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
day = 1
endtime = day * 24*60*60*1000

env = simpy.Environment(start_time)

_sf = np.random.choice(LoRaParameters.SPREADING_FACTORS)
lora_param = LoRaParameters(freq=np.random.choice(LoRaParameters.DEFAULT_CHANNELS),
                            sf=_sf,
                            bw=125, cr=5, crc_enabled=1, de_enabled=0, header_implicit_mode=0, tp=14)

node_location = Location(x=5,y=5,indoor=False)
gateway_location = Location(x=1,y=1,indoor=False)

gateway = Gateway(env, gateway_location, max_snr_adr=True, avg_snr_adr=False)
air_interface = AirInterface(gateway, PropagationModel.LogShadow(std=7.9), SNRModel(), env)

node1 = Node(1, EnergyProfile(5.7e-3, 15, tx_power_mW, rx_power=rx_measurements), Battery(solar_data = dataset, env=env), lora_param, sleep_time=(8 * random.choice(range(5, 56, 5)) / transmission_rate_bit_per_ms), 
            process_time=5,
            adr=True,
            location=node_location,
            base_station=gateway, env=env, payload_size=8, air_interface=air_interface,
            confirmed_messages=True)

node2 = Node(2, EnergyProfile(5.7e-3, 15, tx_power_mW, rx_power=rx_measurements), Battery(solar_data = dataset, env=env), lora_param, sleep_time=(8 * random.choice(range(5, 56, 5)) / transmission_rate_bit_per_ms),
            process_time=5,
            adr=True,
            location=node_location,
            base_station=gateway, env=env, payload_size=8, air_interface=air_interface,
            confirmed_messages=True)

env.process(node2.run())
env.process(node1.run())
env.run(until=endtime)
node1.plot()