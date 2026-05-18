# Project Plan & Development Logs

## 📊 Project Completion Dashboard

- [x] **Phase 1: Environment Setup & Spawning** (100%)
- [x] **Phase 2: Basic Flight & Environment** (100%)
- [x] **Phase 3: Sensor & Collision Detection** (100%)
- [ ] **Phase 4: Theoretical Modeling & Derivation** (0%)
- [ ] **Phase 5: Advanced Control & CBF-QP Filter** (0%)
- [ ] **Phase 6: Evaluation & Academic Deliverables** (0%)

---

## 📝 Development Logs (Completed Work)

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

---

## 🚀 The Master Plan (Upcoming Phases)

### Phase 4: Theoretical Modeling & Optimization Derivation
- **Goal:** Develop the complete mathematical framework required by the course guidelines before implementing advanced control logic.
- Derive the full 6-DOF nonlinear dynamic equations for the quadrotor system.
- Design the theoretical foundation for a cascaded controller using Control Lyapunov Functions (CLF) to mathematically guarantee goal-reaching stability.
- Formulate the Control Barrier Functions (CBF) to define forward-invariant safe sets around your cylindrical obstacles.
- Construct the Quadratic Program (QP) optimization objective, setting up real-time cost functions.

### Phase 5: Advanced Control & CBF-QP Safety Filter Implementation
- **Goal:** Replace the baseline navigation scripts with your mathematically rigorous optimization controller.
- Code and execute the cascaded CLF tracking controller to manage the outer-loop position and inner-loop attitude stabilization.
- Implement the CBF safety filter logic to dynamically assess flight commands against the distance to obstacles.
- Integrate an optimization solver library (such as cvxpy or OSQP) into your ROS 2 node.
- Route the target tracking commands and safety constraints through the solver at each individual timestep.

### Phase 6: Performance Evaluation & Academic Deliverables
- **Goal:** Collect experimental data from the simulation and compile your final grading materials.
- Run comprehensive autonomous navigation profiles where the quadrotor successfully navigates the cluttered Gazebo space.
- Collect simulation data and plot your performance metrics (tracking error, rise time, settling time, and total control effort).
- Capture a high-quality screen recording of the simulation actively avoiding obstacles.
- Author the 10–15 page final report in the requested IEEE technical paper style.
- Organize the presentation materials to structurally defend the mathematical validity of your controller.