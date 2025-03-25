# drone_mesh_network/visualization/visualizer.py

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
from typing import Dict, List

from drone_mesh_network.core.drone import Drone, Position, Obstacle, Target, PheromoneTrail
from drone_mesh_network.simulation.environment import Environment

class Visualizer:
    def __init__(self, environment: Environment):
        self.environment = environment
        
        # Set up the figure and axis
        self.fig = plt.figure(figsize=(12, 8))
        self.ax = self.fig.add_subplot(111, projection='3d')
        self.ax.set_xlim(0, environment.width)
        self.ax.set_ylim(0, environment.height)
        self.ax.set_zlim(0, environment.depth)
        self.ax.set_xlabel('X')
        self.ax.set_ylabel('Y')
        self.ax.set_zlabel('Z')
        self.ax.set_title('Drone Mesh Network Simulation')
        
        # Initialize plot elements
        self.drone_scatter = self.ax.scatter([], [], [], c='blue', marker='o', s=50, label='Drones')
        self.leader_scatter = self.ax.scatter([], [], [], c='yellow', marker='*', s=100, label='Leader')
        self.inactive_drone_scatter = self.ax.scatter([], [], [], c='gray', marker='x', s=50, label='Inactive Drones')
        self.obstacle_scatter = self.ax.scatter([], [], [], c='red', marker='s', s=100, label='Obstacles')
        self.target_scatter = self.ax.scatter([], [], [], c='green', marker='^', s=100, label='Targets')
        self.pheromone_scatter = self.ax.scatter([], [], [], c='purple', marker='.', s=20, label='Pheromone Trails')
        
        # Communication links
        self.comm_lines = []
        
        # Legend
        self.ax.legend()
        
        # Information text
        self.info_text = self.ax.text2D(0.02, 0.98, "", transform=self.ax.transAxes)
        
    def update_plot(self, frame):
        """Update the visualization for animation."""
        # Update the simulation
        self.environment.update(dt=0.1)
        
        # Clear old communication links
        for line in self.comm_lines:
            line.remove()
        self.comm_lines = []
        
        # Update drone positions (active, leader, and inactive)
        active_drones = [drone for drone in self.environment.drones.values() if drone.is_active and not drone.is_leader]
        leader_drones = [drone for drone in self.environment.drones.values() if drone.is_active and drone.is_leader]
        inactive_drones = [drone for drone in self.environment.drones.values() if not drone.is_active]
        
        # Active drones
        drone_positions = [drone.position for drone in active_drones]
        x = [pos.x for pos in drone_positions]
        y = [pos.y for pos in drone_positions]
        z = [pos.z for pos in drone_positions]
        self.drone_scatter._offsets3d = (x, y, z)
        
        # Leader drone
        leader_positions = [drone.position for drone in leader_drones]
        x = [pos.x for pos in leader_positions]
        y = [pos.y for pos in leader_positions]
        z = [pos.z for pos in leader_positions]
        self.leader_scatter._offsets3d = (x, y, z)
        
        # Inactive drones
        inactive_positions = [drone.position for drone in inactive_drones]
        x = [pos.x for pos in inactive_positions]
        y = [pos.y for pos in inactive_positions]
        z = [pos.z for pos in inactive_positions]
        self.inactive_drone_scatter._offsets3d = (x, y, z)
        
        # Update obstacle positions
        obstacle_positions = [obstacle.position for obstacle in self.environment.obstacles]
        x = [pos.x for pos in obstacle_positions]
        y = [pos.y for pos in obstacle_positions]
        z = [pos.z for pos in obstacle_positions]
        self.obstacle_scatter._offsets3d = (x, y, z)
        
        # Update target positions
        target_positions = [target.position for target in self.environment.targets]
        x = [pos.x for pos in target_positions]
        y = [pos.y for pos in target_positions]
        z = [pos.z for pos in target_positions]
        self.target_scatter._offsets3d = (x, y, z)
        
        # Update pheromone trails (deduplicate by target_id)
        all_trails = []
        seen_target_ids = set()
        for drone in self.environment.drones.values():
            for trail in drone.pheromone_trails:
                if trail.target_id and trail.target_id not in seen_target_ids:
                    all_trails.append(trail)
                    seen_target_ids.add(trail.target_id)
        trail_positions = [trail.position for trail in all_trails]
        x = [pos.x for pos in trail_positions]
        y = [pos.y for pos in trail_positions]
        z = [pos.z for pos in trail_positions]
        self.pheromone_scatter._offsets3d = (x, y, z)
        
        # Draw communication links
        for drone_id, drone in self.environment.drones.items():
            if not drone.is_active:
                continue
            for neighbor_id in drone.neighboring_drones:
                neighbor = self.environment.drones.get(neighbor_id)
                if neighbor and neighbor.is_active:
                    line = self.ax.plot([drone.position.x, neighbor.position.x],
                                       [drone.position.y, neighbor.position.y],
                                       [drone.position.z, neighbor.position.z],
                                       'k-', alpha=0.2)[0]
                    self.comm_lines.append(line)
        
        # Update information text
        detected_obstacles = sum(len(drone.known_obstacles) for drone in self.environment.drones.values())
        detected_targets = sum(len(drone.known_targets) for drone in self.environment.drones.values())
        active_drones_count = sum(1 for drone in self.environment.drones.values() if drone.is_active)
        info = f"Time: {self.environment.time:.1f}s\n"
        info += f"Active Drones: {active_drones_count}\n"
        info += f"Detected Obstacles: {detected_obstacles}\n"
        info += f"Detected Targets: {detected_targets}\n"
        info += f"Pheromone Trails: {len(all_trails)}"
        self.info_text.set_text(info)
        
        return (self.drone_scatter, self.leader_scatter, self.inactive_drone_scatter, 
                self.obstacle_scatter, self.target_scatter, self.pheromone_scatter, self.info_text)



# drone_mesh_network/visualization/visualizer.py

# ... (previous imports and code)

class Visualizer:
    def __init__(self, environment: Environment):
        self.environment = environment
        
        self.fig = plt.figure(figsize=(12, 8))
        self.ax = self.fig.add_subplot(111, projection='3d')
        self.ax.set_xlim(0, environment.width)
        self.ax.set_ylim(0, environment.height)
        self.ax.set_zlim(0, environment.depth)
        self.ax.set_xlabel('X')
        self.ax.set_ylabel('Y')
        self.ax.set_zlabel('Z')
        self.ax.set_title('Drone Mesh Network Simulation')
        
        self.drone_scatter = self.ax.scatter([], [], [], c='blue', marker='o', s=50, label='Drones')
        self.leader_scatter = self.ax.scatter([], [], [], c='yellow', marker='*', s=100, label='Leader')
        self.inactive_drone_scatter = self.ax.scatter([], [], [], c='gray', marker='x', s=50, label='Inactive Drones')
        self.obstacle_scatter = self.ax.scatter([], [], [], c='red', marker='s', s=100, label='Obstacles')
        self.target_scatter = self.ax.scatter([], [], [], c='green', marker='^', s=100, label='Targets')
        self.pheromone_scatter = self.ax.scatter([], [], [], c='purple', marker='.', s=20, label='Pheromone Trails')
        
        self.comm_lines = []
        self.ax.legend()
        self.info_text = self.ax.text2D(0.02, 0.98, "", transform=self.ax.transAxes)
        
        # Metrics for comparison
        self.target_coverage_history = []
        self.energy_efficiency_history = []
        self.network_connectivity_history = []

    def update_plot(self, frame):
        self.environment.update(dt=0.1)
        
        for line in self.comm_lines:
            line.remove()
        self.comm_lines = []
        
        active_drones = [drone for drone in self.environment.drones.values() if drone.is_active and not drone.is_leader]
        leader_drones = [drone for drone in self.environment.drones.values() if drone.is_active and drone.is_leader]
        inactive_drones = [drone for drone in self.environment.drones.values() if not drone.is_active]
        
        drone_positions = [drone.position for drone in active_drones]
        x = [pos.x for pos in drone_positions]
        y = [pos.y for pos in drone_positions]
        z = [pos.z for pos in drone_positions]
        self.drone_scatter._offsets3d = (x, y, z)
        
        leader_positions = [drone.position for drone in leader_drones]
        x = [pos.x for pos in leader_positions]
        y = [pos.y for pos in leader_positions]
        z = [pos.z for pos in leader_positions]
        self.leader_scatter._offsets3d = (x, y, z)
        
        inactive_positions = [drone.position for drone in inactive_drones]
        x = [pos.x for pos in inactive_positions]
        y = [pos.y for pos in inactive_positions]
        z = [pos.z for pos in inactive_positions]
        self.inactive_drone_scatter._offsets3d = (x, y, z)
        
        obstacle_positions = [obstacle.position for obstacle in self.environment.obstacles]
        x = [pos.x for pos in obstacle_positions]
        y = [pos.y for pos in obstacle_positions]
        z = [pos.z for pos in obstacle_positions]
        self.obstacle_scatter._offsets3d = (x, y, z)
        
        target_positions = [target.position for target in self.environment.targets]
        x = [pos.x for pos in target_positions]
        y = [pos.y for pos in target_positions]
        z = [pos.z for pos in target_positions]
        self.target_scatter._offsets3d = (x, y, z)
        
        all_trails = []
        seen_target_ids = set()
        for drone in self.environment.drones.values():
            for trail in drone.pheromone_trails:
                if trail.target_id and trail.target_id not in seen_target_ids:
                    all_trails.append(trail)
                    seen_target_ids.add(trail.target_id)
        trail_positions = [trail.position for trail in all_trails]
        x = [pos.x for pos in trail_positions]
        y = [pos.y for pos in trail_positions]
        z = [pos.z for pos in trail_positions]
        self.pheromone_scatter._offsets3d = (x, y, z)
        
        for drone_id, drone in self.environment.drones.items():
            if not drone.is_active:
                continue
            for neighbor_id in drone.neighboring_drones:
                neighbor = self.environment.drones.get(neighbor_id)
                if neighbor and neighbor.is_active:
                    line = self.ax.plot([drone.position.x, neighbor.position.x],
                                       [drone.position.y, neighbor.position.y],
                                       [drone.position.z, neighbor.position.z],
                                       'k-', alpha=0.2)[0]
                    self.comm_lines.append(line)
        
        # Calculate metrics
        detected_obstacles = sum(len(drone.known_obstacles) for drone in self.environment.drones.values())
        detected_targets = sum(len(drone.known_targets) for drone in self.environment.drones.values())
        active_drones_count = sum(1 for drone in self.environment.drones.values() if drone.is_active)
        total_battery = sum(drone.battery_level for drone in self.environment.drones.values())
        avg_battery = total_battery / len(self.environment.drones) if self.environment.drones else 0
        connectivity = sum(len(drone.neighboring_drones) for drone in self.environment.drones.values()) / 2
        
        self.target_coverage_history.append(detected_targets)
        self.energy_efficiency_history.append(avg_battery)
        self.network_connectivity_history.append(connectivity)
        
        info = f"Time: {self.environment.time:.1f}s\n"
        info += f"Active Drones: {active_drones_count}\n"
        info += f"Detected Obstacles: {detected_obstacles}\n"
        info += f"Detected Targets: {detected_targets}\n"
        info += f"Pheromone Trails: {len(all_trails)}"
        self.info_text.set_text(info)
        
        return (self.drone_scatter, self.leader_scatter, self.inactive_drone_scatter, 
                self.obstacle_scatter, self.target_scatter, self.pheromone_scatter, self.info_text)