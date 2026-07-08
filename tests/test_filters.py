import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import numpy as np
from filters import _LowPass, OneEuroFilter


# ---------- _LowPass ----------

def test_lowpass_first_call_passthrough():
    lp = _LowPass()
    assert lp(5.0, 0.5) == 5.0

def test_lowpass_blends_toward_new():
    lp = _LowPass()
    lp(0.0, 0.5)                 # seed at 0
    out = lp(10.0, 0.5)          # halfway blend -> 5
    assert out == 5.0

def test_lowpass_alpha_one_is_responsive():
    lp = _LowPass()
    lp(0.0, 1.0)
    assert lp(10.0, 1.0) == 10.0  # alpha=1 -> fully trust new value


# ---------- OneEuroFilter ----------

def test_first_sample_passthrough():
    f = OneEuroFilter()
    x = np.array([1.0, 2.0, 3.0])
    out = f(x, t=0.0)
    assert np.allclose(out, x)

def test_works_on_vectors():
    f = OneEuroFilter()
    f(np.array([0.0, 0.0, 0.0]), t=0.0)
    out = f(np.array([1.0, 1.0, 1.0]), t=1/30)
    assert out.shape == (3,)

def test_smooths_noise_when_still():
    # constant signal + noise: filtered variance should be well below raw variance
    rng = np.random.default_rng(0)
    f = OneEuroFilter()
    t = 0.0
    raw, filt = [], []
    for _ in range(200):
        x = np.array([1.0]) + rng.normal(0, 0.05, size=1)
        y = f(x, t)
        raw.append(x[0]); filt.append(y[0])
        t += 1/30
    # drop the warm-up samples
    assert np.var(filt[20:]) < np.var(raw[20:]) * 0.5

def test_tracks_fast_ramp():
    # on a fast linear ramp, output should follow closely (adaptive cutoff opens up)
    f = OneEuroFilter()
    t = 0.0
    last_in = last_out = None
    for i in range(100):
        x = np.array([float(i)])       # steep ramp
        y = f(x, t)
        last_in, last_out = x[0], y[0]
        t += 1/30
    # should be within a couple steps of the input, not lagging far behind
    assert abs(last_in - last_out) < 6.0