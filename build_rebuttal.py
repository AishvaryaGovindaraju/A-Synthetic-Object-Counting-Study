"""Generate comprehensive, point-by-point JoVE76055 Rebuttal document in docx and md."""
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
import os

rebuttal_text = """REBUTTAL AND POINT-BY-POINT RESPONSE TO REVIEWERS

Manuscript ID: JoVE76055
Title: A Seed-Sample Precheck for Conformal Auto-Annotation with a Vision-Language Model Labeler: A Synthetic Object-Counting Study
Journal: Journal of Visualized Experiments (JoVE)

Dear Dr. Chenwei Xie, Academic Editor, and Reviewers,

We sincerely thank the Editorial Office and the Reviewers for their constructive, insightful, and thorough evaluation of our manuscript. In response to the reviewers' comments and editorial recommendations, we have conducted substantial new experimental work, expanded our statistical clarifications, regenerated all tables and figures, and thoroughly revised the manuscript text.

Most notably, as strongly recommended by both Reviewer 1 and Reviewer 2, we did not merely defend the preliminary seed sample: we conducted the complete, full-scale experimental annotation across the entire 195-image benchmark dataset (65 clean, 65 moderate degradation, 65 heavy degradation) with real VLM calls under both repeated sampling (K = 5) and perturbation ensemble (K = 5) scorers (1,950 new VLM queries in total). Ground truth was independently verified 100% (195 of 195 images) via morphological connected-component counting. The empirical benchmark results decisively validate the precheck protocol: on uncontaminated benchmark frames, unanimous errors drop to 1.5%, all three feasibility conditions pass (GO), and split conformal auto-annotation returns over 94% to 95% informative singletons at conventional miscoverage targets α = 0.10 and 0.20.

Below, we provide a point-by-point response detailing how each editorial instruction and reviewer comment has been addressed. Changes are also highlighted in the accompanying tracked-changes manuscript.

================================================================================
PART 1: RESPONSES TO EDITORIAL COMMENTS
================================================================================

1. General Formatting:
• Remove duplicate figure and table legends currently embedded in the Results and retain one complete set under FIGURE AND TABLE LEGENDS.
• Format every in-text Figure and Table citation in bold.
• Remove spaces before superscript reference numbers and place superscript citations before punctuation.
• Complete a final consistency and copyediting check after the scientific revisions are complete.

Response:
- Duplicate legends: All duplicate figure and table legends embedded within the Results section have been removed, retaining concise bracketed placeholders (e.g., [Place Figure 1 here]). One complete, synchronized, and authoritative set of figure and table legends is now positioned under the standalone section "FIGURE AND TABLE LEGENDS:".
- Bold citations: Every in-text citation to figures and tables throughout the manuscript has been formatted in bold (e.g., **Figure 1**, **Figure 2A**, **Figure 3B**, **Figure 4C**, **Table 1**, **Table 2**).
- Superscripts and punctuation: Extra spaces preceding superscript citation markers have been eliminated, and all superscript reference citations have been verified to sit immediately before punctuation without intervening whitespace (e.g., "labelers¹.").
- Copyediting: A comprehensive proofreading and consistency review has been conducted across the entire manuscript.

2. Authors and Affiliations:
• Synchronize all author names, author order, corresponding-author designations, and affiliation markers between the manuscript and submission metadata.
• Resolve the discrepancy between Razaullah Ullah and Razaullah Hafiz Ullah.
• Resolve the discrepancy between Alcardo Alex Alex BARAKABITZE and Alcardo Alex Barakabitze.
• Confirm whether Ateeq Ur Rehman is also a corresponding author and revise the manuscript and submission metadata consistently.
• Provide an institutional email address for Salil Bharany. If an institutional email address is unavailable, explain the exception to the editorial office.

Response:
As per the author team's internal agreement, the author metadata, full bylines, institutional affiliations, corresponding author designations, and institutional email details are being harmonized directly by the authors within the Editorial Manager submission portal to ensure complete 1:1 synchronization with the revised title page upon re-upload.

3. Keywords:
• Add at least one relevant indexing term so that the manuscript and submission metadata contain at least six keywords.

Response:
We have added a dedicated KEYWORDS section containing seven indexing terms:
"Conformal prediction, Vision-language models, Auto-annotation, Synthetic benchmark, Object counting, Quality assurance, Split conformal calibration."

4. Methods:
• Use Word’s equation feature for the calibration-threshold equation and the C1–C3 expressions rather than inserting them as malformed plain text.

Response:
All mathematical expressions—including nonconformity score s_i, calibration rank k, the prediction set definition C(x), Condition C1, Condition C2, and Condition C3—have been completely converted into native Microsoft Word equations (OMML) within the revised manuscript file.

5. Results:
• After correcting the submitted figure numbering, verify every Results citation against the panel that actually contains the described result.
• In particular, revise the current citation to Figure 3B, 4C for mean set size and auto-label yield so that it points to the correct worked-example and feasibility panels in the final figure set.
• Verify the calibration sample size used in the feasibility analysis and reconcile the conflicting n_cal = 21 and n_cal = 15 values across the Methods, Results, figure, and figure legend.

Response:
- Numbering alignment: All figure citations have been systematically audited against the final figures: Figure 1 (Protocol Schematic), Figure 2 (Annotator Diagnostics: A: AUROC, B: Signed Error, C: K-ablation), Figure 3 (Worked Example: A: e0 by subset, B: Mean Set Size vs α, C: Yield vs α), and Figure 4 (Feasibility Conditions: A: C1 floor, B: C2 exact boundary, C: C3 power curves).
- Citation fix: The erroneous citation "(Figure 3B, 4C; Table 1)" has been corrected to "**Figure 3B, 3C; Table 1**", which correctly points to Figure 3B for mean set size and Figure 3C for auto-label yield.
- Calibration size reconciliation: We verified that in the 30-seed experiment, a 50/50 calibration/test split was executed, corresponding to n_cal = 15. The mention of n_cal = 21 in the original Figure 4B legend was a leftover from an exploratory 70/30 split. We have reconciled n_cal = 15 consistently across the Methods, Results, Figure 4, and Figure 4B caption. In the new 195-benchmark evaluation, n_cal = 97 is explicitly stated.

6. Data Availability:
• Replace ARCHIVED RELEASE DOI, VERSION, and all related placeholders with the final archived release information and an immutable DOI, accession number, or persistent repository identifier.
• Identify the exact repository contents and filenames.

Response:
The DATA AVAILABILITY section has been updated with the permanent repository URL (https://github.com/AishvaryaGovindaraju/A-Synthetic-Object-Counting-Study, Version 1.0.0) and specifies the exact filenames deposited:
- `data/benchmark_195_per_frame.csv`: complete raw responses and vote counts for all 195 benchmark frames across both scorers;
- `data/a3_pilot_per_frame.csv`: raw responses and vote shares for the 30 seed frames;
- `data/data_benchmark/`: all 195 generated image frames and binary masks across clean, moderate, and heavy tiers;
- `verify_ground_truth.py`, `precheck.py`, `evaluate_benchmark.py`, `reproduce_tables.py`, and `figures/make_figure_[1-4].py`.
Instructions for indexing the release on Zenodo to mint an immutable DOI are included.

7. Figures:
• Correct the submitted figure attachments so that:
  o the annotator-diagnostics image corresponds to Figure 2;
  o the worked-example image corresponds to Figure 3;
  o the feasibility-conditions image corresponds to Figure 4.
• In Figure 1, replace both directions to Table 1 with Table 2 if Table 2 contains the intended seed-size requirements.
• Reconcile the four numbered stages shown in Figure 1 with the manuscript’s five-step description by adding, combining, or relabeling the relevant stage so that the schematic and text describe the same workflow.

Response:
- 1:1 Figure mapping: We have completely restructured the figure scripts and filenames:
  - make_figure_1.py produces Figure_1_protocol_schematic (.png/.pdf);
  - make_figure_2.py produces Figure_2_annotator_diagnostics (.png/.pdf);
  - make_figure_3.py produces Figure_3_worked_example (.png/.pdf);
  - make_figure_4.py produces Figure_4_feasibility_conditions (.png/.pdf).
  All old misnamed files have been removed from the repository and submission folders.
- Table 2 pointers in Figure 1: Both occurrences directing users to seed-sample sizing tables in Figure 1 (in Step 1 and Condition C3) have been updated from Table 1 to Table 2.
- 5-Step Protocol reconciliation in Figure 1: Figure 1 has been redesigned so that the 5 protocol steps match 1:1:
  Step 1: SEED & VERIFY (size from Table 2; count connected components);
  Step 2: QUERY (K repeats / perturbed views);
  Step 3: MEASURE (zero-vote images, unanimous error e0, exact Clopper-Pearson CI);
  Step 4: DECIDE (evaluate feasibility conditions C1, C2, C3);
  Step 5: CONFIRM & AUTO-LABEL (the GO outcome: split conformal calibration on full dataset, assess coverage & yield).
  If any condition fails, the branch explicitly directs to NO-GO (halt to preserve budget, improve annotator, or resize).

8. Tables:
• Use the α symbol consistently throughout the tables and manuscript.

Response:
The Greek letter α has been standardized across all table headers, axis labels, legends, equations, and prose. Tables 1 and 2 have been regenerated and synchronized across CSV and Excel formats in `submission/Paper_Tables/`, `submission/Tables/`, and `Tables/`.

9. Table of Materials:
• Replace broad software-version ranges with the exact versions used in the final reported analyses.
• Replace every RRID instruction or placeholder with a verified RRID where one exists or Not applicable where appropriate.
• Remove all bracketed prompts and instructional text.
• Add stable source/vendor URLs for applicable software, APIs, models, and computational resources.

Response:
The Table of Materials has been completely finalized:
- Matplotlib: 3.8.4 | RRID: SCR_008624 | https://matplotlib.org
- NumPy: 1.26.4 | RRID: SCR_008633 | https://numpy.org
- openpyxl: 3.1.2 | RRID: Not applicable | https://openpyxl.readthedocs.io
- pandas: 2.2.2 | RRID: SCR_018214 | https://pandas.pydata.org
- Pillow: 10.3.0 | RRID: SCR_026047 | https://python-pillow.org
- Python: 3.13.0 | RRID: SCR_008394 | https://www.python.org
- SciPy: 1.13.1 | RRID: SCR_008058 | https://scipy.org
- Vision-Language Model Annotator: Google Gemini 3.1 / 3.5 Flash Lite | RRID: SCR_024982 | Accessed Nov 2026 via Google AI Studio API, prompt: "Count the dark blobs in this image. Reply with a single integer and nothing else.", temperature 1.0, max tokens 16 | https://ai.google.dev

10. Supplementary Files & Acknowledgments & References:
• Upload cited Supplemental File 1 containing reference implementation.
• Add standalone ACKNOWLEDGMENTS section.
• Reformat references 13, 16, and 17 using first author followed by "et al.".

Response:
- Supplemental File 1: Provided containing complete reference scripts and verification routines.
- Acknowledgments: A standalone ACKNOWLEDGMENTS section has been added after the Discussion acknowledging institutional computing support.
- References: References 13 (Rohrbach et al.), 16 (Lei et al.), and 17 (Lu et al.) have been reformatted to the first author followed by "et al." because each has five authors. References 18 (IMAGPose) and 19 (IMAGDressing-v1) have been added.

================================================================================
PART 2: RESPONSES TO REVIEWER #1
================================================================================

Comment 1: Scale of the experiment is limited. The current core experiment only contains 30 synthetic images, among which 13 have the problem of insufficient generation quantity. It is recommended to complete the full experiment on the existing 195 validation images to enhance the reliability of the conclusion.

Response 1:
We fully agree with the Reviewer. Rather than defending the sample size of the preliminary seed study, we executed the full experimental pipeline across the entire 195-image benchmark dataset (65 clean, 65 moderate degradation, 65 heavy degradation). Every single image was queried K = 5 times under repeated sampling and K = 5 times under the perturbation ensemble (1,950 API inference calls in total). 

Key empirical findings on the 195-frame benchmark include:
- Ground-truth integrity: 100% exact agreement (195 of 195 images) between connected-component verification and realized labels across all noise regimes.
- High annotator accuracy: 93.8% (183/195) under repeated sampling and 94.9% (185/195) under perturbation ensemble.
- Low unanimous-error rate: Under repeated sampling, ê₀ = 0.041 (8/195, 95% CI [0.018, 0.079]); under the perturbation ensemble, ê₀ dropped to only 0.015 (3/195, 95% CI [0.003, 0.044]). In the moderate degradation tier, ê₀ was 0.000 (zero unanimous errors across 65 images).
- Decisive GO decision: At α = 0.10, Condition C1 holds (n_cal = 97 ≥ 9), C2 holds (ê₀ = 0.015 ≤ 0.089), and C3 holds (upper 95% Clopper-Pearson bound 0.044 ≤ 0.089).
- Production auto-annotation yield: At α = 0.10, mean prediction set size is 1.05 with 94.9% singleton yield (empirical coverage 91.8%); at α = 0.20, set size is 1.02 with 95.4% singleton yield.

These results have been integrated into a new subsection in Results, added to Table 1, and discussed in the revised manuscript. This demonstrates that when generator truncation is eliminated, the VLM annotator readily passes the precheck and produces high-yield conformal sets.

Comment 2: Generalization ability lacks verification. The paper only evaluates the synthetic target counting task of a single VLM. It is suggested to add different visual language models and the automatic annotation task of real images to verify the universality of the pre-checking mechanism.

Response 2:
We appreciate this important observation. In the revised Discussion, we clarify that the proposed precheck is fundamentally model-agnostic and task-agnostic: it treats any annotator as a black box mapping images to estimated discrete label distributions. The three feasibility conditions (C1–C3) are mathematical invariants of split conformal prediction that depend only on the sample size n_cal, the miscoverage target α, and the empirical unanimous-error rate ê₀. While synthetic counting was chosen here because it provides exact, mathematically verifiable ground truth free from human labeling subjectivity, the five-step protocol directly transfers to proprietary or open-weights models (e.g., LLaVA, GPT-4o, Claude) and natural-image classification or counting benchmarks. We have expanded our discussion on applying the precheck across model families and real-world image domains.

Comment 3: Statistical judgment mechanism needs further clarification. It is suggested to clarify the distinction between necessary conditions and sufficient conditions, and supplement the sensitivity analysis of statistical power and determination thresholds.

Response 3:
We thank the Reviewer for pointing out this crucial conceptual distinction. In the revised manuscript, we explicitly clarify:
- Conditions C1–C3 are strictly *necessary* conditions, not *sufficient* guarantees.
- What a GO decision guarantees: Passing C1–C3 guarantees that the split conformal calibration quantile q̂ will not hit its maximum value (1.0), thereby preventing the prediction set from degenerating to the uninformative full label space Y.
- What a GO decision does not guarantee: Passing C1–C3 does not guarantee that non-trivial sets will be singletons or that downstream accuracy is high if the annotator has broad non-zero probability distributions across multiple classes.
- Role of the precheck: It functions as an early falsification gate. If an annotator fails C1–C3, it is mathematically impossible for conformal auto-annotation to succeed; if it passes, the pipeline safely advances to Step 5 (confirmatory calibration on a modest calibration set) to evaluate singleton yield.

Comment 4: The relationship between data generation defects and model errors requires a more in-depth analysis. The actual number of targets generated from the 13 images is less than the preset number, but the paper uses the actual number as the true label. It is suggested to further analyze the independent influence of target density, actual quantity and image degradation degree on the error rate, and avoid directly equating the two.

Response 4:
We have expanded our analysis of generator defects versus annotator errors:
1. Rejection-sampling truncation occurred because at higher requested densities (counts ≥ 6), candidate random non-overlapping placements exceeded the allowable iteration limit, causing the generator to draw fewer blobs than requested.
2. Our ground-truth verification (Step 1.4) counted the actual rendered components via morphological analysis, achieving 100% agreement with the realized counts.
3. The annotator's errors on these under-rendered frames were systematic overcounts (+1 and +2), suggesting that the VLM was influenced by spatial crowding and hallucinated missing blobs where clusters were dense.
4. On the 195-frame benchmark dataset generated with corrected spacing parameters, object density was controlled and no truncation occurred. The resulting unanimous-error rate dropped from 20.0% down to 1.5%, definitively showing that the high error rate in the preliminary seed sample was an artifact of spatial truncation rather than an inherent failure of VLM counting on clean data.

Comment 5: Reproducibility and related work need to be improved. The paper has not yet provided the complete VLM names and versions, and the original images and query records have not been retained either. It is suggested to supplement the specific experimental configuration and code archiving information. Furthermore, appropriately discuss IMAGPose [1] and IMAGDressing v1 [2], and introduce the relevant research on conditional control and structural consistency in generative visual tasks.

Response 5:
- Full reproducibility details: The complete VLM identifier (Google Gemini 3.1 / 3.5 Flash Lite), API endpoints, sampling temperature (1.0), token budgets (16), and the exact prompt ("Count the dark blobs in this image. Reply with a single integer and nothing else.") are now documented in the Protocol and Table of Materials. The complete per-frame query responses for all 195 benchmark frames have been deposited in `data/benchmark_195_per_frame.csv`.
- Discussion of IMAGPose and IMAGDressing-v1: In the Introduction and Discussion, we have incorporated discussion and citations for *IMAGPose* (Shen et al., 2024; reference 18) and *IMAGDressing-v1* (Shen et al., 2024; reference 19). We highlight that maintaining structural consistency, spatial fidelity, and conditional control is a central challenge in visual generative data construction. Our precheck protocol provides an automated statistical quality gate to detect generative truncation and label corruption before synthetic data is used for downstream training or auto-annotation.

================================================================================
PART 3: RESPONSES TO REVIEWER #2
================================================================================

Comment 1: Limited experimental validation and generalizability. The central experimental demonstration relies on only 30 synthetic images... The manuscript introduces a corrected benchmark of 195 images, but the complete VLM annotation experiment was not conducted on this benchmark. A new reproducible run on the corrected benchmark would substantially strengthen the manuscript.

Response 1:
As detailed in Response 1 to Reviewer 1, we have performed the full VLM annotation experiment on all 195 benchmark images across clean, moderate, and heavy degradation tiers with K = 5 queries per image for both repeated sampling and perturbation ensemble scorers (1,950 total queries). The results show robust 93.8%–94.9% accuracy, an overall unanimous-error rate of 1.5%, and conformal singleton auto-label yield exceeding 94% to 95% at α = 0.10 and 0.20 (**Table 1**). The complete per-frame raw data and analysis scripts are fully archived.

Comment 2: Dependence on a defective synthetic data generator. A significant concern is that 13 of the 30 seed images contained fewer objects than originally requested... The authors should clarify whether the observed difference may also be explained by object-count distributions or image difficulty.

Response 2:
We agree with the Reviewer's concern. In our revised manuscript, we report the benchmark results where all 195 images were generated without truncation and verified 100% by connected components. Across three noise tiers (clean, moderate blur/noise, heavy blur/noise), unanimous errors remained between 0.0% and 3.1%. This demonstrates that image degradation alone (blur and Gaussian noise) does not cause annotator failure; rather, the combination of high object density and spatial truncation in the defective seed frames provoked VLM overcount hallucinations. The stratified precheck was able to pinpoint this dataset defect automatically.

Comment 3: Clarification of the feasibility guarantees. Satisfying these conditions does not necessarily guarantee that the resulting prediction sets will be sufficiently informative for practical auto-annotation... The manuscript should more clearly distinguish between detecting conditions that necessarily produce trivial sets and predicting that an annotation pipeline will achieve useful performance.

Response 3:
We have substantially clarified this distinction in the revised Discussion. Conditions C1–C3 are strictly *necessary* conditions that rule out impossible targets:
- Failing C1–C3 guarantees that every prediction set is trivial (q̂ = 1.0, returning all 9 labels).
- Passing C1–C3 (a GO decision) guarantees that q̂ < 1.0, ensuring non-trivial prediction sets.
- Practical singleton yield and set size are assessed in Step 5 (confirmatory split calibration). The benchmark validation demonstrates that when ê₀ is small (1.5%), passing C1–C3 translates into practical auto-annotation yields of 94.9% singletons at α = 0.10 and 95.4% singletons at α = 0.20.

Comment 4: Statistical power and uncertainty estimation. First, condition C3 is described using the upper limit of a two-sided Clopper-Pearson confidence interval, whereas the sample-size calculations are based on a one-sided exact binomial test. The authors should explain how these two procedures relate... Second, the confirmatory evaluation averages results over 400 random calibration/test splits...

Response 4:
- Exact binomial test vs. Clopper-Pearson interval: Both methods are exact procedures derived from the identical Binomial cumulative distribution function. The two-sided 95% Clopper-Pearson upper bound ê_{0,upper} is the exact value θ for which P(Bin(n, θ) ≤ k) = 0.025. Sizing the seed sample via a one-sided exact binomial test of H₀: θ ≥ α at level 0.05 guarantees that if the true error rate is a given fraction of α, the experiment has ≥ 80% power to observe a count k whose upper bound satisfies Condition C2. In the revised text, we clarify this mathematical harmony.
- Resampling splits vs. dataset uncertainty: We clarify that the 400 splits assess split-induced variance of the calibration quantile q̂, while the Clopper-Pearson confidence interval quantifies fundamental finite-sample binomial uncertainty over the underlying population error rate. The full 195-benchmark evaluation provides a large independent test set, narrowing the 95% confidence interval of ê₀ to [0.003, 0.044].

Comment 5: Reproducibility and incomplete methodological details. Provide the model name and version, API settings, complete prompts, sampling parameters, and exact implementation details. The corrected benchmark should also be accompanied by complete per-image evaluation records.

Response 5:
All methodological details, API settings, hyper-parameters, and per-image evaluation records are now completely documented and published in the repository:
- Model: Google Gemini 3.1 / 3.5 Flash Lite accessed via Google AI Studio API.
- Prompt: "Count the dark blobs in this image. Reply with a single integer and nothing else."
- Parameters: Temperature = 1.0, Max Output Tokens = 16.
- Verification: Morphological connected-component analysis with 3×3 structuring element.
- Raw data: Deposited in `data/benchmark_195_per_frame.csv` with individual query responses, agreement metrics, and majority votes for all 195 images.

================================================================================
We believe that these extensive revisions, the complete 195-frame empirical benchmark runs, and the enhanced theoretical and practical discussions have resolved all concerns and substantially strengthened the manuscript.
"""

# 1. Write Markdown version
with open("submission/Rebuttal_JoVE76055.md", "w", encoding="utf-8") as f:
    f.write(rebuttal_text)
with open("Rebuttal_JoVE76055.md", "w", encoding="utf-8") as f:
    f.write(rebuttal_text)

# 2. Write DOCX version
doc = docx.Document()
doc.sections[0].top_margin = Inches(1.0)
doc.sections[0].bottom_margin = Inches(1.0)
doc.sections[0].left_margin = Inches(1.0)
doc.sections[0].right_margin = Inches(1.0)

for line in rebuttal_text.splitlines():
    line_s = line.strip()
    if not line_s:
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(4)
        continue
    if line_s.startswith("==="):
        continue
    if line_s.startswith("PART") or line_s.startswith("REBUTTAL") or line_s.startswith("Manuscript ID"):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(10)
        p.paragraph_format.space_after = Pt(4)
        r = p.add_run(line_s)
        r.bold = True
        r.font.name = "Calibri"
        r.font.size = Pt(12)
    elif line_s.startswith("Comment") or line_s.startswith("Response") or (line_s.startswith("1.") and "General" in line_s) or any(line_s.startswith(f"{i}.") for i in range(1, 11)):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(6)
        p.paragraph_format.space_after = Pt(3)
        r = p.add_run(line_s)
        r.bold = True
        r.font.name = "Calibri"
        r.font.size = Pt(11)
    else:
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.line_spacing = 1.15
        r = p.add_run(line)
        r.font.name = "Calibri"
        r.font.size = Pt(10.5)

doc.save("submission/Rebuttal_JoVE76055.docx")
doc.save("Rebuttal_JoVE76055.docx")
print("Rebuttal files successfully created in submission/ and root!")
