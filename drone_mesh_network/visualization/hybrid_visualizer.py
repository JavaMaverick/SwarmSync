# # drone_mesh_network/visualization/hybrid_visualizer.py

# import matplotlib.pyplot as plt
# from matplotlib.animation import FuncAnimation
# import numpy as np
# from typing import Dict, List

# from drone_mesh_network.core.hybrid_drone import HybridDrone, Position, Obstacle, Target, PheromoneTrail, RecruitmentSignal
# from drone_mesh_network.simulation.hybrid_environment import HybridEnvironment

# class HybridVisualizer:
#     def __init__(self, environment: HybridEnvironment):
#         self.environment = environment
        
#         self.fig = plt.figure(figsize=(12, 8))
#         self.ax = self.fig.add_subplot(111, projection='3d')
#         self.ax.set_xlim(0, environment.width)
#         self.ax.set_ylim(0, environment.height)
#         self.ax.set_zlim(0, environment.depth)
#         self.ax.set_xlabel('X')
#         self.ax.set_ylabel('Y')
#         self.ax.set_zlabel('Z')
#         self.ax.set_title('Hybrid Drone Mesh Network Simulation')
        
#         self.drone_scatter = self.ax.scatter([], [], [], c='blue', marker='o', s=50, label='Drones')
#         self.scout_scatter = self.ax.scatter([], [], [], c='cyan', marker='o', s=50, label='Scouts')
#         self.leader_scatter = self.ax.scatter([], [], [], c='yellow', marker='*', s=100, label='Leader')
#         self.inactive_drone_scatter = self.ax.scatter([], [], [], c='gray', marker='x', s=50, label='Inactive Drones')
#         self.obstacle_scatter = self.ax.scatter([], [], [], c='red', marker='s', s=100, label='Obstacles')
#         self.target_scatter = self.ax.scatter([], [], [], c='green', marker='^', s=100, label='Targets')
#         self.pheromone_scatter = self.ax.scatter([], [], [], c='purple', marker='.', s=20, label='Pheromone Trails')
#         self.recruitment_scatter = self.ax.scatter([], [], [], c='orange', marker='*', s=30, label='Recruitment Signals')
        
#         self.comm_lines = []
#         self.ax.legend()
#         self.info_text = self.ax.text2D(0.02, 0.98, "", transform=self.ax.transAxes)
        
#         # Metrics for comparison
#         self.target_coverage_history = []
#         self.energy_efficiency_history = []
#         self.network_connectivity_history = []

#     def update_plot(self, frame):
#         self.environment.update(dt=0.1)
        
#         for line in self.comm_lines:
#             line.remove()
#         self.comm_lines = []
        
#         active_drones = [drone for drone in self.environment.drones.values() if drone.is_active and not drone.is_leader and not drone.is_scout]
#         scout_drones = [drone for drone in self.environment.drones.values() if drone.is_active and drone.is_scout]
#         leader_drones = [drone for drone in self.environment.drones.values() if drone.is_active and drone.is_leader]
#         inactive_drones = [drone for drone in self.environment.drones.values() if not drone.is_active]
        
#         # Active drones
#         drone_positions = [drone.position for drone in active_drones]
#         x = [pos.x for pos in drone_positions]
#         y = [pos.y for pos in drone_positions]
#         z = [pos.z for pos in drone_positions]
#         self.drone_scatter._offsets3d = (x, y, z)
        
#         # Scout drones
#         scout_positions = [drone.position for drone in scout_drones]
#         x = [pos.x for pos in scout_positions]
#         y = [pos.y for pos in scout_positions]
#         z = [pos.z for pos in scout_positions]
#         self.scout_scatter._offsets3d = (x, y, z)
        
#         # Leader drone
#         leader_positions = [drone.position for drone in leader_drones]
#         x = [pos.x for pos in leader_positions]
#         y = [pos.y for pos in leader_positions]
#         z = [pos.z for pos in leader_positions]
#         self.leader_scatter._offsets3d = (x, y, z)
        
#         # Inactive drones
#         inactive_positions = [drone.position for drone in inactive_drones]
#         x = [pos.x for pos in inactive_positions]
#         y = [pos.y for pos in inactive_positions]
#         z = [pos.z for pos in inactive_positions]
#         self.inactive_drone_scatter._offsets3d = (x, y, z)
        
#         # Update obstacle positions
#         obstacle_positions = [obstacle.position for obstacle in self.environment.obstacles]
#         x = [pos.x for pos in obstacle_positions]
#         y = [pos.y for pos in obstacle_positions]
#         z = [pos.z for pos in obstacle_positions]
#         self.obstacle_scatter._offsets3d = (x, y, z)
        
#         # Update target positions
#         target_positions = [target.position for target in self.environment.targets]
#         x = [pos.x for pos in target_positions]
#         y = [pos.y for pos in target_positions]
#         z = [pos.z for pos in target_positions]
#         self.target_scatter._offsets3d = (x, y, z)
        
#         # Update pheromone trails
#         all_trails = []
#         seen_target_ids = set()
#         for drone in self.environment.drones.values():
#             for trail in drone.pheromone_trails:
#                 if trail.target_id and trail.target_id not in seen_target_ids:
#                     all_trails.append(trail)
#                     seen_target_ids.add(trail.target_id)
#         trail_positions = [trail.position for trail in all_trails]
#         x = [pos.x for pos in trail_positions]
#         y = [pos.y for pos in trail_positions]
#         z = [pos.z for pos in trail_positions]
#         self.pheromone_scatter._offsets3d = (x, y, z)
        
#         # Update recruitment signals
#         all_signals = []
#         seen_signal_ids = set()
#         for drone in self.environment.drones.values():
#             for signal in drone.recruitment_signals:
#                 if signal.target_id and signal.target_id not in seen_signal_ids:
#                     all_signals.append(signal)
#                     seen_signal_ids.add(signal.target_id)
#         signal_positions = [signal.position for signal in all_signals]
#         x = [pos.x for pos in signal_positions]
#         y = [pos.y for pos in signal_positions]
#         z = [pos.z for pos in signal_positions]
#         self.recruitment_scatter._offsets3d = (x, y, z)
        
#         # Draw communication links
#         for drone_id, drone in self.environment.drones.items():
#             if not drone.is_active:
#                 continue
#             for neighbor_id in drone.neighboring_drones:
#                 neighbor = self.environment.drones.get(neighbor_id)
#                 if neighbor and neighbor.is_active:
#                     line = self.ax.plot([drone.position.x, neighbor.position.x],
#                                        [drone.position.y, neighbor.position.y],
#                                        [drone.position.z, neighbor.position.z],
#                                        'k-', alpha=0.2)[0]
#                     self.comm_lines.append(line)
        
#         # Calculate metrics
#         detected_obstacles = sum(len(drone.known_obstacles) for drone in self.environment.drones.values())
#         detected_targets = sum(len(drone.known_targets) for drone in self.environment.drones.values())
#         active_drones_count = sum(1 for drone in self.environment.drones.values() if drone.is_active)
#         total_battery = sum(drone.battery_level for drone in self.environment.drones.values())
#         avg_battery = total_battery / len(self.environment.drones) if self.environment.drones else 0
#         connectivity = sum(len(drone.neighboring_drones) for drone in self.environment.drones.values()) / 2
        
#         self.target_coverage_history.append(detected_targets)
#         self.energy_efficiency_history.append(avg_battery)
#         self.network_connectivity_history.append(connectivity)
        
#         # Update information text
#         info = f"Time: {self.environment.time:.1f}s\n"
#         info += f"Active Drones: {active_drones_count}\n"
#         info += f"Detected Obstacles: {detected_obstacles}\n"
#         info += f"Detected Targets: {detected_targets}\n"
#         info += f"Pheromone Trails: {len(all_trails)}\n"
#         info += f"Recruitment Signals: {len(all_signals)}"
#         self.info_text.set_text(info)
        
#         return (self.drone_scatter, self.scout_scatter, self.leader_scatter, self.inactive_drone_scatter, 
#                 self.obstacle_scatter, self.target_scatter, self.pheromone_scatter, self.recruitment_scatter, self.info_text)









import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
import time
from typing import Dict, List

from drone_mesh_network.core.hybrid_drone import HybridDrone, Position, Obstacle, Target, PheromoneTrail, RecruitmentSignal
from drone_mesh_network.simulation.hybrid_environment import HybridEnvironment

class HybridVisualizer:
    def __init__(self, environment: HybridEnvironment):
        self.environment = environment
        
        self.fig = plt.figure(figsize=(12, 8))
        self.ax = self.fig.add_subplot(111, projection='3d')
        self.ax.set_xlim(0, environment.width)
        self.ax.set_ylim(0, environment.height)
        self.ax.set_zlim(0, environment.depth)
        self.ax.set_xlabel('X')
        self.ax.set_ylabel('Y')
        self.ax.set_zlabel('Z')
        self.ax.set_title('Hybrid Drone Mesh Network Simulation (Bee-Ant Inspired)')
        
        self.drone_scatter = self.ax.scatter([], [], [], c='blue', marker='o', s=50, label='Drones')
        self.scout_scatter = self.ax.scatter([], [], [], c='cyan', marker='o', s=50, label='Scouts')
        self.leader_scatter = self.ax.scatter([], [], [], c='yellow', marker='*', s=100, label='Leader')
        self.inactive_drone_scatter = self.ax.scatter([], [], [], c='gray', marker='x', s=50, label='Inactive Drones')
        self.obstacle_scatter = self.ax.scatter([], [], [], c='red', marker='s', s=100, label='Obstacles')
        self.target_scatter = self.ax.scatter([], [], [], c='green', marker='^', s=100, label='Targets')
        self.pheromone_scatter = self.ax.scatter([], [], [], c='purple', marker='.', s=20, label='Pheromone Trails')
        self.recruitment_scatter = self.ax.scatter([], [], [], c='orange', marker='*', s=30, label='Recruitment Signals')
        
        self.comm_lines = []
        self.ax.legend()
        self.info_text = self.ax.text2D(0.02, 0.98, "", transform=self.ax.transAxes)
        
        # Metrics for comparison
        self.target_coverage_history = []
        self.energy_efficiency_history = []
        self.network_connectivity_history = []
        self.swarm_cohesion_history = []
        self.target_latency_history = []
        self.fdr_history = []
        self.ptd_history = []
        self.oasr_history = []

    def update_plot(self, frame):
        """Update the visualization for animation."""
        self.environment.update(dt=0.1)
        
        for line in self.comm_lines:
            line.remove()
        self.comm_lines = []
        
        active_drones = [drone for drone in self.environment.drones.values() if drone.is_active and not drone.is_leader and not drone.is_scout]
        scout_drones = [drone for drone in self.environment.drones.values() if drone.is_active and drone.is_scout]
        leader_drones = [drone for drone in self.environment.drones.values() if drone.is_active and drone.is_leader]
        inactive_drones = [drone for drone in self.environment.drones.values() if not drone.is_active]
        
        # Active drones
        drone_positions = [drone.position for drone in active_drones]
        x = [pos.x for pos in drone_positions]
        y = [pos.y for pos in drone_positions]
        z = [pos.z for pos in drone_positions]
        self.drone_scatter._offsets3d = (x, y, z)
        
        # Scout drones
        scout_positions = [drone.position for drone in scout_drones]
        x = [pos.x for pos in scout_positions]
        y = [pos.y for pos in scout_positions]
        z = [pos.z for pos in scout_positions]
        self.scout_scatter._offsets3d = (x, y, z)
        
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
        
        # Update pheromone trails
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
        
        # Update recruitment signals
        all_signals = []
        seen_signal_ids = set()
        for drone in self.environment.drones.values():
            for signal in drone.recruitment_signals:
                if signal.target_id and signal.target_id not in seen_signal_ids:
                    all_signals.append(signal)
                    seen_signal_ids.add(signal.target_id)
        signal_positions = [signal.position for signal in all_signals]
        x = [pos.x for pos in signal_positions]
        y = [pos.y for pos in signal_positions]
        z = [pos.z for pos in signal_positions]
        self.recruitment_scatter._offsets3d = (x, y, z)
        
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
        
        # Calculate existing metrics
        detected_obstacles = sum(len(drone.known_obstacles) for drone in self.environment.drones.values())
        detected_targets = sum(len(drone.known_targets) for drone in self.environment.drones.values())
        active_drones_count = sum(1 for drone in self.environment.drones.values() if drone.is_active)
        total_battery = sum(drone.battery_level for drone in self.environment.drones.values())
        avg_battery = total_battery / len(self.environment.drones) if self.environment.drones else 0
        connectivity = sum(len(drone.neighboring_drones) for drone in self.environment.drones.values()) / 2
        
        # New metrics
        # Swarm Cohesion: Average distance to centroid
        if active_drones_count > 0:
            centroid = Position(
                x=sum(d.position.x for d in self.environment.drones.values() if d.is_active) / active_drones_count,
                y=sum(d.position.y for d in self.environment.drones.values() if d.is_active) / active_drones_count,
                z=sum(d.position.z for d in self.environment.drones.values() if d.is_active) / active_drones_count
            )
            cohesion = sum(d.position.distance_to(centroid) for d in self.environment.drones.values() if d.is_active) / active_drones_count
        else:
            cohesion = 0.0
        
        # Target Detection Latency: Average time to detect targets
        total_latency = 0
        detected_count = 0
        for drone in self.environment.drones.values():
            for target_id, target in drone.known_targets.items():
                latency = target.timestamp - next((t.timestamp for t in self.environment.targets if t.id == target_id), target.timestamp)
                total_latency += latency if latency > 0 else 0
                detected_count += 1
        avg_latency = total_latency / detected_count if detected_count > 0 else 0
        
        # Foreign Detection Rate: % of new targets detected within 10s
        recent_targets = [t for t in self.environment.targets if time.time() - t.timestamp < 10]
        detected_recent = sum(1 for t in recent_targets if any(t.id in d.known_targets for d in self.environment.drones.values()))
        fdr = (detected_recent / len(recent_targets)) * 100 if recent_targets else 0
        
        # Pheromone Trail Density: Trails per target
        ptd = len(all_trails) / len(self.environment.targets) if self.environment.targets else 0
        
        # Obstacle Avoidance Success Rate
        total_attempts = sum(getattr(drone, 'obstacle_avoidance_attempts', 0) 
                            for drone in self.environment.drones.values())
        total_success = sum(getattr(drone, 'obstacle_avoidance_success', 0) 
                           for drone in self.environment.drones.values())
        oasr = (total_success / total_attempts) * 100 if total_attempts > 0 else 0
        
        # Store metrics
        self.target_coverage_history.append(detected_targets)
        self.energy_efficiency_history.append(avg_battery)
        self.network_connectivity_history.append(connectivity)
        self.swarm_cohesion_history.append(cohesion)
        self.target_latency_history.append(avg_latency)
        self.fdr_history.append(fdr)
        self.ptd_history.append(ptd)
        self.oasr_history.append(oasr)
        
        # Update information text
        info = f"Time: {self.environment.time:.1f}s\n"
        info += f"Active Drones: {active_drones_count}\n"
        info += f"Detected Obstacles: {detected_obstacles}\n"
        info += f"Detected Targets: {detected_targets}\n"
        info += f"Pheromone Trails: {len(all_trails)}\n"
        info += f"Recruitment Signals: {len(all_signals)}\n"
        info += f"Cohesion: {cohesion:.2f}\n"
        info += f"Latency: {avg_latency:.2f}s\n"
        info += f"FDR: {fdr:.1f}%\n"
        info += f"PTD: {ptd:.2f}\n"
        info += f"OASR: {oasr:.1f}%"
        self.info_text.set_text(info)
        
        return (self.drone_scatter, self.scout_scatter, self.leader_scatter, self.inactive_drone_scatter, 
                self.obstacle_scatter, self.target_scatter, self.pheromone_scatter, self.recruitment_scatter, self.info_text)
