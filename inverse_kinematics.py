import numpy as np
import pybullet as p
import pybullet_data
import config as c
 
 
class IKSolver:
    def __init__(self, urdf_path, joints, end_effector_link, damping=0.05):
        self._cid = p.connect(p.DIRECT)
        p.setAdditionalSearchPath(pybullet_data.getDataPath(), physicsClientId=self._cid)
        self._body = p.loadURDF(urdf_path, useFixedBase=True,
                                 physicsClientId=self._cid)
 
        self._joints = joints
        self._ee = end_effector_link
        self._damping = damping
 
        self._lower, self._upper = self._get_joint_limits()
 
    def _get_joint_limits(self):
        lower, upper = [], []
        for j in self._joints:
            info = p.getJointInfo(self._body, j, physicsClientId=self._cid)
            lo, hi = info[8], info[9]
            if lo > hi:
                lo, hi = -np.inf, np.inf
            lower.append(lo)
            upper.append(hi)
        return np.array(lower), np.array(upper)
 
    def _apply_angles(self, angles):
        for j, a in zip(self._joints, angles):
            p.resetJointState(self._body, j, a, physicsClientId=self._cid)
 
    def _fk(self, angles):
        self._apply_angles(angles)
        state = p.getLinkState(self._body, self._ee, physicsClientId=self._cid)
        return np.array(state[0])
 
    def solve(self, current_angles, target_xyz):
        angles = np.array(current_angles, dtype=float)
        n = len(self._joints)
        target = np.array(target_xyz, dtype=float)
 
        for _ in range(c.IK_MAX_ITERS):
            tip = self._fk(angles)
            error = target - tip
            if np.linalg.norm(error) < c.IK_TOLERANCE:
                break
 
            zeros = [0.0] * n
            J_lin, _ = p.calculateJacobian(
                self._body, self._ee, [0, 0, 0],
                list(angles), zeros, zeros,
                physicsClientId=self._cid,
            )
            J = np.array(J_lin)

            JJt = J @ J.T
            damped_inv = J.T @ np.linalg.inv(JJt + (self._damping ** 2) * np.eye(JJt.shape[0]))
            d_theta = (damped_inv @ error) * c.IK_STEP
 
            angles = angles + d_theta
            angles = np.clip(angles, self._lower, self._upper)
 
        return angles.tolist()
 
    def close(self):
        p.disconnect(self._cid)