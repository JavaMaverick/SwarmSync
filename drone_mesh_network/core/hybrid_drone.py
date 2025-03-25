# drone_mesh_network/core/hybrid_drone.py

import random
import time
import math
from typing import Dict, List, Optional, Set
from pydantic import BaseModel

from .drone import Drone, Position, Target, PheromoneTrail, Obstacle

class RecruitmentSignal(BaseModel):
    target_id: str
    position: Position
    strength: float
    timestamp: float
    priority: int

class HybridDrone(Drone):
    def __init__(self, drone_id: str = None, position: Position = None, communication_range: float = 100.0):
        super().__init__(drone_id, position, communication_range)
        self.is_scout = random.random() < 0.2  # 20% chance to be a scout
        self.recruitment_signals: List[RecruitmentSignal] = []
        self.assigned_target: Optional[str] = None  # Target the drone is recruited to

    def perform_waggle_dance(self, target: Target):
        """Simulate a bee-like waggle dance by broadcasting a recruitment signal."""
        if random.random() < 0.7:  # 70% chance to perform a "dance"
            signal = RecruitmentSignal(
                target_id=target.id,
                position=Position(x=self.position.x, y=self.position.y, z=self.position.z),
                strength=target.priority * 2.0,  # Strength scales with priority
                timestamp=time.time(),
                priority=target.priority
            )
            self.recruitment_signals.append(signal)
            if len(self.recruitment_signals) > 5:  # Limit signals to prevent overload
                self.recruitment_signals.pop(0)
        # Evaporate old signals
        self.recruitment_signals = [
            signal for signal in self.recruitment_signals
            if time.time() - signal.timestamp < 30  # Signals last 30 seconds
        ]

    def follow_recruitment_signal(self):
        """Move toward the strongest recruitment signal if not already assigned."""
        if self.assigned_target or not self.recruitment_signals:
            return
        strongest_signal = max(self.recruitment_signals, key=lambda s: s.strength)
        distance = self.position.distance_to(strongest_signal.position)
        if distance < 50:  # Only follow if within a certain range
            self.assigned_target = strongest_signal.target_id
            direction_x = strongest_signal.position.x - self.position.x
            direction_y = strongest_signal.position.y - self.position.y
            direction_z = strongest_signal.position.z - self.position.z
            magnitude = math.sqrt(direction_x**2 + direction_y**2 + direction_z**2)
            if magnitude > 0:
                self.velocity.x = (direction_x / magnitude) * 5
                self.velocity.y = (direction_y / magnitude) * 5
                self.velocity.z = (direction_z / magnitude) * 2
            self.limit_velocity()

    def scout_explore(self):
        """Scouts explore more aggressively by increasing velocity and range."""
        if self.is_scout and not self.assigned_target:
            self.velocity.x = random.uniform(-10, 10)
            self.velocity.y = random.uniform(-10, 10)
            self.velocity.z = random.uniform(-2, 2)
            self.limit_velocity(max_speed=15.0)  # Scouts move faster

    def optimize_energy(self, targets: List[Target]):
        """Prioritize targets based on distance and priority to conserve energy."""
        if not targets or self.assigned_target:
            return
        best_target = min(
            targets,
            key=lambda t: self.position.distance_to(t.position) / t.priority,
            default=None
        )
        if best_target:
            self.assigned_target = best_target.id
            direction_x = best_target.position.x - self.position.x
            direction_y = best_target.position.y - self.position.y
            direction_z = best_target.position.z - self.position.z
            magnitude = math.sqrt(direction_x**2 + direction_y**2 + direction_z**2)
            if magnitude > 0:
                self.velocity.x = (direction_x / magnitude) * 5
                self.velocity.y = (direction_y / magnitude) * 5
                self.velocity.z = (direction_z / magnitude) * 2
            self.limit_velocity()

    def detect_targets(self, targets: List[Target]):
        """Override to include waggle dance and energy optimization."""
        super().detect_targets(targets)
        for target in targets:
            if target.id in self.known_targets:
                self.perform_waggle_dance(target)
        self.optimize_energy(targets)

    def share_knowledge(self, drones: Dict[str, 'Drone']):
        """Override to share recruitment signals."""
        super().share_knowledge(drones)
        for neighbor_id in self.neighboring_drones:
            neighbor = drones.get(neighbor_id)
            if neighbor and neighbor.is_active:
                existing_signal_ids = {signal.target_id for signal in neighbor.recruitment_signals}
                for signal in self.recruitment_signals:
                    if signal.target_id not in existing_signal_ids:
                        neighbor.recruitment_signals.append(signal)
                        existing_signal_ids.add(signal.target_id)
                neighbor.recruitment_signals = [
                    signal for signal in neighbor.recruitment_signals
                    if time.time() - signal.timestamp < 30
                ]
                if len(neighbor.recruitment_signals) > 5:
                    neighbor.recruitment_signals = neighbor.recruitment_signals[-5:]

    def update(self, dt: float, drones: Dict[str, 'Drone'], obstacles: List['Obstacle'], targets: List[Target]):
        """Override to include hybrid behaviors."""
        if not self.is_active:
            return
        self.update_battery(dt)
        if not self.is_active:
            return
        self.detect_obstacles(obstacles)
        self.detect_targets(targets)
        self.sense_environment()
        self.discover_neighbors(list(drones.values()))
        self.share_knowledge(drones)
        self.follow_pheromone_trails()
        self.follow_recruitment_signal()
        self.scout_explore()
        self.predict_connectivity_loss(drones)
        self.self_heal_network(drones)
        self.avoid_obstacles()
        self.move(dt)

