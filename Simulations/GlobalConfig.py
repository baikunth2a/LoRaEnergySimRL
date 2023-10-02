import numpy as np

token = "M0lj1uTaCHTJjLKh_QTRlOSb70JG08KHRLcv-D3eFT19k79F1TkajiDAHrslZUBjwUSflaSS4-3TdsiVYBHE5g=="
org = "Baikuntha"
bucket = "Test"

############### SIMULATION SPECIFIC PARAMETERS ###############
start_with_fixed_sf = True
start_sf = 10

no_of_simulation_days = 4
scaling_factor = 1 #0.1, 0.5, 1, 1.5, 2
transmission_rate_id = str(scaling_factor)
transmission_rate_bit_per_ms = scaling_factor*(12*8)/(60*60*1000)  # 12*8 bits per one minute (1 typical packet per minute)
simulation_time = no_of_simulation_days * 24 * 60 * 60 * 1000/scaling_factor
cell_size = 1000
adr = False
confirmed_messages = True   #TO change DR

payload_sizes = range(5, 45, 5)
path_loss_variances = [15] #[0, 5, 7.8, 15, 20] #[0, 7.8, 20]
battery_scaling = [0.2, 0.4, 0.6, 0.8, 1]

MAC_IMPROVEMENT = False
num_locations = 1 #Modified
num_of_simulations = 1 #Modified

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
