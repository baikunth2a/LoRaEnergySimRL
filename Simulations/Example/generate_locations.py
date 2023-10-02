import os
import pickle
import matplotlib.pyplot as plt
import seaborn as sns

from Simulations.GlobalConfig import *
from Framework.Location import Location

locations_file = os.path.join("./Simulations/Example/", locations_file)

# num_locations = 3
# cell_size = 100
# num_of_simulations = 1

locations_per_simulation = list()

for num_sim in range(num_of_simulations):
    locations = list()
    for i in range(num_locations):
        locations.append(Location(min=0, max=cell_size, indoor=False))
    locations_per_simulation.append(locations)

os.makedirs(os.path.dirname(locations_file), exist_ok=True)
with open(locations_file, 'wb') as f:
    pickle.dump(locations_per_simulation, f)

# just to test the code
# Load locations from .pkl file
with open(locations_file, 'rb') as filehandler:
    locations = pickle.load(filehandler)

# Extract x and y coordinates from Location objects
x_coords = [location.x for simulation in locations for location in simulation]
y_coords = [location.y for simulation in locations for location in simulation]

# Setting the style using seaborn
sns.set_style("whitegrid")

# Plotting
plt.figure(figsize=(6, 6))
node_scatter = plt.scatter(x_coords, y_coords, color='red', edgecolor='red', s=200/(num_of_simulations*num_of_simulations), alpha=0.3, linewidth=0.5, label='Node')
gateway_location = Location(x=middle, y=middle, indoor=False)
gateway_scatter = plt.scatter(gateway_location.x, gateway_location.y, color='green', s=1500/(num_of_simulations*num_of_simulations), alpha=0.5, label='Gateway', edgecolor='green')

plt.legend(handles=[node_scatter, gateway_scatter])

plt.title("Locations Visualization")
plt.xlabel("X Coordinate")
plt.ylabel("Y Coordinate")

# Set axis limits to ensure they go up to cell_size
plt.xlim(0, cell_size)
plt.ylim(0, cell_size)

# Save the plot as an image
plt.grid(False)
plt.savefig('locations_visualization.png', dpi=300, bbox_inches='tight')
# Also show the plot
plt.show()

    
