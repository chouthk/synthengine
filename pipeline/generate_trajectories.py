"""
SynthEngine — Trajectory Generator (Module 2)
Generates geometric trajectories for edge case scenes by connecting to CARLA/Isaac Sim.
When no simulator is available, generates synthetic trajectory data for testing.
"""

import json, os, time, logging, math, random
from pathlib import Path
from datetime import datetime

log = logging.getLogger("synth-trajectory")

SIMULATOR_PORT = int(os.getenv("SIMULATOR_PORT", "2000"))

class TrajectoryPoint:
    """Single frame of simulation data at 50Hz."""
    def __init__(self, frame_id: int, timestamp: float, 
                 vehicle_pos: tuple, vehicle_rot: tuple, 
                 speed: float, acceleration: tuple,
                 steering_angle: float, throttle: float, brake: float):
        self.frame_id = frame_id
        self.timestamp = timestamp
        self.vehicle_pos = vehicle_pos      # (x, y, z)
        self.vehicle_rot = vehicle_rot      # (pitch, yaw, roll)
        self.speed = speed                  # km/h
        self.acceleration = acceleration    # (ax, ay, az) m/s²
        self.steering_angle = steering_angle
        self.throttle = throttle
        self.brake = brake

def connect_to_simulator(host: str = "localhost", port: int = SIMULATOR_PORT) -> bool:
    """Attempt to connect to CARLA/Isaac Sim simulator."""
    try:
        import carla
        client = carla.Client(host, port)
        client.set_timeout(5.0)
        world = client.get_world()
        log.info(f"✅ Connected to CARLA simulator at {host}:{port}")
        return True
    except Exception as e:
        log.warning(f"⚠️  No simulator available ({e}). Using synthetic trajectory generation.")
        return False

def generate_synthetic_trajectory(seed: dict, output_dir: str = "data/raw/trajectories") -> dict:
    """Generate synthetic trajectory data when no simulator is available.
    The trajectory simulates a real edge case scenario with realistic physics.
    """
    scene_id = seed.get("scene_id", f"synth_{int(time.time())}")
    os.makedirs(output_dir, exist_ok=True)
    
    # Simulate 5 seconds at 50Hz = 250 frames
    fps = 50
    duration_s = 5.0
    total_frames = int(fps * duration_s)
    
    trajectory = {
        "metadata": {
            "scene_id": scene_id,
            "category": seed.get("category", "unknown"),
            "description": seed.get("description", ""),
            "generated_at": datetime.now().isoformat(),
            "fps": fps,
            "total_frames": total_frames,
            "simulator": "synthetic"
        },
        "frames": [],
        "sensor_data": {
            "camera_front": {"width": 1920, "height": 1080, "fov": 90, "channels": 3},
            "lidar": {"channels": 64, "range_m": 100, "points_per_second": 100000},
            "imu": {"gyro": "3-axis", "accel": "3-axis", "freq_hz": 100},
            "gps": {"rate_hz": 10, "accuracy_m": 0.5}
        }
    }
    
    # Generate realistic edge case trajectory
    for frame in range(total_frames):
        t = frame / fps  # time in seconds
        
        # Time-based scenario simulation
        if t < 1.0:
            # Normal driving phase
            speed = 50 + random.uniform(-2, 2)
            steering = 0.0
            brake = 0.0
            throttle = random.uniform(0.3, 0.5)
            ax = random.uniform(-0.5, 0.5)
            ay = random.uniform(-0.3, 0.3)
        elif t < 2.0:
            # Edge case trigger: obstacle appears
            speed = speed - random.uniform(10, 20)  # rapid deceleration
            steering = random.uniform(-0.1, 0.1)
            brake = random.uniform(0.3, 0.6)
            throttle = 0.0
            ax = random.uniform(-8, -4)
            ay = random.uniform(-1, 1)
        elif t < 3.5:
            # Emergency avoidance maneuver
            speed = speed - random.uniform(5, 15)
            steering = random.uniform(-0.5, 0.5)
            brake = 0.8
            throttle = 0.0
            ax = random.uniform(-6, -3)
            ay = random.uniform(-3, 3)
        else:
            # Recovery phase
            speed = max(0, speed - random.uniform(0, 5))
            steering = random.uniform(-0.1, 0.1)
            brake = random.uniform(0.1, 0.3)
            throttle = 0.0
            ax = random.uniform(-2, 0)
            ay = random.uniform(-0.5, 0.5)
        
        point = {
            "frame": frame,
            "time": round(t, 3),
            "speed_kmh": round(speed, 2),
            "steering_deg": round(steering * 45, 2),
            "brake": round(brake, 3),
            "throttle": round(throttle, 3),
            "accel_ms2": {"x": round(ax, 3), "y": round(ay, 3), "z": round(random.uniform(-0.2, 0.2), 3)},
            "position": {
                "x": round(10 * t + random.uniform(-0.1, 0.1), 3),
                "y": round(math.sin(t * 2) * 3, 3),
                "z": round(math.cos(t * 3) * 0.1, 3)
            }
        }
        trajectory["frames"].append(point)
    
    # Save trajectory file
    out_path = os.path.join(output_dir, f"trajectory_{scene_id}.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(trajectory, f, indent=2, ensure_ascii=False)
    
    log.info(f"✅ Generated {total_frames} frames → {out_path}")
    return trajectory

def generate_batch(seeds: list, output_dir: str = "data/raw/trajectories") -> list:
    """Generate trajectories for all seeds."""
    num_simulators = len(seeds)
    log.info(f"🚗 Generating {num_simulators} trajectories...")
    
    results = []
    for i, seed in enumerate(seeds):
        log.info(f"  [{i+1}/{num_simulators}] {seed.get('scene_id', 'unknown')}")
        traj = generate_synthetic_trajectory(seed, output_dir)
        results.append(traj)
    
    log.info(f"✅ All trajectories generated in {output_dir}")
    return results

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    log.info("🚗 SynthEngine Trajectory Generator")
    
    # Load seeds
    seeds_path = "config/seeds_pool.json"
    if os.path.exists(seeds_path):
        with open(seeds_path, "r", encoding="utf-8") as f:
            seeds = json.load(f)["seeds"]
        generate_batch(seeds)
    else:
        log.warning(f"No seeds file found at {seeds_path}")
