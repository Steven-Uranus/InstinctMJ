import math

import numpy as np

"""A general configuration file for the robots, shared between different scripts. """


class UnitreeWirelessButtons:
    R1 = 0b00000001  # 1
    L1 = 0b00000010  # 2
    start = 0b00000100  # 4
    select = 0b00001000  # 8
    R2 = 0b00010000  # 16
    L2 = 0b00100000  # 32
    F1 = 0b01000000  # 64
    F2 = 0b10000000  # 128
    A = 0b100000000  # 256
    B = 0b1000000000  # 512
    X = 0b10000000000  # 1024
    Y = 0b100000000000  # 2048
    up = 0b1000000000000  # 4096
    right = 0b10000000000000  # 8192
    down = 0b100000000000000  # 16384
    left = 0b1000000000000000  # 32768


class G1_29Dof_TorsoBase:
    NUM_JOINTS = 29
    NUM_ACTIONS = 29
    # NOTE:
    # This order must match InstinctMJ / MuJoCo exported env.yaml + ONNX semantics.
    # It differs from the older shoulder-first InstinctLab ordering.
    joint_map = [
        14,  # waist pitch
        13,  # waist roll
        12,  # waist yaw
        0,  # left hip pitch
        1,  # left hip roll
        2,  # left hip yaw
        3,  # left knee
        4,  # left ankle pitch
        5,  # left ankle roll
        6,  # right hip pitch
        7,  # right hip roll
        8,  # right hip yaw
        9,  # right knee
        10,  # right ankle pitch
        11,  # right ankle roll
        15,  # left shoulder pitch
        16,  # left shoulder roll
        17,  # left shoulder yaw
        18,  # left elbow
        19,  # left wrist roll
        20,  # left wrist pitch
        21,  # left wrist yaw
        22,  # right shoulder pitch
        23,  # right shoulder roll
        24,  # right shoulder yaw
        25,  # right elbow
        26,  # right wrist roll
        27,  # right wrist pitch
        28,  # right wrist yaw
    ]
    sim_joint_names = [  # NOTE: order matters. This list is the order in simulation.
        "waist_pitch_joint",
        "waist_roll_joint",
        "waist_yaw_joint",
        "left_hip_pitch_joint",
        "left_hip_roll_joint",
        "left_hip_yaw_joint",
        "left_knee_joint",
        "left_ankle_pitch_joint",
        "left_ankle_roll_joint",
        "right_hip_pitch_joint",
        "right_hip_roll_joint",
        "right_hip_yaw_joint",
        "right_knee_joint",
        "right_ankle_pitch_joint",
        "right_ankle_roll_joint",
        "left_shoulder_pitch_joint",
        "left_shoulder_roll_joint",
        "left_shoulder_yaw_joint",
        "left_elbow_joint",
        "left_wrist_roll_joint",
        "left_wrist_pitch_joint",
        "left_wrist_yaw_joint",
        "right_shoulder_pitch_joint",
        "right_shoulder_roll_joint",
        "right_shoulder_yaw_joint",
        "right_elbow_joint",
        "right_wrist_roll_joint",
        "right_wrist_pitch_joint",
        "right_wrist_yaw_joint",
    ]
    real_joint_names = [  # NOTE: order matters. This list is the order in real robot.
        "left_hip_pitch_joint",
        "left_hip_roll_joint",
        "left_hip_yaw_joint",
        "left_knee_joint",
        "left_ankle_pitch_joint",
        "left_ankle_roll_joint",
        "right_hip_pitch_joint",
        "right_hip_roll_joint",
        "right_hip_yaw_joint",
        "right_knee_joint",
        "right_ankle_pitch_joint",
        "right_ankle_roll_joint",
        "waist_yaw_joint",
        "waist_roll_joint",
        "waist_pitch_joint",
        "left_shoulder_pitch_joint",
        "left_shoulder_roll_joint",
        "left_shoulder_yaw_joint",
        "left_elbow_joint",
        "left_wrist_roll_joint",
        "left_wrist_pitch_joint",
        "left_wrist_yaw_joint",
        "right_shoulder_pitch_joint",
        "right_shoulder_roll_joint",
        "right_shoulder_yaw_joint",
        "right_elbow_joint",
        "right_wrist_roll_joint",
        "right_wrist_pitch_joint",
        "right_wrist_yaw_joint",
    ]
    joint_signs = np.array(
        [
            -1,
            -1,
            -1,
            1,
            1,
            1,
            1,
            1,
            1,
            1,
            1,
            1,
            1,
            1,
            1,
            1,
            1,
            1,
            1,
            1,
            1,
            1,
            1,
            1,
            1,
            1,
            1,
            1,
            1,
        ],
        dtype=np.float32,
    )
    joint_limits_high = np.array(
        [
            0.5200,
            0.5236,
            2.6180,
            2.8798,
            2.9671,
            2.7576,
            2.8798,
            0.5236,
            0.2618,
            2.8798,
            0.5236,
            2.7576,
            2.8798,
            0.5236,
            0.2618,
            2.6704,
            2.2515,
            2.6180,
            2.0944,
            1.9722,
            1.6144,
            1.6144,
            2.6704,
            1.5882,
            2.6180,
            2.0944,
            1.9722,
            1.6144,
            1.6144,
        ],
        dtype=np.float32,
    )
    joint_limits_low = np.array(
        [
            -0.5200,
            -0.5200,
            -2.6180,
            -2.5307,
            -0.5236,
            -2.7576,
            -0.0873,
            -0.8727,
            -0.2618,
            -2.5307,
            -2.9671,
            -2.7576,
            -0.0873,
            -0.8727,
            -0.2618,
            -3.0892,
            -1.5882,
            -2.6180,
            -1.0472,
            -1.9722,
            -1.6144,
            -1.6144,
            -3.0892,
            -2.2515,
            -2.6180,
            -1.0472,
            -1.9722,
            -1.6144,
            -1.6144,
        ],
        dtype=np.float32,
    )
    torque_limits = np.array(
        [  # from urdf and in simulation order
            50,
            50,
            88,
            88,
            88,
            88,
            139,
            50,
            50,
            88,
            88,
            88,
            139,
            50,
            50,
            25,
            25,
            25,
            25,
            25,
            5,
            5,
            25,
            25,
            25,
            25,
            25,
            5,
            5,
        ],
        dtype=np.float32,
    )
    turn_on_motor_mode = [0x01] * 29
    mode_pr = 0
    mode_machine = 5
    """ please check this value from
        https://support.unitree.com/home/zh/G1_developer/basic_services_interface
        https://github.com/unitreerobotics/unitree_ros/tree/master/robots/g1_description
    """
    realsense_depth_link_transform = {
        "translation": (
            0.04764571478 + 0.0039635 - 0.0042 * math.cos(math.radians(48)),
            0.015,
            0.46268178553 - 0.044 + 0.0042 * math.sin(math.radians(48)) + 0.016,
        ),
        "rotation": (
            math.cos(math.radians(0.5) / 2) * math.cos(math.radians(48) / 2),  # w
            math.sin(math.radians(0.5) / 2),  # x
            math.sin(math.radians(48) / 2),  # y
            0.0,  # z
        ),
        "parent_frame": "torso_link",
        "child_frame": "realsense_depth_link",
    }
