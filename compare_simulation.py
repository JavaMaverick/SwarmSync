#drone_mesh_network/compare_simulations.py

import pickle
import matplotlib.pyplot as plt
import numpy as np

def load_metrics(file_path):
    """Load metrics from a pickle file."""
    try:
        with open(file_path, 'rb') as f:
            return pickle.load(f)
    except (FileNotFoundError, pickle.PickleError) as e:
        print(f"Error loading {file_path}: {e}")
        return {}

def plot_comparison(ant_metrics, hybrid_metrics):
    """Plot comparisons between ant-inspired and hybrid bee-ant simulations."""
    # Check if metrics are loaded successfully
    if not ant_metrics or not hybrid_metrics:
        print("One or both metrics files are empty or failed to load.")
        return

    # Determine the number of frames based on the shorter simulation
    ant_frames = len(ant_metrics.get('target_coverage', []))
    hybrid_frames = len(hybrid_metrics.get('target_coverage', []))
    if ant_frames == 0 or hybrid_frames == 0:
        print("No target_coverage data available in one or both metrics.")
        return
    max_frames = min(ant_frames, hybrid_frames)
    time_steps = np.arange(0, max_frames * 0.1, 0.1)

    # Helper function to truncate or pad data
    def prepare_data(data, length, default_value=0):
        if not data:
            return [default_value] * length
        return data[:length] if len(data) >= length else data + [default_value] * (length - len(data))

    # Truncate or pad metrics to the same length
    ant_target_coverage = prepare_data(ant_metrics.get('target_coverage', []), max_frames)
    hybrid_target_coverage = prepare_data(hybrid_metrics.get('target_coverage', []), max_frames)
    ant_energy_efficiency = prepare_data(ant_metrics.get('energy_efficiency', []), max_frames)
    hybrid_energy_efficiency = prepare_data(hybrid_metrics.get('energy_efficiency', []), max_frames)
    ant_network_connectivity = prepare_data(ant_metrics.get('network_connectivity', []), max_frames)
    hybrid_network_connectivity = prepare_data(hybrid_metrics.get('network_connectivity', []), max_frames)
    
    # Additional metrics with defaults
    ant_swarm_cohesion = prepare_data(ant_metrics.get('swarm_cohesion', []), max_frames)
    hybrid_swarm_cohesion = prepare_data(hybrid_metrics.get('swarm_cohesion', []), max_frames)
    hybrid_fddr = prepare_data(hybrid_metrics.get('foreign_detection_rate', []), max_frames)
    ant_ptd = prepare_data(ant_metrics.get('pheromone_trail_density', []), max_frames)
    hybrid_ptd = prepare_data(hybrid_metrics.get('pheromone_trail_density', []), max_frames)
    ant_oasr = prepare_data(ant_metrics.get('obstacle_avoidance_success', []), max_frames)
    hybrid_oasr = prepare_data(hybrid_metrics.get('obstacle_avoidance_success', []), max_frames)

    # Plot 1: Target Coverage
    plt.figure(figsize=(10, 6))
    plt.plot(time_steps, ant_target_coverage, label='Ant-Inspired', color='blue')
    plt.plot(time_steps, hybrid_target_coverage, label='Hybrid Bee-Ant', color='orange')
    plt.xlabel('Time (s)')
    plt.ylabel('Number of Detected Targets')
    plt.title('Target Coverage Over Time')
    plt.legend()
    plt.grid()
    plt.savefig('target_coverage_comparison.png')
    plt.show()

    # Plot 2: Energy Efficiency
    plt.figure(figsize=(10, 6))
    plt.plot(time_steps, ant_energy_efficiency, label='Ant-Inspired', color='blue')
    plt.plot(time_steps, hybrid_energy_efficiency, label='Hybrid Bee-Ant', color='orange')
    plt.xlabel('Time (s)')
    plt.ylabel('Average Battery Level (%)')
    plt.title('Energy Efficiency Over Time')
    plt.legend()
    plt.grid()
    plt.savefig('energy_efficiency_comparison.png')
    plt.show()

    # Plot 3: Network Connectivity
    plt.figure(figsize=(10, 6))
    plt.plot(time_steps, ant_network_connectivity, label='Ant-Inspired', color='blue')
    plt.plot(time_steps, hybrid_network_connectivity, label='Hybrid Bee-Ant', color='orange')
    plt.xlabel('Time (s)')
    plt.ylabel('Number of Communication Links')
    plt.title('Network Connectivity Over Time')
    plt.legend()
    plt.grid()
    plt.savefig('network_connectivity_comparison.png')
    plt.show()

def main():
    """Main function to load metrics and generate plots."""
    ant_metrics = load_metrics('ant_metrics.pkl')
    hybrid_metrics = load_metrics('hybrid_metrics.pkl')
    plot_comparison(ant_metrics, hybrid_metrics)

if __name__ == "__main__":
    main()