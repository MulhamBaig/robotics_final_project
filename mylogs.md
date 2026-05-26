# Project Plan & Development Logs

## 📊 Project Completion Dashboard

- [x] **Phase 1: Environment Setup & Spawning** (100%)
- [x] **Phase 2: Basic Flight & Environment** (100%)
- [x] **Phase 3: Sensor & Collision Detection** (100%)
- [ ] **Phase 4: Theoretical Modeling & Derivation** (0%)
- [x] **Phase 5: Advanced Control & CBF-QP Filter** (100%)
- [ ] **Phase 6: Evaluation & Academic Deliverables** (0%)

---

## 📝 Development Logs (Completed Work)

### [Completed] May 26, 2026: Stable “Video Demo” Runbook + Runtime Fix
- **Root cause of “topics exist but no messages / drone not moving”:** DDS discovery mismatch across terminals caused by inconsistent `ROS_DOMAIN_ID` usage.
	- `~/.bashrc` exports `ROS_DOMAIN_ID=10`, but some runs were started in shells/environments that didn’t match, so nodes couldn’t discover each other.
- **Secondary fix:** helper scripts originally used `set -u` (nounset), which can break `/opt/ros/jazzy/setup.bash` due to unset variables.
- **Solution implemented:** helper scripts now force `ROS_DOMAIN_ID=10`, clear inherited overlay env vars (e.g., from other workspaces), and avoid `set -u`.
- **Validated after fix (ROS-side):**
	- `/model/simple_drone/odometry` bridged at ~50 Hz
	- `/scan` bridged at ~10 Hz
	- controller subscribes to odometry and publishes `/model/simple_drone/cmd_vel`
- **Runbook:** documented in `README.md` with both script-based and manual commands.

### [Verified] May 26, 2026: Demo Run Success
- Verified an end-to-end demo run where the quadrotor navigated to the beacon and avoided obstacles using the CBF-QP controller.
- Confirmed ROS bridge rates: `/model/simple_drone/odometry` ~50 Hz, `/scan` ~10 Hz.
- Actions taken: updated helper scripts to enforce `ROS_DOMAIN_ID=10`, cleared overlay env vars, and avoided `set -u` in runner scripts.
- This commit contains the documentation and script hardening for repeatable demo recordings.

### [Completed] Phase 1: Environment Setup & Drone Spawning
- Initialized `~/drone_ws/src` and created the `safe_quadrotor` ROS 2 package.
- Built the URDF structure for the quadrotor (base_link, rotors).
- Successfully launched Gazebo Sim and spawned the drone model.

### [Completed] Phase 2: Basic Flight Control & Environment Building
- Created a 3D Gazebo world (`obstacle_world.sdf`) populated with two rigid cylindrical obstacles.
- Configured Gazebo physics plugins for velocity control and odometry.
- Wrote `waypoint_navigator.py` to command the drone from origin to `[3.0, 3.0, 2.0]`.

### [Completed] Phase 3: Sensor Integration & Collision Detection
- Added `<sensor name="gpu_lidar">` to the URDF. 
- Fixed URDF parsing bug by wrapping the sensor in a `<gazebo reference="base_link">` tag.
- Bridged the `/scan` topic from Gazebo to ROS 2.
- Wrote `safety_monitor.py` to listen to `/scan` and calculate nearest obstacle distances.
- Fixed a silent ROS 2 network failure by updating the Python subscriber to use `qos_profile_sensor_data` (Best Effort).
- **Result:** System successfully tracks flight and throws a `[WARN] CRITICAL SAFETY BREACH` precisely when the drone crosses the 1.5m threshold from `cylinder_1`. Baseline crash test achieved.

### [Completed] Phase 5: Advanced Control & CBF-QP Safety Filter Implementation
- Replaced the baseline waypoint navigator with a mathematically rigorous Control Barrier Function (CBF) and Quadratic Program (QP) controller.
- Integrated `cvxpy` and `OSQP` to solve the optimization problem at 20 Hz, dynamically restricting nominal control inputs (CLF) to maintain a 1.5m safe set boundary.
- **Critical Architecture Fix:** Resolved package metadata resolution errors by isolating the `cvxpy` dependency inside a virtual environment (`venv_robo`). The system now natively builds Gazebo/ROS nodes via system Python while allowing the QP controller to execute directly from source.
- **Critical Algorithmic Fix (Local Minima Deadlock):** Encountered an unstable equilibrium (saddle point) where the target vector perfectly opposed the CBF safety gradient, causing the drone to freeze for 60+ seconds. Engineered a permanent **Tangential Escape Vector (Vortex Field)**. The algorithm now monitors the dot product of the nominal and obstacle vectors; if they align perfectly, it instantly injects a 90-degree lateral force, forcing the drone to smoothly curve around the obstacle without delay.

---

## 🚀 The Master Plan (Upcoming Phases)

### Phase 4: Theoretical Modeling & Optimization Derivation
- **Goal:** Develop the complete mathematical framework required by the course guidelines.
- Derive the full 6-DOF nonlinear dynamic equations for the quadrotor system.
- Design the theoretical foundation for a cascaded controller using Control Lyapunov Functions (CLF).
- Formulate the Control Barrier Functions (CBF) and construct the Quadratic Program (QP) optimization objective.

### Phase 6: Performance Evaluation & Academic Deliverables
- **Goal:** Collect experimental data from the simulation and compile your final grading materials.
- Run comprehensive autonomous navigation profiles where the quadrotor successfully navigates the cluttered Gazebo space.
- Collect simulation data and plot your performance metrics (tracking error, rise time, settling time, and total control effort).
- Capture a high-quality screen recording of the simulation actively avoiding obstacles.
- Author the 10–15 page final report in the requested IEEE technical paper style.
- Organize the presentation materials to structurally defend the mathematical validity of your controller.