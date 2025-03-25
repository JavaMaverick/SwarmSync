# drone_mesh_network/core/drone.py

import uuid
import time
import math
import random
from typing import Dict, List, Tuple, Optional, Set
from pydantic import BaseModel

class Position(BaseModel):
    x: float
    y: float
    z: float
    
    def distance_to(self, other: 'Position') -> float:
        return math.sqrt(
            (self.x - other.x) ** 2 + 
            (self.y - other.y) ** 2 + 
            (self.z - other.z) ** 2
        )

class Obstacle(BaseModel):
    id: str
    position: Position
    radius: float
    detected_by: str
    timestamp: float

class Target(BaseModel):
    id: str
    position: Position
    priority: int
    detected_by: str
    timestamp: float

class EnvironmentalCondition(BaseModel):
    position: Position
    wind_speed: float
    wind_direction: float
    temperature: float
    humidity: float
    detected_by: str
    timestamp: float

class PheromoneTrail(BaseModel):
    position: Position
    strength: float
    timestamp: float
    target_id: Optional[str] = None  # Link to a specific target

class Drone:
    def __init__(self, 
                 drone_id: str = None, 
                 position: Position = None, 
                 communication_range: float = 100.0):
        self.id = drone_id or str(uuid.uuid4())
        self.position = position or Position(x=random.uniform(0, 1000), 
                                            y=random.uniform(0, 1000), 
                                            z=random.uniform(0, 100))
        self.communication_range = communication_range
        
        # Local knowledge base
        self.known_obstacles: Dict[str, Obstacle] = {}
        self.known_targets: Dict[str, Target] = {}
        self.environmental_conditions: List[EnvironmentalCondition] = []
        self.neighboring_drones: Set[str] = set()
        self.pheromone_trails: List[PheromoneTrail] = []
        self.laid_trails_for_targets: Set[str] = set()  # Track targets for which trails have been laid
        
        # Velocity and direction
        self.velocity = Position(x=random.uniform(-5, 5), 
                                y=random.uniform(-5, 5), 
                                z=random.uniform(-1, 1))
        
        # Battery and health
        self.battery_level = 100.0
        self.battery_drain_rate = 0.1
        self.is_active = True
        
        # Leader status
        self.is_leader = False

    def lay_pheromone_trail(self, target: Target):
        """Lay a pheromone trail to guide mesh formation toward a target."""
        # Only lay a trail if we haven't already for this target
        if target.id not in self.laid_trails_for_targets and random.random() < 0.5:
            trail = PheromoneTrail(
                position=Position(x=self.position.x, y=self.position.y, z=self.position.z),
                strength=1.0 * target.priority,
                timestamp=time.time(),
                target_id=target.id
            )
            self.pheromone_trails.append(trail)
            self.laid_trails_for_targets.add(target.id)
            # Limit the number of trails per drone to prevent memory overload
            if len(self.pheromone_trails) > 10:  # Max 10 trails per drone
                self.pheromone_trails.pop(0)
        # Evaporate old trails
        self.pheromone_trails = [
            trail for trail in self.pheromone_trails
            if time.time() - trail.timestamp < 60
        ]

    def follow_pheromone_trails(self):
        """Move toward the strongest pheromone trail to form mesh around targets."""
        if not self.pheromone_trails:
            return
        strongest_trail = max(self.pheromone_trails, key=lambda t: t.strength)
        direction_x = strongest_trail.position.x - self.position.x
        direction_y = strongest_trail.position.y - self.position.y
        direction_z = strongest_trail.position.z - self.position.z
        magnitude = math.sqrt(direction_x**2 + direction_y**2 + direction_z**2)
        if magnitude > 0:
            self.velocity.x = (direction_x / magnitude) * 5
            self.velocity.y = (direction_y / magnitude) * 5
            self.velocity.z = (direction_z / magnitude) * 2
        self.limit_velocity()

    def predict_connectivity_loss(self, drones: Dict[str, 'Drone']):
        """Predict potential connectivity loss based on distance and battery levels."""
        for neighbor_id in self.neighboring_drones:
            neighbor = drones.get(neighbor_id)
            if not neighbor or not neighbor.is_active:
                continue
            distance = self.position.distance_to(neighbor.position)
            if distance > 0.8 * self.communication_range or neighbor.battery_level < 20:
                direction_x = neighbor.position.x - self.position.x
                direction_y = neighbor.position.y - self.position.y
                direction_z = neighbor.position.z - self.position.z
                magnitude = math.sqrt(direction_x**2 + direction_y**2 + direction_z**2)
                if magnitude > 0:
                    self.velocity.x += (direction_x / magnitude) * 3
                    self.velocity.y += (direction_y / magnitude) * 3
                    self.velocity.z += (direction_z / magnitude) * 1
                self.limit_velocity()

    def self_heal_network(self, drones: Dict[str, 'Drone']):
        """Reconfigure the network if a drone fails."""
        if not self.is_active:
            return
        failed_neighbors = [nid for nid in self.neighboring_drones if not drones.get(nid) or not drones[nid].is_active]
        if failed_neighbors:
            self.neighboring_drones.difference_update(failed_neighbors)
            if self.is_leader and not self.is_active:
                self.is_leader = False
            if not any(drone.is_leader for drone in drones.values() if drone.is_active):
                self.is_leader = True
            if self.neighboring_drones:
                avg_position = Position(x=0, y=0, z=0)
                count = 0
                for nid in self.neighboring_drones:
                    neighbor = drones.get(nid)
                    if neighbor and neighbor.is_active:
                        avg_position.x += neighbor.position.x
                        avg_position.y += neighbor.position.y
                        avg_position.z += neighbor.position.z
                        count += 1
                if count > 0:
                    avg_position.x /= count
                    avg_position.y /= count
                    avg_position.z /= count
                    direction_x = avg_position.x - self.position.x
                    direction_y = avg_position.y - self.position.y
                    direction_z = avg_position.z - self.position.z
                    magnitude = math.sqrt(direction_x**2 + direction_y**2 + direction_z**2)
                    if magnitude > 0:
                        self.velocity.x += (direction_x / magnitude) * 2
                        self.velocity.y += (direction_y / magnitude) * 2
                        self.velocity.z += (direction_z / magnitude) * 1
                    self.limit_velocity()

    def move(self, dt: float = 0.1):
        """Move the drone based on its current velocity."""
        if not self.is_active:
            return
        self.position.x += self.velocity.x * dt
        self.position.y += self.velocity.y * dt
        self.position.z += self.velocity.z * dt
        self.position.x = max(0, min(1000, self.position.x))
        self.position.y = max(0, min(1000, self.position.y))
        self.position.z = max(0, min(100, self.position.z))
        
    def detect_obstacles(self, obstacles: List[Obstacle]):
        """Detect obstacles within sensor range."""
        sensor_range = 50.0
        for obstacle in obstacles:
            if self.position.distance_to(obstacle.position) <= sensor_range:
                new_obstacle = Obstacle(
                    id=obstacle.id,
                    position=obstacle.position,
                    radius=obstacle.radius,
                    detected_by=self.id,
                    timestamp=time.time()
                )
                self.known_obstacles[obstacle.id] = new_obstacle
                
    def detect_targets(self, targets: List[Target]):
        """Detect targets within sensor range."""
        sensor_range = 75.0
        for target in targets:
            if self.position.distance_to(target.position) <= sensor_range:
                new_target = Target(
                    id=target.id,
                    position=target.position,
                    priority=target.priority,
                    detected_by=self.id,
                    timestamp=time.time()
                )
                self.known_targets[target.id] = new_target
                self.lay_pheromone_trail(target)
                
    def sense_environment(self):
        """Sense environmental conditions at current position."""
        condition = EnvironmentalCondition(
            position=self.position,
            wind_speed=random.uniform(0, 10),
            wind_direction=random.uniform(0, 360),
            temperature=random.uniform(15, 35),
            humidity=random.uniform(20, 80),
            detected_by=self.id,
            timestamp=time.time()
        )
        self.environmental_conditions.append(condition)
        if len(self.environmental_conditions) > 10:
            self.environmental_conditions.pop(0)
        
    def discover_neighbors(self, drones: List['Drone']):
        """Discover neighboring drones within communication range."""
        self.neighboring_drones.clear()
        for drone in drones:
            if drone.id != self.id and self.position.distance_to(drone.position) <= self.communication_range and drone.is_active:
                self.neighboring_drones.add(drone.id)
                
    def share_knowledge(self, drones: Dict[str, 'Drone']):
        """Share knowledge with neighboring drones."""
        for neighbor_id in self.neighboring_drones:
            neighbor = drones.get(neighbor_id)
            if neighbor and neighbor.is_active:
                # Share obstacles
                for obstacle_id, obstacle in self.known_obstacles.items():
                    if obstacle_id not in neighbor.known_obstacles:
                        neighbor.known_obstacles[obstacle_id] = obstacle
                    elif neighbor.known_obstacles[obstacle_id].timestamp < obstacle.timestamp:
                        neighbor.known_obstacles[obstacle_id] = obstacle
                
                # Share targets
                for target_id, target in self.known_targets.items():
                    if target_id not in neighbor.known_targets:
                        neighbor.known_targets[target_id] = target
                    elif neighbor.known_targets[target_id].timestamp < target.timestamp:
                        neighbor.known_targets[target_id] = target
                
                # Share pheromone trails, but only if not already known
                existing_trail_ids = {trail.target_id for trail in neighbor.pheromone_trails if trail.target_id}
                for trail in self.pheromone_trails:
                    if trail.target_id and trail.target_id not in existing_trail_ids:
                        neighbor.pheromone_trails.append(trail)
                        existing_trail_ids.add(trail.target_id)
                # Evaporate trails in neighbor's list
                neighbor.pheromone_trails = [
                    trail for trail in neighbor.pheromone_trails
                    if time.time() - trail.timestamp < 60
                ]
                # Limit neighbor's trails
                if len(neighbor.pheromone_trails) > 10:
                    neighbor.pheromone_trails = neighbor.pheromone_trails[-10:]
                
                # Share environmental conditions
                if self.environmental_conditions:
                    latest_condition = self.environmental_conditions[-1]
                    neighbor.environmental_conditions.append(latest_condition)
                    if len(neighbor.environmental_conditions) > 10:
                        neighbor.environmental_conditions.pop(0)
    
    def avoid_obstacles(self):
        """Simple obstacle avoidance behavior."""
        for obstacle in self.known_obstacles.values():
            distance = self.position.distance_to(obstacle.position)
            if distance < obstacle.radius + 10:
                direction_x = self.position.x - obstacle.position.x
                direction_y = self.position.y - obstacle.position.y
                direction_z = self.position.z - obstacle.position.z
                magnitude = math.sqrt(direction_x**2 + direction_y**2 + direction_z**2)
                if magnitude > 0:
                    direction_x /= magnitude
                    direction_y /= magnitude
                    direction_z /= magnitude
                self.velocity.x += direction_x * 2
                self.velocity.y += direction_y * 2
                self.velocity.z += direction_z * 2
                self.limit_velocity()
    
    def limit_velocity(self, max_speed: float = 10.0):
        """Limit the drone's velocity to a maximum speed."""
        speed = math.sqrt(self.velocity.x**2 + self.velocity.y**2 + self.velocity.z**2)
        if speed > max_speed:
            self.velocity.x = (self.velocity.x / speed) * max_speed
            self.velocity.y = (self.velocity.y / speed) * max_speed
            self.velocity.z = (self.velocity.z / speed) * max_speed
    
    def update_battery(self, dt: float):
        """Update battery level and deactivate drone if battery is depleted."""
        self.battery_level -= self.battery_drain_rate * dt
        if self.battery_level <= 0:
            self.is_active = False
            self.velocity = Position(x=0, y=0, z=0)

    def update(self, dt: float, drones: Dict[str, 'Drone'], obstacles: List[Obstacle], targets: List[Target]):
        """Update the drone's state."""
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
        self.predict_connectivity_loss(drones)
        self.self_heal_network(drones)
        self.avoid_obstacles()
        self.move(dt)
