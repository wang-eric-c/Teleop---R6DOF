import numpy as np
import pybullet as p
import pybullet_data

import config
from arm_backend import ArmBackend


class SimBackend(ArmBackend):
    def __init__(self, gui=True):
        self._cid = p.connect(p.GUI if gui else p.DIRECT)
        p.configureDebugVisualizer(p.COV_ENABLE_GUI, 0)
        p.resetDebugVisualizerCamera(1.2, 180, -20, [0, 0, 0.4])
        p.setAdditionalSearchPath(pybullet_data.getDataPath())
        p.setGravity(0, 0, -9.81)
        p.loadURDF("plane.urdf")
        self._arm = p.loadURDF(config.URDF_PATH, useFixedBase=True)
        self._ee = config.END_EFFECTOR_LINK

        self._joints = [
            j for j in range(p.getNumJoints(self._arm))
            if p.getJointInfo(self._arm, j)[2] != p.JOINT_FIXED
        ]

    def move_to_pose(self, target_xyz):
        joint_angles = p.calculateInverseKinematics(self._arm, self._ee, target_xyz)
        for i, j in enumerate(self._joints):
            p.setJointMotorControl2(self._arm, j, p.POSITION_CONTROL,
                                    targetPosition=joint_angles[i])

    def set_gripper(self, closed):
        #no gripper with the kuka_iiwa framework, but is possible with other URDFs with frippers
        pass

    def step(self):
        p.stepSimulation()

    def close(self):
        p.disconnect(self._cid)