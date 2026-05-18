# Safe Quadrotor Navigation with CBF-QP

This repository contains a ROS 2 Jazzy and Gazebo simulation package for a quadrotor drone. The project aims to implement a Control Barrier Function (CBF) and Quadratic Program (QP) based safety filter to guarantee collision-free autonomous navigation in a cluttered 3D environment.

## Current Capabilities
- Spawns a custom quadrotor with 6-DOF physics in a Gazebo world populated with cylindrical obstacles.
- GPU LiDAR integration streaming high-frequency range data (`/scan`) via `ros_gz_bridge`.
- Automated waypoint navigation system publishing velocity commands.
- Active safety monitoring node that tracks obstacle distance and triggers critical warnings when safe thresholds (1.5m) are breached.

## Prerequisites
- **OS:** Ubuntu 24.04 (or compatible)
- **ROS 2:** Jazzy Jalisco
- **Simulator:** Gazebo Harmonic (or current Gazebo Sim compatible with Jazzy)
- **Dependencies:** `ros-jazzy-ros-gz`, `sensor_msgs`, `geometry_msgs`, `nav_msgs`

## Build and Run Instructions

### 1. Environment Setup
If you are using Anaconda or VS Code Snaps, you must clear conflicting environment variables before compiling or running ROS 2 nodes. Run this in **every new terminal** you open:
```bash
conda deactivate
unset GTK_PATH
unset GIO_MODULE_DIR

2. Build the Workspace

Navigate to your ROS 2 workspace, build the package, and source the installation:
Bash

cd ~/drone_ws
colcon build --packages-select safe_quadrotor
source install/setup.bash

3. Launching the Simulation (Terminal 1)

Open a terminal, apply the environment setup steps above, and launch the Gazebo world and drone bridge:
Bash

source /opt/ros/jazzy/setup.bash
source ~/drone_ws/install/setup.bash
ros2 launch safe_quadrotor spawn_drone.launch.py

Leave this terminal running.
4. Run the Safety Monitor (Terminal 2)

Open a second terminal, apply the environment setup steps, and start the safety node. This node uses a Sensor Data QoS profile to read the Best Effort LiDAR stream.
Bash

source ~/drone_ws/install/setup.bash
ros2 run safe_quadrotor safety_monitor

You should see an active readout of the nearest obstacle distance.
5. Start the Waypoint Navigator (Terminal 3)

Open a third terminal, apply the environment setup steps, and command the drone to fly:
Bash

source ~/drone_ws/install/setup.bash
ros2 run safe_quadrotor waypoint_navigator

Watch the drone fly toward its target and monitor Terminal 2 for critical safety breach warnings!


---