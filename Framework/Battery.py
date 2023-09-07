import pandas as pd
dataset = pd.read_csv("dataset_one_day.csv", index_col=0, parse_dates=True)

class Battery:
    def __init__(self, env, capacity=1000, solar_data = dataset, charging_efficiency=0.9, discharging_efficiency=0.9):
        self.capacity = capacity
        self.state_of_charge = 0.0  # Initially empty
        self.charging_efficiency = charging_efficiency
        self.discharging_efficiency = discharging_efficiency
        self.solar_data = solar_data
        self.env = env
        self.power = 0
        self.delta_time = 0

    def charge(self, del_time):
    # Always add the del_time to the accumulated time.
        self.delta_time += del_time
        mask = self.solar_data.index.time == pd.Timestamp(self.env.now, unit='s').time()
        
        try:
            I, V = self.solar_data[mask].iloc[0][["I_in", "V_in"]]
            self.power = -(I*V)
            # Use the accumulated delta_time for the integration and then reset it to zero.
            self.state_of_charge = min(self.state_of_charge + (self.power * self.delta_time * self.charging_efficiency), self.capacity)
            self.delta_time = 0
        except IndexError:
            # If the index is missed, simply pass and keep accumulating the delta_time.
            pass

    def discharge(self, energy):
        energy /= self.discharging_efficiency
        self.state_of_charge = max(self.state_of_charge - energy, 0)

    def get_state_of_charge(self):
        return self.state_of_charge

    def is_depleted(self):
        return self.state_of_charge <= 0
    
    def get_delta_time(self):
        return self.delta_time
