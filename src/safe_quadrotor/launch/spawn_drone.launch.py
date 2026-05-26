import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node

def generate_launch_description():
    pkg_safe_quadrotor = get_package_share_directory('safe_quadrotor')
    pkg_ros_gz_sim = get_package_share_directory('ros_gz_sim')

    urdf_model_path = os.path.join(pkg_safe_quadrotor, 'models', 'drone.urdf')
    # ADD THE PATH TO YOUR NEW WORLD:
    world_file_path = os.path.join(pkg_safe_quadrotor, 'worlds', 'obstacle_world.sdf')

    # 1. Launch Gazebo with YOUR specific world instead of empty.sdf
    gazebo_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_ros_gz_sim, 'launch', 'gz_sim.launch.py')
        ),
        # PASS THE WORLD FILE PATH HERE:
        launch_arguments={'gz_args': f'-r {world_file_path}'}.items(),
    )

    # 2. Spawn the URDF Drone Model
    spawn_drone_node = Node(
        package='ros_gz_sim',
        executable='create',
        arguments=[
            '-name', 'simple_drone',
            '-file', urdf_model_path,
            '-x', '0.0',
            '-y', '0.0',
            '-z', '0.5'
        ],
        output='screen'
    )

    # 3. Network Bridge: Maps control and odometry topics across networks
    ros_gz_bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        arguments=[
            '/model/simple_drone/cmd_vel@geometry_msgs/msg/Twist@gz.msgs.Twist',
            '/model/simple_drone/odometry@nav_msgs/msg/Odometry@gz.msgs.Odometry',
            '/scan@sensor_msgs/msg/LaserScan@gz.msgs.LaserScan'
        ],
        output='screen'
    )

    return LaunchDescription([
        gazebo_launch,
        spawn_drone_node,
        ros_gz_bridge
    ])