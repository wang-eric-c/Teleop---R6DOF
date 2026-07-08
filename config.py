# --- MediaPipe ---
MODEL_PATH = "hand_landmarker.task"
NUM_HANDS = 1
DETECT_CONF = 0.5
TRACK_CONF = 0.5

# --- Arm workspace (meters). Maps hand position into this box. ---
ARM_X = (-0.3, 0.3)   # left / right
ARM_Y = (0.2, 0.6)    # depth 
ARM_Z = (0.1, 0.8)    # up / down

PINCH_THRESHOLD = 0.05    # thumb tip <-> index tip: below this = gripper closed
FIST_THRESHOLD = 0.15     # fingertip curl metric below this = fist (disengage)

EURO_MIN_CUTOFF = 1.0     # lower = smoother but more lag
EURO_BETA = 0.007         # higher = less lag on fast motion
EURO_D_CUTOFF = 1.0

# --- Sim ---
URDF_PATH = "kuka_iiwa/model.urdf"
END_EFFECTOR_LINK = 6     


"""
Everything hardware related is abstract since I haven't finished designing my Robotic Arm yet, but stay tuned!
"""
# --- Serial (real hardware, later) ---
# SERIAL_PORT = "/dev/ttyUSB0"
# SERIAL_BAUD = 115200