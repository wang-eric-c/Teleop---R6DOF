# Hand Teleop

Control a simulated 6-DOF arm by moving your hand. MediaPipe tracks your hand,
the pose maps to an end-effector target, IK solves for joint angles, and a
PyBullet sim executes it. I'm currently building a custom 6DOF arm, so the hardware connection will be
updated after I finish the PCB and mechanical design.

## Pipeline

```
webcam -> tracking -> mapping -> filter -> backend
          (MediaPipe) (pose+     (one-    (sim: PyBullet IK)
                       gestures)  euro)    (FUTURE) (real: serial to STM32)
```

## Setup

```bash
pip install -r requirements.txt
# hand landmark model (downloads once):
wget -O hand_landmarker.task \
  https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task
```

## Run

```bash
python main.py
```

Move your hand to drive the arm. Make a fist to disengage (clutch) so you can
reposition, open to re-engage. Pinch thumb+index to close the gripper. `q` quits.

## Files

| file                | role                                                    |
|---------------------|---------------------------------------------------------|
| `main.py`           | wires the loop: capture -> track -> map -> filter -> arm |
| `tracking.py`       | MediaPipe hand landmark extraction                      |
| `mapping.py`        | landmarks -> target pose + gesture detection            |
| `filters.py`        | one-euro filter for smoothing jittery landmarks         |
| `arm_backend.py`    | abstract backend interface (the sim/real contract)      |
| `sim_backend.py`    | PyBullet implementation (loads URDF, solves IK)         |
| `serial_backend.py` | STM32 serial stub â€” the sim-to-real hook                |
| `config.py`         | workspace bounds, thresholds, ports, paths              |
