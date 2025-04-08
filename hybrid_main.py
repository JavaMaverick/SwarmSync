# # drone_mesh_network/hybrid_main.py

# import time
# import logging
# from matplotlib.animation import FuncAnimation
# import matplotlib.pyplot as plt

# from drone_mesh_network.simulation.hybrid_environment import HybridEnvironment
# from drone_mesh_network.visualization.hybrid_visualizer import HybridVisualizer

# # Configure logging
# logging.basicConfig(
#     level=logging.INFO,
#     filename='hybrid_simulation.log',
#     filemode='w',
#     format='%(asctime)s - %(levelname)s - %(message)s'
# )

# def main():
#     logging.info("Initializing hybrid drone mesh network simulation...")
#     env = HybridEnvironment(num_drones=20, num_obstacles=20, num_targets=5)
#     logging.info(f"Created environment with {len(env.drones)} drones, {len(env.obstacles)} obstacles, and {len(env.targets)} targets")
    
#     logging.info("Setting up visualization...")
#     vis = HybridVisualizer(env)
    
#     def update(frame):
#         if frame % 100 == 0:
#             active_drones = sum(1 for drone in env.drones.values() if drone.is_active)
#             logging.info(f"Frame {frame}: {active_drones} active drones, {len(env.targets)} targets remaining")
#         return vis.update_plot(frame)
    
#     logging.info("Starting simulation...")
#     ani = FuncAnimation(vis.fig, update, frames=range(1000), interval=50, blit=False)
    
#     plt.show()

# if __name__ == "__main__":
#     main()





import time
import logging
from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
import pickle

from drone_mesh_network.simulation.hybrid_environment import HybridEnvironment
from drone_mesh_network.visualization.hybrid_visualizer import HybridVisualizer

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    filename='hybrid_simulation.log',
    filemode='w',
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def main():
    logging.info("Initializing hybrid drone mesh network simulation...")
    env = HybridEnvironment(num_drones=20, num_obstacles=20, num_targets=5)
    logging.info(f"Created environment with {len(env.drones)} drones, {len(env.obstacles)} obstacles, and {len(env.targets)} targets")
    
    logging.info("Setting up visualization...")
    vis = HybridVisualizer(env)
    
    def update(frame):
        if frame % 100 == 0:
            active_drones = sum(1 for drone in env.drones.values() if drone.is_active)
            logging.info(f"Frame {frame}: {active_drones} active drones, {len(env.targets)} targets remaining")
        return vis.update_plot(frame)
    
    logging.info("Starting simulation...")
    ani = FuncAnimation(vis.fig, update, frames=range(1000), interval=50, blit=False)
    
    plt.show()
    
    # Save metrics to file
    logging.info("Saving simulation metrics to hybrid_metrics.pkl...")
    with open('hybrid_metrics.pkl', 'wb') as f:
        pickle.dump({
            'target_coverage': vis.target_coverage_history,
            'energy_efficiency': vis.energy_efficiency_history,
            'network_connectivity': vis.network_connectivity_history,
            'swarm_cohesion': vis.swarm_cohesion_history,
            'target_latency': vis.target_latency_history,
            'foreign_detection_rate': vis.fdr_history,
            'pheromone_trail_density': vis.ptd_history,
            'obstacle_avoidance_success': vis.oasr_history
        }, f)
    logging.info("Metrics saved successfully.")

if __name__ == "__main__":
    main()
