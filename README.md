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

## Build and Run Instructions

### 1. Build the Workspace (System Python)
Ensure you are using the standard system Python to build the workspace to prevent ROS 2 metadata corruption.
```bash
cd ~/drone_ws
conda deactivate
source /opt/ros/jazzy/setup.bash
colcon build --packages-select safe_quadrotor --symlink-install

2. Launching the Simulation (Terminal 1)

Open a terminal and launch the Gazebo world and drone bridge natively:
Bash

cd ~/drone_ws
conda deactivate
source /opt/ros/jazzy/setup.bash
source install/setup.bash
ros2 launch safe_quadrotor spawn_drone.launch.py

(Note: Ignore any Gtk-Message warnings regarding canberra-gtk-module)
3. Run the Safety Monitor (Terminal 2)

Open a second terminal and start the safety node natively:
Bash

cd ~/drone_ws
conda deactivate
source /opt/ros/jazzy/setup.bash
source install/setup.bash
ros2 run safe_quadrotor safety_monitor

4. Start the CBF-QP Controller (Terminal 3)

Because the controller requires isolated math libraries (cvxpy), we execute the script directly from the source directory while activating the local virtual environment.
Bash

cd ~/drone_ws
conda deactivate
source /opt/ros/jazzy/setup.bash
source install/setup.bash

# Activate the virtual environment
source venv_robo/bin/activate

# Execute the controller directly
python3 src/safe_quadrotor/safe_quadrotor/cbf_qp_controller.py

Watch the drone fly toward its target, intelligently side-step obstacles to break deadlocks, and reach its goal safely!