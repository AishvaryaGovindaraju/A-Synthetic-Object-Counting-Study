"""
Annotator query harness - REIMPLEMENTATION, not the original script.

Implements the two self-consistency scorers of the protocol (steps 2.2 and 2.3) and writes a
vote-share table in the schema of the deposited a3_pilot_per_frame.csv. The annotator itself is
a pluggable callable: no vendor SDK, credential, or model identifier is hard-coded here. Supply
your own `annotate` function, which must take an image path and return a single integer count.
"""
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter

LABELS = list(range(9))
PROMPT = ("Count the dark blobs in this image. Reply with a single integer and nothing else.")


def annotate_stub(image_path):
    raise NotImplementedError(
        "Provide your own annotator. It must accept an image path and return one integer. "
        "Record the model name, version, and access date for the Table of Materials."
    )


def perturbed_views(path, k=5):
    """The K transformed views of protocol step 2.3."""
    im = Image.open(path).convert("L")
    return [im,
            im.filter(ImageFilter.GaussianBlur(1.0)),
            im.filter(ImageFilter.GaussianBlur(2.0)),
            im.resize((im.width // 2, im.height // 2)).resize(im.size, Image.BILINEAR),
            ImageEnhance.Brightness(im).enhance(1.15)][:k]


def vote_shares(votes):
    """Empirical label distribution over LABELS from a list of integer answers."""
    p = np.zeros(len(LABELS))
    for v in votes:
        if 0 <= v < len(LABELS):
            p[v] += 1
    return p / max(1, len(votes))


def score_image(path, y_true, annotate, k=5, mode="repeat", tmpdir=None):
    """Query one image under one scorer. Returns a dict of vote shares and derived quantities."""
    if mode == "repeat":
        votes = [annotate(path) for _ in range(k)]
    elif mode == "perturb":
        import os, tempfile
        votes = []
        tmpdir = tmpdir or tempfile.mkdtemp()
        for i, view in enumerate(perturbed_views(path, k)):
            vp = os.path.join(tmpdir, f"view{i}.png")
            view.save(vp)
            votes.append(annotate(vp))
    else:
        raise ValueError("mode must be 'repeat' or 'perturb'")
    p = vote_shares(votes)
    maj = int(np.argmax(p))
    return dict(agreement=float(p.max()), majority=maj, p_true=float(p[y_true]),
                correct=bool(maj == y_true), **{f"p{i}": float(p[i]) for i in LABELS})


if __name__ == "__main__":
    import argparse, pandas as pd
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--meta", required=True, help="CSV with columns path,n (n = realized count)")
    ap.add_argument("--root", default=".", help="directory the paths are relative to")
    ap.add_argument("--k", type=int, default=5)
    ap.add_argument("--out", default="vote_shares.csv")
    a = ap.parse_args()
    annotate = annotate_stub          # <- replace with your annotator
    meta = pd.read_csv(a.meta)
    rows = []
    for r in meta.itertuples():
        import os
        p = os.path.join(a.root, r.path)
        row = dict(path=r.path, n=getattr(r, "n_requested", r.n), n_visible=r.n,
                   blur=getattr(r, "blur", None), noise=getattr(r, "noise", None))
        for mode, pre in [("repeat", "rep"), ("perturb", "pert")]:
            for key, val in score_image(p, int(r.n), annotate, a.k, mode).items():
                row[f"{pre}_{key}"] = val
        rows.append(row)
    pd.DataFrame(rows).to_csv(a.out, index=False)
    print(f"wrote {len(rows)} rows to {a.out}")
