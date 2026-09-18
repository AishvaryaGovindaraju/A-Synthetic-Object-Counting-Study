"""
Synthetic counting-frame generator - REIMPLEMENTATION, not the original script.

The original generator was not retained. This module was written to match the deposited
benchmark images, and its constants are measurements taken from them rather than the
original settings:

    image size            220 x 220 px          (all 195 deposited frames)
    background intensity  1.000                 (95th percentile of every frame)
    blob fill intensity   0.141                 (1st percentile, clean-tier frames with n > 0)
    blob radius           9.2 - 18.9 px         (equivalent-area radius, 897 deposited blobs)
    degradation           Gaussian blur sigma, then additive Gaussian pixel noise

It therefore produces frames of the same family as the deposited benchmark, but it cannot
reproduce the exact 30 seed frames used for the reported results: those frames were not
retained and no random seed for them was recorded. Numbers recomputed from frames generated
here will differ from the published ones.
"""
import numpy as np
from scipy import ndimage

IMG = 220
BG = 1.0
FILL = 0.141
R_MIN, R_MAX = 9.2, 18.9


def _place(n_requested, rng, max_attempts_per_blob=200):
    """Rejection-sample non-overlapping blob centres. Returns the blobs actually placed."""
    blobs = []
    for _ in range(n_requested):
        for _attempt in range(max_attempts_per_blob):
            r = rng.uniform(R_MIN, R_MAX)
            cx, cy = rng.uniform(r, IMG - r), rng.uniform(r, IMG - r)
            if all((cx - bx) ** 2 + (cy - by) ** 2 > (r + br) ** 2 for bx, by, br in blobs):
                blobs.append((cx, cy, r))
                break
    return blobs


def generate(n_requested, blur, noise, rng):
    """Render one frame. Returns (image float array in [0,1], n_realized).

    n_realized is the number of blobs the sampler actually placed, which is the ground-truth
    label. It can fall below n_requested at high density, when rejection sampling exhausts its
    attempt budget - the defect this study found in its own seed sample.
    """
    img = np.full((IMG, IMG), BG, dtype=float)
    yy, xx = np.mgrid[0:IMG, 0:IMG]
    blobs = _place(n_requested, rng)
    for cx, cy, r in blobs:
        img[(xx - cx) ** 2 + (yy - cy) ** 2 <= r ** 2] = FILL
    if blur > 0:
        img = ndimage.gaussian_filter(img, sigma=blur)
    if noise > 0:
        img = img + rng.normal(0.0, noise, img.shape)
    return np.clip(img, 0.0, 1.0), len(blobs)


def make_set(n_frames, seed, label_max=8, blur_range=(0.5, 2.9), noise_range=(0.015, 0.10)):
    """Generate a seed sample. Always record the seed you pass here alongside the outputs."""
    rng = np.random.default_rng(seed)
    out = []
    for i in range(n_frames):
        n_req = int(rng.integers(0, label_max + 1))
        blur = float(rng.uniform(*blur_range))
        noise = float(rng.uniform(*noise_range))
        img, n_real = generate(n_req, blur, noise, rng)
        out.append(dict(index=i, n_requested=n_req, n=n_real, blur=blur, noise=noise, image=img))
    return out


if __name__ == "__main__":
    import argparse, os, pandas as pd
    from PIL import Image
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--n", type=int, default=30)
    ap.add_argument("--seed", type=int, required=True, help="recorded in the output metadata")
    ap.add_argument("--out", default="frames_out")
    a = ap.parse_args()
    os.makedirs(os.path.join(a.out, "frames"), exist_ok=True)
    rows = []
    for rec in make_set(a.n, a.seed):
        p = f"frames/f{rec['index']:03d}.png"
        Image.fromarray((rec.pop("image") * 255).astype(np.uint8)).save(os.path.join(a.out, p))
        rec["path"] = p
        rec["seed"] = a.seed
        rows.append(rec)
    pd.DataFrame(rows).to_csv(os.path.join(a.out, "meta.csv"), index=False)
    under = sum(r["n"] < r["n_requested"] for r in rows)
    print(f"wrote {len(rows)} frames to {a.out}; {under} under-rendered (n < n_requested)")
