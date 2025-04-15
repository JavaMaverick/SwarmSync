# SwarmSync: A Hybrid Bee-Ant Bio-Inspired Framework for 3D Drone Mesh Networks

## Overview

SwarmSync is a Python-based simulation framework for adaptive 3D drone mesh networks, combining ant-inspired pheromone trails and bee-inspired waggle dance communication to optimize network connectivity, target coverage, and energy efficiency. This project implements the hybrid bio-inspired approach described in the research paper *"SwarmSync: A Hybrid Bee-Ant Bio-Inspired Framework for Adaptive 3D Drone Mesh Networks"* by Priyanshu Singh et al. It simulates a swarm of 20 drones in a 1000x1000x100m³ environment with dynamic targets and static obstacles, comparing the hybrid model against an ant-inspired baseline.

The simulation visualizes drone behaviors, tracks performance metrics (e.g., target coverage, swarm cohesion, network connectivity, pheromone trail density), and generates comparative plots. It is designed for researchers and developers interested in swarm intelligence, drone coordination, and bio-inspired algorithms.

## Features

- **Hybrid Bio-Inspired Model**:
  - **Ant-Inspired**: Pheromone trails (60s lifespan, strength = priority × 1.0) for decentralized pathfinding and self-healing.
  - **Bee-Inspired**: Waggle dance signals (30s lifespan, strength = priority × 2.0, 70% probability) and scouting (20% of drones, 15 m/s) for rapid target detection.
  - Energy optimization prioritizing targets by distance-to-priority ratio.
- **3D Simulation**:
  - Environment: 20 drones, 20 obstacles (5-20m radius), 5 initial targets (priority 1-5).
  - Dynamic targets: 1% addition, 0.5% removal per frame.
  - Real-time updates every 0.1s over 1000 frames (100s).
- **Visualization**:
  - 3D plots of drones (active, scout, leader, inactive), obstacles, targets, trails, and signals using Matplotlib.
  - Updated every 50ms via `FuncAnimation`.
- **Metrics**:
  - Target coverage, network connectivity, swarm cohesion, pheromone trail density, and more.
  - Saved to pickle files (`ant_metrics.pkl`, `hybrid_metrics.pkl`).
- **Comparison**:
  - Plots comparing hybrid (SwarmSync) vs. ant-inspired baseline, showing 60% more targets detected, 14% more links, and 32% better cohesion.

## Repository Structure

```
SwarmSync/
├── drone_mesh_network/
│   ├── simulation/
│   │   ├── drone.py              # Base drone class with ant-inspired behaviors
│   │   ├── environment.py        # Ant-inspired simulation environment
│   │   ├── hybrid_drone.py       # Hybrid drone with bee-inspired behaviors
│   │   ├── hybrid_environment.py # Hybrid simulation environment
│   ├── visualization/
│   │   ├── visualizer.py         # Ant-inspired visualizer
│   │   ├── hybrid_visualizer.py  # Hybrid visualizer with scout and signal support
├── main.py                       # Runs ant-inspired simulation
├── hybrid_main.py                # Runs hybrid simulation
├── compare_simulations.py        # Generates comparative plots
├── ant_metrics.pkl               # Metrics from ant-inspired simulation
├── hybrid_metrics.pkl            # Metrics from hybrid simulation
├── Final_Review.pdf              # Research paper
├── README.md                     # This file
```

## Prerequisites

- Python 3.8+
- Required libraries:

  ```bash
  pip install matplotlib numpy
  ```

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/SwarmSync.git
   cd SwarmSync
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

   Create a `requirements.txt` with:

   ```
   matplotlib==3.7.1
   numpy==1.24.3
   ```

## Usage

1. **Run the Ant-Inspired Simulation**:

   ```bash
   python main.py
   ```

   - Simulates 20 drones with pheromone trails.
   - Saves metrics to `ant_metrics.pkl`.
   - Displays a 3D visualization.

2. **Run the Hybrid Bee-Ant Simulation**:

   ```bash
   python hybrid_main.py
   ```

   - Simulates 20 drones with trails, signals, and scouts.
   - Saves metrics to `hybrid_metrics.pkl`.
   - Displays a 3D visualization with enhanced features.

3. **Compare Simulations**:

   ```bash
   python compare_simulations.py
   ```

   - Loads `ant_metrics.pkl` and `hybrid_metrics.pkl`.
   - Generates plots:
     - `target_coverage_comparison.png`
     - `network_connectivity_comparison.png`
     - `swarm_cohesion_comparison.png`
     - `pheromone_trail_density_comparison.png`

## Key Results

Based on the research paper:

- **Target Coverage**: SwarmSync detects 8 targets vs. 5 for ant-inspired (60% more) at 20s.
- **Network Connectivity**: Maintains 16 links vs. 14 (14% more) at 35s.
- **Swarm Cohesion**: Reduces to 300 units vs. 440 (32% better) at 35s.
- **Pheromone Trail Density**: Peaks at 0.8 trails/target vs. 0.2 (4x higher).

## Contributing

Contributions are welcome! To contribute:

1. Fork the repository.
2. Create a branch (`git checkout -b feature/your-feature`).
3. Commit changes (`git commit -m "Add your feature"`).
4. Push to the branch (`git push origin feature/your-feature`).
5. Open a pull request.

Please ensure code follows PEP 8 and includes comments for clarity.

## Limitations

- **Obstacle Avoidance**: Success rate (OASR) may overestimate due to simplistic collision checks.
- **Energy Model**: Basic battery drain (0.1% per 0.1s) lacks realism.
- **Performance**: Matplotlib may lag with many drones; consider Plotly for large swarms.
- **Static Obstacles**: Simulation assumes fixed obstacles; dynamic obstacles could enhance realism.

