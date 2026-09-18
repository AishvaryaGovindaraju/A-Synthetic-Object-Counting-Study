"""
Reference implementation of the three-condition feasibility precheck for conformal
auto-annotation (Supplemental File 1). Requires numpy and scipy.

Given, for each seed image, the vote share the annotator assigned to every label and the
true label, precheck() returns the three conditions and the go/no-go decision.
"""
import numpy as np
from scipy import stats


def cp_ci(k, n, conf=0.95):
    """Exact two-sided Clopper-Pearson interval for a binomial proportion."""
    a = (1.0 - conf) / 2.0
    lo = 0.0 if k == 0 else stats.beta.ppf(a, k, n - k + 1)
    hi = 1.0 if k == n else stats.beta.ppf(1 - a, k + 1, n - k)
    return float(lo), float(hi)


def c2_threshold(alpha, n_cal):
    """Exact finite-sample upper bound on e0 for non-trivial sets; -inf if C1 fails."""
    k = int(np.ceil((n_cal + 1) * (1 - alpha)))
    if k > n_cal:
        return -np.inf
    return 1.0 - k / n_cal


def crit_k(n, alpha, sig=0.05):
    """Largest unanimous-error count rejecting H0: e0 >= alpha (one-sided exact binomial)."""
    cdf = stats.binom.cdf(np.arange(n + 1), n, alpha)
    ok = np.where(cdf <= sig)[0]
    return int(ok.max()) if len(ok) else -1


def min_seed(alpha, true_e0, power=0.80, sig=0.05, nmax=5000):
    """Smallest seed size reaching `power` for a GO decision at `alpha` when e0 = true_e0."""
    for n in range(5, nmax + 1):
        k = crit_k(n, alpha, sig)
        if k >= 0 and stats.binom.cdf(k, n, true_e0) >= power:
            return n
    return None


def precheck(vote_shares, y_true, alpha, n_cal=None, conf=0.95):
    """
    vote_shares : (n_images, n_labels) array of per-label vote shares
    y_true      : (n_images,) integer true labels
    alpha       : target miscoverage level
    n_cal       : calibration-set size to be used downstream (default: half the seed sample)
    """
    P = np.asarray(vote_shares, float)
    y = np.asarray(y_true, int)
    n = len(y)
    n_cal = int(round(n / 2)) if n_cal is None else int(n_cal)
    k = int((P[np.arange(n), y] == 0).sum())
    e0 = k / n
    lo, hi = cp_ci(k, n, conf)
    c1 = n_cal >= int(np.ceil(1 / alpha) - 1)
    thr = c2_threshold(alpha, n_cal)
    c2 = bool(e0 <= thr)
    c3 = bool(hi <= thr)
    return dict(n=n, n_cal=n_cal, alpha=alpha, unanimous_errors=k, e0=e0, e0_ci=(lo, hi),
                c2_threshold=thr, C1_size_floor=bool(c1), C2_unanimous_error=c2,
                C3_decision_power=c3, decision="GO" if (c1 and c2 and c3) else "NO-GO",
                seed_needed_for_power=min_seed(alpha, e0) if not c3 else n)


def split_conformal(vote_shares, y_true, alpha, n_splits=400, cal_frac=0.5, seed=0):
    """Mean set size, empirical coverage and singleton yield over random cal/test splits."""
    P = np.asarray(vote_shares, float)
    y = np.asarray(y_true, int)
    rng = np.random.default_rng(seed)
    n = len(y)
    ncal = max(2, int(round(cal_frac * n)))
    S, C, G = [], [], []
    for _ in range(n_splits):
        idx = rng.permutation(n)
        cal, test = idx[:ncal], idx[ncal:]
        if len(test) == 0:
            continue
        s = 1 - P[cal, y[cal]]
        k = int(np.ceil((len(cal) + 1) * (1 - alpha)))
        qhat = 1.0 if k > len(cal) else np.sort(s)[k - 1]
        sets = (1 - P[test]) <= qhat
        S.append(sets.sum(1).mean())
        C.append(sets[np.arange(len(test)), y[test]].mean())
        G.append((sets.sum(1) == 1).mean())
    return float(np.mean(S)), float(np.mean(C)), float(np.mean(G))
