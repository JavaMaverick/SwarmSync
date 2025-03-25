# SwarmSync: A Hybrid Bee-Ant Bio-Inspired Framework for Adaptive 3D Drone Mesh Networks

## Overview
This project simulates decentralized drone mesh networks using bio-inspired algorithms. It compares two models:

1. **Ant-Inspired Approach** - Drones use pheromone trails to coordinate and locate targets.
2. **Hybrid Bee-Ant Approach** - Enhances coordination with bee-like recruitment signals.

The simulation runs in a 3D environment, visualizing drone movements, target detection, obstacle avoidance, and network connectivity. Performance metrics such as target coverage, energy efficiency, and network connectivity are generated and compared. This repository contains Python scripts for simulation, visualization, and metrics analysis, showcasing swarm intelligence in action.

---

## Ant-Inspired Simulation (`main.py`)

### 1. Environment Setup
- Initializes a 3D space (1000x1000x100 units) with 20 drones, 20 obstacles, and 5 targets.
- Drones are randomly positioned with one designated as the leader.

### 2. Drone Behavior
- Drones detect targets and obstacles within sensor range, laying pheromone trails to guide others.
- They share knowledge with neighbors, avoid obstacles, and self-heal the network if drones fail.

### 3. Visualization
- A 3D animation displays drones, targets, obstacles, pheromone trails, and communication links.
- Metrics (target coverage, energy efficiency, network connectivity) are tracked in real-time.

### 4. Running the Simulation
```bash
python main.py
```
- Generates `ant_metrics.pkl` and displays the simulation.

### 5. Output
- Saves metrics to `ant_metrics.pkl` and logs simulation details to `simulation.log`.

---

## Hybrid Bee-Ant Simulation (`hybrid_main.py`)

### 1. Environment Setup
- Similar to the ant-inspired setup, with 20 drones, 20 obstacles, and 5 targets in a 3D space.

### 2. Enhanced Drone Behavior
- Incorporates scout drones (20% of total) that explore aggressively and use recruitment signals (waggle dance) to prioritize targets.
- Combines pheromone trails with energy optimization for efficient target tracking.

### 3. Visualization
- Displays drones, scouts, targets, obstacles, pheromone trails, recruitment signals, and communication links in 3D.
- Tracks the same metrics as the ant-inspired model.

### 4. Running the Simulation
```bash
python hybrid_main.py
```
- Generates `hybrid_metrics.pkl` and displays the simulation.

### 5. Output
- Saves metrics to `hybrid_metrics.pkl` and logs details to `hybrid_simulation.log`.

---

## Metrics Comparison (`drone_mesh_network/compare_simulations.py`)

### 1. Loading Metrics
- Reads `ant_metrics.pkl` and `hybrid_metrics.pkl` generated from the simulations.

### 2. Plotting Comparisons
- Generates three plots comparing:
  - **Target Coverage:** Number of detected targets over time.
  - **Energy Efficiency:** Average battery level (%) over time.
  - **Network Connectivity:** Number of communication links over time.
- Saves plots as PNG files (e.g., `target_coverage_comparison.png`).

### 3. Comparing Results
```bash
python drone_mesh_network/compare_simulations.py
```
- Creates comparison plots from the `.pkl` files.

---

## Dependencies
- Python 3.8+
- `matplotlib`
- `numpy`
- `pydantic`

### Install Dependencies:
```bash
pip install matplotlib numpy pydantic
```

---

## Usage
### Run Ant-Inspired Simulation:
```bash
python main.py
```
- Generates `ant_metrics.pkl` and displays the simulation.

### Run Hybrid Bee-Ant Simulation:
```bash
python hybrid_main.py
```
- Generates `hybrid_metrics.pkl` and displays the simulation.

### Compare Results:
```bash
python drone_mesh_network/compare_simulations.py
