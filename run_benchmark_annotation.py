"""
Automated annotation of the 195 benchmark frames using Google Gemini API.
Runs both scorers (repeated sampling K=5 and perturbation ensemble K=5)
and records per-image vote shares, agreement, correctness, and signed errors.
Saves progress incrementally to data/benchmark_195_per_frame.csv.
"""
import os, sys, time, re, base64, tempfile
from concurrent.futures import ThreadPoolExecutor
import numpy as np, pandas as pd
from PIL import Image, ImageEnhance, ImageFilter
import requests

API_KEYS = [
    k.strip() for k in os.environ.get("GEMINI_API_KEY", "").split(",") if k.strip()
] or [os.environ.get("GOOGLE_API_KEY", "YOUR_API_KEY_HERE")]
MODELS = ["gemini-3.1-flash-lite", "gemini-3.5-flash-lite", "gemini-3.5-flash"]
LABELS = list(range(11))  # 0 through 10
PROMPT = "Count the dark blobs in this image. Reply with a single integer and nothing else."


def annotate_bytes(img_bytes, temp=1.0, retries=8):
    img_b64 = base64.b64encode(img_bytes).decode("utf-8")
    payload = {
        "contents": [{
            "parts": [
                {"inline_data": {"mime_type": "image/png", "data": img_b64}},
                {"text": PROMPT}
            ]
        }],
        "generationConfig": {"temperature": temp, "maxOutputTokens": 16}
    }
    for attempt in range(retries):
        key = API_KEYS[attempt % len(API_KEYS)]
        model_name = MODELS[(attempt // len(API_KEYS)) % len(MODELS)]
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={key}"
        try:
            r = requests.post(url, json=payload, timeout=30)
            if r.status_code == 200:
                txt = r.json().get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "").strip()
                m = re.findall(r"\b\d+\b", txt)
                if m:
                    return int(m[0])
            elif r.status_code == 429:
                sleep_s = 3.0 * (attempt + 1)
                time.sleep(sleep_s)
        except Exception:
            time.sleep(2.0)
    return -1


def get_perturbed_images(im):
    gray = im.convert("L")
    return [
        gray,
        gray.filter(ImageFilter.GaussianBlur(1.0)),
        gray.filter(ImageFilter.GaussianBlur(2.0)),
        gray.resize((gray.width // 2, gray.height // 2)).resize(gray.size, Image.BILINEAR),
        ImageEnhance.Brightness(gray).enhance(1.15)
    ]


def vote_shares(votes):
    p = np.zeros(len(LABELS), dtype=float)
    valid = 0
    for v in votes:
        if 0 <= v < len(LABELS):
            p[v] += 1
            valid += 1
    return p / max(1, valid)


def process_image(row_dict, root="data/data_benchmark"):
    rel_path = row_dict["path"]
    full_path = os.path.join(root, rel_path)
    y_true = int(row_dict["n"])

    # Load image once into memory
    with open(full_path, "rb") as f:
        orig_bytes = f.read()

    # 1. Repeated Sampling (K=5)
    with ThreadPoolExecutor(max_workers=5) as ex:
        rep_votes = list(ex.map(lambda _: annotate_bytes(orig_bytes, temp=1.0), range(5)))
    rep_p = vote_shares(rep_votes)
    rep_maj = int(np.argmax(rep_p))
    rep_agree = float(rep_p.max())
    rep_p_true = float(rep_p[y_true]) if y_true < len(rep_p) else 0.0
    rep_corr = bool(rep_maj == y_true)

    # 2. Perturbation Ensemble (K=5)
    im = Image.open(full_path)
    pert_views = get_perturbed_images(im)
    pert_bytes_list = []
    for v in pert_views:
        import io
        buf = io.BytesIO()
        v.save(buf, format="PNG")
        pert_bytes_list.append(buf.getvalue())

    with ThreadPoolExecutor(max_workers=5) as ex:
        pert_votes = list(ex.map(lambda b: annotate_bytes(b, temp=0.0), pert_bytes_list))
    pert_p = vote_shares(pert_votes)
    pert_maj = int(np.argmax(pert_p))
    pert_agree = float(pert_p.max())
    pert_p_true = float(pert_p[y_true]) if y_true < len(pert_p) else 0.0
    pert_corr = bool(pert_maj == y_true)

    res = {
        "path": rel_path,
        "tier": row_dict.get("tier", "unknown"),
        "n": row_dict.get("n_requested", y_true),
        "n_visible": y_true,
        "blur": row_dict.get("blur", None),
        "noise": row_dict.get("noise", None),
        "rep_agreement": rep_agree,
        "rep_majority": rep_maj,
        "rep_p_true": rep_p_true,
        "rep_correct": rep_corr,
        "rep_votes": str(rep_votes),
        "pert_agreement": pert_agree,
        "pert_majority": pert_maj,
        "pert_p_true": pert_p_true,
        "pert_correct": pert_corr,
        "pert_votes": str(pert_votes)
    }
    for i in LABELS:
        res[f"rep_p{i}"] = float(rep_p[i])
        res[f"pert_p{i}"] = float(pert_p[i])

    return res


def run_benchmark(meta_csv="data/benchmark_meta.csv", out_csv="data/benchmark_195_per_frame.csv", max_frames=None):
    meta = pd.read_csv(meta_csv)
    if max_frames:
        meta = meta.iloc[:max_frames]

    # Check for existing completed rows to support resumption
    completed_paths = set()
    rows = []
    if os.path.exists(out_csv):
        try:
            existing = pd.read_csv(out_csv)
            completed_paths = set(existing["path"].values)
            rows = existing.to_dict("records")
            print(f"Resuming: found {len(completed_paths)} already annotated images in {out_csv}")
        except Exception:
            pass

    total = len(meta)
    print(f"Starting annotation on {total} frames using Gemini (flash-lite / flash)...", flush=True)
    t_start = time.time()

    for idx, r in meta.iterrows():
        p = r["path"]
        if p in completed_paths:
            continue

        t0 = time.time()
        row_res = process_image(r.to_dict())
        rows.append(row_res)
        completed_paths.add(p)

        # Incrementally save after every single image
        pd.DataFrame(rows).to_csv(out_csv, index=False)
        elapsed = time.time() - t_start
        rate = len(completed_paths) / max(1e-4, elapsed)
        remaining = (total - len(completed_paths)) / max(1e-4, rate)
        print(f"[{len(completed_paths)}/{total}] {p} (true={r['n']}) | rep_maj={row_res['rep_majority']} pert_maj={row_res['pert_majority']} | {time.time()-t0:.1f}s (ETA {remaining/60:.1f}m)", flush=True)

    print(f"\nALL {len(rows)} FRAMES COMPLETED in {(time.time()-t_start)/60:.1f} minutes! Saved to {out_csv}", flush=True)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--meta", default="data/benchmark_meta.csv")
    parser.add_argument("--out", default="data/benchmark_195_per_frame.csv")
    parser.add_argument("--limit", type=int, default=None)
    args = parser.parse_args()
    run_benchmark(args.meta, args.out, args.limit)
