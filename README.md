## Safe Quadrotor Navigation with CBF-QP

This repository contains a ROS 2 Jazzy and Gazebo simulation package for a quadrotor drone. The project implements a Control Barrier Function (CBF) and Quadratic Program (QP) based safety filter to guarantee collision-free autonomous navigation in a cluttered 3D environment, entirely eliminating potential field deadlocks.

## Current Capabilities
- Spawns a custom quadrotor with 6-DOF physics in a Gazebo world populated with cylindrical obstacles.
- GPU LiDAR integration streaming high-frequency range data (`/scan`) via `ros_gz_bridge`.
- **Advanced Navigation:** A real-time CBF-QP controller utilizing `cvxpy` to guarantee safety boundaries (1.5m).
- **Deadlock Resolution:** Features a custom Tangential Escape Vector algorithm that detects saddle-point deadlocks and injects lateral velocity to seamlessly bypass obstacles.
- Active safety monitoring node that tracks obstacle distance and verifies safe thresholds.

## Prerequisites
- **OS:** Ubuntu 24.04 (or compatible)
- **ROS 2:** Jazzy Jalisco
- **Simulator:** Gazebo Harmonic (or current Gazebo Sim compatible with Jazzy)
- **Python Dependencies:** `cvxpy`, `osqp` (Installed within a local virtual environment `venv_robo`)

## Video Demo Runbook (No-Missing-Steps)

This project uses **system ROS/Python** for Gazebo + ROS nodes, and uses the **local virtualenv** `venv_robo` only for the CBF-QP controller.

Important:
- Your machine exports `ROS_DOMAIN_ID=10` in `~/.bashrc`. All terminals must use the **same** ROS domain or nodes won’t see each other.
- The helper scripts below force `ROS_DOMAIN_ID=10` and also clear any accidentally-inherited overlays from other workspaces.

### 0) One-time setup
```bash
cd ~/drone_ws
chmod +x scripts/*.sh
```

### 1) Clean build (recommended before recording)
```bash
cd ~/drone_ws
./scripts/clean_build.sh
```

### 2) Run the 3 terminals (recommended)

Terminal 1 (Gazebo + spawn + bridge):
```bash
cd ~/drone_ws
./scripts/terminal1_sim.sh
```

Terminal 2 (Safety monitor):
```bash
cd ~/drone_ws
./scripts/terminal2_safety.sh
```

Terminal 3 (CBF-QP controller; uses `venv_robo`):
```bash
cd ~/drone_ws
./scripts/terminal3_controller.sh
```

### 3) Quick “is it working?” checks
Run these in any extra terminal (system ROS):
```bash
cd ~/drone_ws
source /opt/ros/jazzy/setup.bash
source install/setup.bash
export ROS_DOMAIN_ID=10

# Expect ~50 Hz
ros2 topic hz /model/simple_drone/odometry

# Expect ~10 Hz
ros2 topic hz /scan
```

### 4) Stop
In each terminal press `Ctrl+C`.

If Gazebo got stuck running in the background, you can stop it with:
```bash
pkill -f "gz sim" || true
```

## Verified Demo Run

- Date: 2026-05-26
- Status: End-to-end demo completed successfully on this machine. The drone navigated to the target, avoided obstacles, and reached the beacon while the safety monitor and CBF-QP controller ran concurrently.
- Notes: This run validated the DDS domain fix (`ROS_DOMAIN_ID=10`) and the venv split (controller runs inside `venv_robo`). See `mylogs.md` for details and the git commit that recorded these changes.

## Manual Commands (if you don’t want scripts)

### Clean build
```bash
cd ~/drone_ws

# Keep all terminals in the same DDS domain
export ROS_DOMAIN_ID=10

# If you use conda or any other venv, get out of it for building
conda deactivate 2>/dev/null || true
deactivate 2>/dev/null || true

# Avoid GUI/plugin env quirks
unset GTK_PATH GIO_MODULE_DIR

# Avoid inheriting overlays from other workspaces
unset AMENT_PREFIX_PATH COLCON_PREFIX_PATH CMAKE_PREFIX_PATH PYTHONPATH

rm -rf build/ install/ log/
find src -type d -name "__pycache__" -prune -exec rm -rf {} +
find src -type f -name "*.pyc" -delete

source /opt/ros/jazzy/setup.bash
colcon build --packages-select safe_quadrotor --symlink-install
```

### Terminal 1 (sim + spawn + bridge)
```bash
cd ~/drone_ws
export ROS_DOMAIN_ID=10
conda deactivate 2>/dev/null || true
deactivate 2>/dev/null || true
unset GTK_PATH GIO_MODULE_DIR
unset AMENT_PREFIX_PATH COLCON_PREFIX_PATH CMAKE_PREFIX_PATH PYTHONPATH
source /opt/ros/jazzy/setup.bash
source install/setup.bash
ros2 launch safe_quadrotor spawn_drone.launch.py
```

### Terminal 2 (safety)
```bash
cd ~/drone_ws
export ROS_DOMAIN_ID=10
conda deactivate 2>/dev/null || true
deactivate 2>/dev/null || true
unset GTK_PATH GIO_MODULE_DIR
unset AMENT_PREFIX_PATH COLCON_PREFIX_PATH CMAKE_PREFIX_PATH PYTHONPATH
source /opt/ros/jazzy/setup.bash
source install/setup.bash
ros2 run safe_quadrotor safety_monitor
```

### Terminal 3 (controller; venv only here)
```bash
cd ~/drone_ws
export ROS_DOMAIN_ID=10
conda deactivate 2>/dev/null || true
unset GTK_PATH GIO_MODULE_DIR
unset AMENT_PREFIX_PATH COLCON_PREFIX_PATH CMAKE_PREFIX_PATH PYTHONPATH
source /opt/ros/jazzy/setup.bash
source install/setup.bash

source venv_robo/bin/activate
python3 src/safe_quadrotor/safe_quadrotor/cbf_qp_controller.py
```