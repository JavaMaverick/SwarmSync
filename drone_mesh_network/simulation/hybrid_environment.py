# drone_mesh_network/simulation/hybrid_environment.py

import random
from typing import Dict, List, Optional
import time
from concurrent.futures import ThreadPoolExecutor

from drone_mesh_network.core.hybrid_drone import HybridDrone, Position, Obstacle, Target

class HybridEnvironment:
    def __init__(self, 
                 width: float = 1000.0, 
                 height: float = 1000.0, 
                 depth: float = 100.0,
                 num_drones: int = 10,
                 num_obstacles: int = 20,
                 num_targets: int = 5):
        self.width = width
        self.height = height
        self.depth = depth
        self.time = 0.0
        
        # Create drones
        self.drones: Dict[str, HybridDrone] = {}
        for i in range(num_drones):
            drone = HybridDrone(position=Position(
                x=random.uniform(0, width),
                y=random.uniform(0, height),
                z=random.uniform(0, depth)
            ))
            self.drones[drone.id] = drone
            if i == 0:
                drone.is_leader = True
        
        # Create obstacles
        self.obstacles: List[Obstacle] = []
        for _ in range(num_obstacles):
            obstacle = Obstacle(
                id=f"obstacle_{len(self.obstacles)}",
                position=Position(
                    x=random.uniform(0, width),
                    y=random.uniform(0, height),
                    z=random.uniform(0, depth)
                ),
                radius=random.uniform(5, 20),
                detected_by="environment",
                timestamp=time.time()
            )
            self.obstacles.append(obstacle)
        
        # Create targets
        self.targets: List[Target] = []
        for _ in range(num_targets):
            target = Target(
                id=f"target_{len(self.targets)}",
                position=Position(
                    x=random.uniform(0, width),
                    y=random.uniform(0, height),
                    z=random.uniform(0, depth)
                ),
                priority=random.randint(1, 5),
                detected_by="environment",
                timestamp=time.time()
            )
            self.targets.append(target)
    
    def update(self, dt: float = 0.1):
        """Update the environment state."""
        self.time += dt
        
        def update_drone(drone):
            if drone.is_active:
                drone.update(dt, self.drones, self.obstacles, self.targets)
        
        with ThreadPoolExecutor() as executor:
            executor.map(update_drone, self.drones.values())
        
        if random.random() < 0.01:
            new_target = Target(
                id=f"target_{len(self.targets)}",
                position=Position(
                    x=random.uniform(0, self.width),
                    y=random.uniform(0, self.height),
                    z=random.uniform(0, self.depth)
                ),
                priority=random.randint(1, 5),
                detected_by="environment",
                timestamp=time.time()
            )
            self.targets.append(new_target)
            
        if self.targets and random.random() < 0.005:
            self.targets.pop(random.randint(0, len(self.targets) - 1))
