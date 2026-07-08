"""
Everything hardware related is abstract since I haven't finished designing my Robotic Arm yet, but stay tuned!
"""
from abc import ABC, abstractmethod
import numpy as np

class ArmBackend(ABC):
    @abstractmethod
    def move_to_pose(self, target_xyz: np.ndarray) -> None:
        ...

    @abstractmethod
    def set_gripper(self, closed: bool) -> None:
        ...

    @abstractmethod
    def step(self) -> None:
        ...

    def close(self) -> None:
        pass