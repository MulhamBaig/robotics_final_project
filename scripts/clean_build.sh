#!/usr/bin/env bash
set -eo pipefail

cd "${HOME}/drone_ws"

# Ensure every terminal uses the same DDS domain
export ROS_DOMAIN_ID=10

# Stop here if user is running Gazebo/ROS in this shell.
# Clean colcon artifacts (most common source of stale worlds/launch files)
rm -rf build/ install/ log/

# Clean python caches in the source tree
find src -type d -name "__pycache__" -prune -exec rm -rf {} +
find src -type f -name "*.pyc" -delete

# Clean environment quirks
conda deactivate 2>/dev/null || true
unset GTK_PATH GIO_MODULE_DIR

# Avoid accidentally inheriting overlays from other workspaces
unset AMENT_PREFIX_PATH COLCON_PREFIX_PATH CMAKE_PREFIX_PATH PYTHONPATH

source /opt/ros/jazzy/setup.bash
colcon build --packages-select safe_quadrotor --symlink-install

echo "OK: build complete. Now run: source install/setup.bash"