import pandas as pd
dataset = pd.read_csv("dataset_one_day.csv", index_col=0, parse_dates=True).index.time


class Battery:
    def __init__(self, env, capacity=1000, solar_data = dataset, charging_efficiency=0.9, discharging_efficiency=0.9, power_scaling=1):
        self.capacity = capacity
        self.state_of_charge = 0.0  # Initially empty
        self.charging_efficiency = charging_efficiency
        self.discharging_efficiency = discharging_efficiency
        self.solar_data = solar_data
        self.env = env
        self.power = 0
        self.delta_time = 0
        self.power_scaling = power_scaling

    def charge(self, del_time):
        self.delta_time += del_time
        try:
            data_row = self.solar_data.loc[pd.Timestamp(self.env.now, unit='ms').time()]
            if not data_row.empty:
                self.power = -(data_row["I_in"].iloc[0]*data_row["V_in"].iloc[0])*self.power_scaling
                self.state_of_charge = min(self.state_of_charge + (self.power * self.delta_time * self.charging_efficiency), self.capacity)
                self.delta_time = 0
        except KeyError:
            pass



    def discharge(self, energy):
        energy /= self.discharging_efficiency
        self.state_of_charge = max(self.state_of_charge - energy, -100)

    def get_state_of_charge(self):
        return self.state_of_charge

    def is_depleted(self):
        return self.state_of_charge <= 0
    
    def get_delta_time(self):
        return self.delta_time
