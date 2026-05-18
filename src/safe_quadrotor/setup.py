from setuptools import find_packages, setup
import os
from glob import glob

package_name = 'safe_quadrotor'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob(os.path.join('launch', '*launch.py'))),
        (os.path.join('share', package_name, 'models'), glob(os.path.join('models', '*'))),
        (os.path.join('share', package_name, 'worlds'), glob(os.path.join('worlds', '*.sdf'))),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='mulham-baig',
    maintainer_email='mulham-baig@todo.todo',
    description='Safe autonomous quadrotor navigation tracking and control',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'flight_controller = safe_quadrotor.flight_controller:main',
            'waypoint_navigator = safe_quadrotor.waypoint_navigator:main',
            'safety_monitor = safe_quadrotor.safety_monitor:main',
            'cbf_qp_controller = safe_quadrotor.cbf_qp_controller:main',
        ],
    },
)