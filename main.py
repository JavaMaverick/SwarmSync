# main.py

import time
import logging
from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt

from drone_mesh_network.simulation.environment import Environment
from drone_mesh_network.visualization.visualizer import Visualizer

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    filename='simulation.log',
    filemode='w',
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def main():
    # Create the simulation environment
    logging.info("Initializing drone mesh network simulation...")
    env = Environment(num_drones=20, num_obstacles=20, num_targets=5)
    logging.info(f"Created environment with {len(env.drones)} drones, {len(env.obstacles)} obstacles, and {len(env.targets)} targets")
    
    # Create the visualizer
    logging.info("Setting up visualization...")
    vis = Visualizer(env)
    
    # Define the animation update function
    def update(frame):
        # Log frame updates periodically
        if frame % 100 == 0:
            active_drones = sum(1 for drone in env.drones.values() if drone.is_active)
            logging.info(f"Frame {frame}: {active_drones} active drones, {len(env.targets)} targets remaining")
        return vis.update_plot(frame)
    
    # Create the animation
    logging.info("Starting simulation...")
    ani = FuncAnimation(vis.fig, update, frames=range(1000), interval=50, blit=False)
    
    # Display the plot
    plt.show()

if __name__ == "__main__":
    main()



