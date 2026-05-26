#!/usr/bin/env bash
set -eo pipefail

cd "${HOME}/drone_ws"

# Match ~/.bashrc domain and keep all nodes discoverable
export ROS_DOMAIN_ID=10

conda deactivate 2>/dev/null || true
unset GTK_PATH GIO_MODULE_DIR

# Avoid accidentally inheriting overlays from other workspaces
unset AMENT_PREFIX_PATH COLCON_PREFIX_PATH CMAKE_PREFIX_PATH PYTHONPATH

source /opt/ros/jazzy/setup.bash
source install/setup.bash

# CBF-QP dependencies live here
source venv_robo/bin/activate

python3 src/safe_quadrotor/safe_quadrotor/cbf_qp_controller.py