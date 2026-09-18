"""
Image-level ground-truth verification (protocol step 1.4).

Counts blobs directly in each rendered frame by thresholding, morphological opening, and
connected-component labelling, then compares the count with the recorded label. Reproduces the
195/195 agreement reported for the deposited benchmark.
"""
import numpy as np, pandas as pd
from PIL import Image
from scipy import ndimage


def count_blobs(path, thresh=0.5, min_area=20):
    im = np.asarray(Image.open(path).convert("L"), dtype=float) / 255.0
    mask = ndimage.binary_opening(im < thresh, np.ones((3, 3)))
    lab, k = ndimage.label(mask)
    areas = ndimage.sum(mask, lab, range(1, k + 1))
    return int((areas >= min_area).sum())


def verify(meta_csv, root="."):
    import os
    meta = pd.read_csv(meta_csv)
    meta["cc_count"] = [count_blobs(os.path.join(root, p)) for p in meta.path]
    meta["agrees"] = meta.cc_count == meta.n
    return meta


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--meta", required=True)
    ap.add_argument("--root", default=".")
    a = ap.parse_args()
    m = verify(a.meta, a.root)
    print(f"exact agreement: {m.agrees.sum()}/{len(m)} ({100 * m.agrees.mean():.1f}%)")
    if "tier" in m:
        print(m.groupby("tier").agrees.mean().mul(100).round(1).to_string())
    bad = m[~m.agrees]
    if len(bad):
        print("disagreements:"); print(bad[["path", "n", "cc_count"]].to_string(index=False))
