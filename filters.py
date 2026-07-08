import numpy as np
import config

class _LowPass:
    def __init__(self):
        self.y_prev = None

    def __call__(self, x, alpha):
        if self.y_prev is None:
            self.y_prev = x
            return x
        
        y = alpha * x + (1 - alpha) * self.y_prev
        self.y_prev = y
        return y

class OneEuroFilter:
    def __init__(self,
                 min_cutoff=config.EURO_MIN_CUTOFF,
                 beta=config.EURO_BETA,
                 d_cutoff=config.EURO_D_CUTOFF):
        self.min_cutoff = min_cutoff
        self.beta = beta
        self.d_cutoff = d_cutoff
        self.t_prev = None
        self.x_prev = None

        self.low_pass_x = _LowPass()
        self.dx_filter = _LowPass()

    @staticmethod
    def _alpha(cutoff, dt):
        tau = 1.0/(2 * np.pi * cutoff)
        return (1.0 / (1.0 + tau/dt))

    def __call__(self, x, t):
        if self.t_prev is None:
            self.t_prev = t
            self.x_prev = x
            return x
        
        dt = t - self.t_prev
        dx = (x - self.x_prev)/dt

        dx_hat = self.dx_filter(dx, self._alpha(self.d_cutoff, dt))

        cutoff = self.beta * np.abs(dx_hat) + self.min_cutoff
        x_hat = self.low_pass_x(x, self._alpha(cutoff, dt))

        self.t_prev = t
        self.x_prev = x
        return x_hat