import numpy as np

import sys
sys.path.append("../")

from scipy.stats import levy_stable

from MFDFA import MFDFA
from MFDFA import singspect

def test_spectrum():
    for N in [1000, 10000]:
        for q_list in [6, 12, 21, 41]:

            alpha = 1.5
            X = levy_stable.rvs(alpha, beta=0, size=N)

            q = np.linspace(-10, 10, q_list)
            q = q[q!=0.0]

            lag = np.unique(
                  np.logspace(
                  0, np.log10(X.size // 4), 55
                  ).astype(int) + 3
                )

            lag, dfa = MFDFA(X, lag = lag, q = q, order = 1)

            alpha, f  = singspect.singularity_spectrum(lag, dfa, q = q)

            _ = singspect.singularity_spectrum(lag, dfa, q=q, lim=[None, None])

            assert alpha.shape[0] == f.shape[0], "Output shape mismatch"
            assert alpha.shape[0] == q.shape[0], "Output shape mismatch"

            q, tau = singspect.scaling_exponents(lag, dfa, q=q)
            assert tau.shape[0] == q.shape[0], "Output shape mismatch"

            q, hq = singspect.hurst_exponents(lag, dfa, q=q)
            assert hq.shape[0] == q.shape[0], "Output shape mismatch"

            try:
                singspect._slopes(lag, dfa, q[0:3])
            except Exception:
                pass
