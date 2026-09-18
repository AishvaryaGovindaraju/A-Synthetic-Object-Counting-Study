# A seed-sample precheck for conformal auto-annotation - code and data deposit

This deposit accompanies the manuscript *A Seed-Sample Precheck for Conformal Auto-Annotation
with a Vision-Language Model Labeler: A Synthetic Object-Counting Study*.

## Read this first: what is original and what is not

**Original, and sufficient to reproduce every published number:** the result tables in `data/`
and the analysis code in `figures/` and `reproduce_tables.py`. These regenerate Figures 1-4 and
Tables 1-2 exactly as submitted.

**Reimplementation, written after the fact:** `generate_frames.py` and `query_annotator.py`.
The original image generator and annotator-query scripts were not retained. These modules were
reconstructed to match the deposited benchmark images, and their constants are measurements
taken from those images rather than the original settings. They generate frames of the same
family and implement the same two scorers, but they **cannot** reproduce the exact seed frames
behind the reported results.

**Not available:** the 30 seed frames themselves, the random seed that produced them, and the
raw per-query annotator responses. The seed sample survives only as the per-image vote shares in
`data/a3_pilot_per_frame.csv`. Anyone rerunning the query step will obtain different frames and
therefore different numbers.

## Layout

    data/                         deposited result tables (original)
      a3_pilot_per_frame.csv      30 seed images: per-label vote shares, both scorers, labels,
                                  degradation parameters. n = requested count, n_visible = realized
                                  count and the ground-truth label
      a3_pilot_alpha_sweep.csv    miscoverage sweep on the seed sample
      a3_precheck_rule_validation.csv  observed vs predicted triviality across 30 alpha values
      a3_ablation_calibration_size.csv, a3_ablation_vote_count.csv
      a3_precheck_summary.json    headline precheck quantities
      benchmark_meta.csv          195 verification frames: tier, requested and realized counts,
                                  blur, noise. The frames themselves are in the separate
                                  data_benchmark archive
    precheck.py                   reference implementation of the three conditions (Supplemental File 1)
    reproduce_tables.py           regenerates Tables 1 and 2
    figures/make_figure_[1-4].py  regenerates each submitted figure
    figures/figstyle_shim.py      minimal stand-ins for the plotting helpers used originally
    verify_ground_truth.py        image-level label verification (protocol step 1.4)
    generate_frames.py            frame generator (REIMPLEMENTATION - see above)
    query_annotator.py            two-scorer query harness (REIMPLEMENTATION - see above)

## Reproducing the published results

    pip install -r requirements.txt
    python reproduce_tables.py --data ./data --out .
    cd figures && PRECHECK_DATA=../data python make_figure_2.py    # and 1, 3, 4

## Running the precheck on your own task

    from precheck import precheck
    precheck(vote_shares, y_true, alpha=0.20)

`vote_shares` is an array of shape (n_images, n_labels) holding the fraction of the K queries
that chose each label; `y_true` holds the true labels. The call returns the three conditions,
the unanimous-error rate with its exact 95% interval, the go/no-go decision, and - when the
decision is underpowered - the seed size that would settle it.

## Verifying ground truth

    python verify_ground_truth.py --meta data/benchmark_meta.csv --root <benchmark frames dir>

Expected output: exact agreement 195/195 (100.0%).

## Citation and licence

Cite the manuscript. [ADD A LICENCE - MIT or CC-BY-4.0 are usual for this kind of deposit.]
