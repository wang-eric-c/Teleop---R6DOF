"""
Everything hardware related is abstract since I haven't finished designing my Robotic Arm yet, but stay tuned!
"""
import numpy as np

import config
from arm_backend import ArmBackend


class SerialBackend(ArmBackend):
    def __init__(self):
        raise NotImplementedError

    def move_to_pose(self, target_xyz):
        raise NotImplementedError

    def set_gripper(self, closed):
        raise NotImplementedError

    def step(self):
        raise NotImplementedError

    def close(self):
        pass