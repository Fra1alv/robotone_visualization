import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.conditions import IfCondition
from launch.substitutions import Command, LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    # Declare launch arguments
    urdf_path = PathJoinSubstitution([
        FindPackageShare('robotone_description'),
        'urdf',
        'robotone.urdf.xacro'
    ])

    # Declare launch arguments for flexibility
    ld = LaunchDescription([
        DeclareLaunchArgument(
            name='urdf',
            default_value=urdf_path,
            description='URDF path'
        ),
        DeclareLaunchArgument(
            name='publish_joints',
            default_value='true',
            description='Launch joint_states_publisher'
        ),
        DeclareLaunchArgument(
            name='use_sim_time',
            default_value='false',
            description='Use simulation time'
        ),
        DeclareLaunchArgument(
            name='rviz',
            default_value='true',
            description='Run rviz'
        ),
    ])

    joint_state_Node = Node(
        package='joint_state_publisher_gui',
        executable='joint_state_publisher_gui',
        name='joint_state_publisher_gui',
        condition=IfCondition(LaunchConfiguration('publish_joints')),
        parameters=[{'use_sim_time': LaunchConfiguration('use_sim_time')}, {'publish_rate': 5.0}]
    )

    robot_state_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        parameters=[{
            'use_sim_time': LaunchConfiguration('use_sim_time'),
            'robot_description': Command(['xacro ', LaunchConfiguration('urdf')])
        }]
    )

    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen',
        condition=IfCondition(LaunchConfiguration('rviz')),
        arguments=[
            '-d',
            os.path.join(
                get_package_share_directory('robotone_visualization'),
                'rviz',
                'robotone_config.rviz'  # Make sure this file exists
            ),
        ],
        parameters=[{'use_sim_time': LaunchConfiguration('use_sim_time')}]
    )

    ld.add_action(joint_state_Node)
    ld.add_action(robot_state_node)
    ld.add_action(rviz_node)

    return ld
