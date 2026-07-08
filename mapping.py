import numpy as np
import config


def _lerp(v, in_lo, in_hi, out_lo, out_hi):
    norm = (v - in_lo)/(in_hi - in_lo + 1e-9)
    norm = max(0.0, min(norm, 1.0))
    return out_lo + norm * (out_hi - out_lo)


def hand_to_pose(landmarks):
    wrist = landmarks[0]
    knuckle = landmarks[9]

    x = _lerp(1 - wrist.x, 0, 1, *config.ARM_X)
    z = _lerp(1 - wrist.y, 0, 1, *config.ARM_Z)

    size = np.hypot(wrist.x - knuckle.x, wrist.y - knuckle.y)
    y = _lerp(size, 0.06, 0.20, *config.ARM_Y)

    return np.array([x, y, z])

def detect_pinch(landmarks):
    wrist = landmarks[0]
    knuckle = landmarks[9]
    scale = np.hypot(wrist.x - knuckle.x, wrist.y - knuckle.y)
    
    thumb = landmarks[4]
    index = landmarks[8]

    dist = np.hypot(thumb.x - index.x, thumb.y - index.y)
    norm = dist/(scale + 1e-9)

    return norm < config.PINCH_THRESHOLD


def is_engaged(landmarks):
    wrist = landmarks[0]
    knuckle = landmarks[9]
    scale = np.hypot(wrist.x - knuckle.x, wrist.y - knuckle.y)

    index = landmarks[8]
    middle = landmarks[12]
    ring = landmarks[16]
    pinky = landmarks[20]

    i_dist = np.hypot(wrist.x - index.x, wrist.y - index.y)
    m_dist = np.hypot(wrist.x - middle.x, wrist.y - middle.y)
    r_dist = np.hypot(wrist.x - ring.x, wrist.y - ring.y)
    p_dist = np.hypot(wrist.x - pinky.x, wrist.y - pinky.y)

    avg = (i_dist + m_dist + r_dist + p_dist)/(4 * scale + 1e-9)

    return avg > config.FIST_THRESHOLD