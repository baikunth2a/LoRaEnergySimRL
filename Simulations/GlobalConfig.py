import numpy as np

############### SIMULATION SPECIFIC PARAMETERS ###############
start_with_fixed_sf = False
start_sf = 7

no_of_simulation_days = 1
scaling_factor = 200 #['0.1', '0.5', '1', '1.5', '2']
transmission_rate_id = str(scaling_factor)
# transmission_rate_bit_per_ms = scaling_factor*(12*8)/(60*60*1000)  # 12*8 bits per hour (1 typical packet per hour)
transmission_rate_bit_per_ms = scaling_factor*(12*8)/(60*60*1000)  # 12*8 bits per one minute (1 typical packet per minute)
simulation_time = 24 * 60 * 60 * 1000 * no_of_simulation_days/scaling_factor
cell_size = 10 #MODIFIED
adr = True
confirmed_messages = True

payload_sizes = range(5, 55, 5)
path_loss_variances = [7.9]  # [0, 5, 7.8, 15, 20]

MAC_IMPROVEMENT = False
num_locations = 50
num_of_simulations = 2 #MODIFIED

locations_file = f'Locations/{num_locations}_locations_{num_of_simulations}_sim.pkl'
results_file = f'Results/{adr}_{confirmed_messages}_{transmission_rate_id}_cnst_num_bytes.pkl'

############### SIMULATION SPECIFIC PARAMETERS ###############

############### DEFAULT PARAMETERS ###############
LOG_ENABLED = True
MAX_DELAY_BEFORE_SLEEP_MS = 500
PRINT_ENABLED = False
MAX_DELAY_START_PER_NODE_MS = np.round(simulation_time / 100)
track_changes = True
middle = np.round(cell_size / 2)
load_prev_simulation_results = True

############### DEFAULT PARAMETERS ###############
