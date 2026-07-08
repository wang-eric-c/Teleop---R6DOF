import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import numpy as np
import pytest
import config
import mapping


class FakeLandmark:
    def __init__(self, x, y, z=0.0):
        self.x, self.y, self.z = x, y, z


def _hand(overrides=None):
    lm = [FakeLandmark(0.5, 0.5) for _ in range(21)]
    for i, (x, y) in (overrides or {}).items():
        lm[i] = FakeLandmark(x, y)
    return lm


# ---------- _lerp ----------

def test_lerp_midpoint():
    assert mapping._lerp(0.5, 0, 1, 0, 10) == pytest.approx(5)

def test_lerp_clamps_above():
    assert mapping._lerp(2.0, 0, 1, 0, 10) == pytest.approx(10)

def test_lerp_clamps_below():
    assert mapping._lerp(-1.0, 0, 1, 0, 10) == pytest.approx(0)

def test_lerp_inverted_output_range():
    # out_lo > out_hi (used for depth): still maps correctly
    assert mapping._lerp(0.0, 0, 1, 10, 0) == pytest.approx(10)


# ---------- detect_pinch ----------

def test_pinch_true_when_tips_touch():
    lm = _hand({4: (0.5, 0.5), 8: (0.5, 0.5)})
    assert mapping.detect_pinch(lm)

def test_pinch_false_when_tips_apart():
    lm = _hand({4: (0.2, 0.2), 8: (0.8, 0.8)})
    assert not mapping.detect_pinch(lm)


# ---------- is_engaged ----------

def test_engaged_true_when_fingers_extended():
    lm = _hand({0: (0.5, 0.9), 8: (0.5, 0.1), 12: (0.5, 0.1),
                16: (0.5, 0.1), 20: (0.5, 0.1)})
    assert mapping.is_engaged(lm)

def test_engaged_false_when_fingers_curled():
    lm = _hand({0: (0.5, 0.5), 8: (0.5, 0.52), 12: (0.5, 0.52),
                16: (0.5, 0.52), 20: (0.5, 0.52)})
    assert not mapping.is_engaged(lm)


# ---------- hand_to_pose ----------

def test_pose_within_workspace():
    rng = np.random.default_rng(0)
    for _ in range(50):
        lm = [FakeLandmark(rng.random(), rng.random()) for _ in range(21)]
        x, y, z = mapping.hand_to_pose(lm)
        assert config.ARM_X[0] <= x <= config.ARM_X[1]
        assert config.ARM_Y[0] <= y <= config.ARM_Y[1]
        assert config.ARM_Z[0] <= z <= config.ARM_Z[1]

def test_pose_mirror_x():
    # hand on the LEFT of image (small wrist.x) -> arm toward +x (mirror)
    left = mapping.hand_to_pose(_hand({0: (0.1, 0.5), 9: (0.1, 0.55)}))
    right = mapping.hand_to_pose(_hand({0: (0.9, 0.5), 9: (0.9, 0.55)}))
    assert left[0] > right[0]

def test_pose_returns_three_axes():
    p = mapping.hand_to_pose(_hand())
    assert p.shape == (3,)