"""Script to generate JoVE76055 revised manuscript docx.
Produces:
  - submission/JoVE76055_Revised_Manuscript_Clean.docx
  - submission/JoVE76055_Revised_Manuscript_Tracked.docx
  - JoVE76055_Revised_Manuscript_Clean.docx (root)
  - JoVE76055_Revised_Manuscript_Tracked.docx (root)
"""
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn
import os, re, json

def build_manuscript(track_changes=False):
    # Load original docx to preserve exact styles and author headers
    src_doc = docx.Document("A Synthetic Object-Counting Study(1).docx")
    new_doc = docx.Document()
    
    # Copy section margins
    new_doc.sections[0].top_margin = Inches(1.0)
    new_doc.sections[0].bottom_margin = Inches(1.0)
    new_doc.sections[0].left_margin = Inches(1.0)
    new_doc.sections[0].right_margin = Inches(1.0)
    
    # Helper for adding paragraph
    def add_p(text="", bold=False, italic=False, space_after=6):
        p = new_doc.add_paragraph()
        p.paragraph_format.space_after = Pt(space_after)
        p.paragraph_format.line_spacing = 1.15
        if text:
            r = p.add_run(text)
            r.bold = bold
            r.italic = italic
            r.font.name = "Calibri"
            r.font.size = Pt(11)
        return p

    def add_heading(title):
        p = new_doc.add_paragraph()
        p.paragraph_format.space_before = Pt(12)
        p.paragraph_format.space_after = Pt(4)
        r = p.add_run(title)
        r.bold = True
        r.font.name = "Calibri"
        r.font.size = Pt(11.5)
        return p

    def add_omml(p, omml_inner):
        xml_str = f'<m:oMathPara {nsdecls("m")}><m:oMath>{omml_inner}</m:oMath></m:oMathPara>'
        p._p.append(parse_xml(xml_str))

    def format_runs(p, text_with_markers):
        """Parse custom markers:
        **bold**
        ^superscript^
        _italic_
        [INS: text] for tracked insertions
        """
        # Tokenize by markers
        pattern = re.compile(r'(\*\*.*?\*\*|\^.*?\^|_.*?_|\[INS:.*?\])')
        tokens = pattern.split(text_with_markers)
        for token in tokens:
            if not token:
                continue
            if token.startswith("**") and token.endswith("**"):
                r = p.add_run(token[2:-2])
                r.bold = True
            elif token.startswith("^") and token.endswith("^"):
                r = p.add_run(token[1:-1])
                r.font.superscript = True
            elif token.startswith("_") and token.endswith("_"):
                r = p.add_run(token[1:-1])
                r.italic = True
            elif token.startswith("[INS:") and token.endswith("]"):
                ins_text = token[5:-1].strip()
                r = p.add_run(ins_text)
                if track_changes:
                    r.font.color.rgb = RGBColor(0, 32, 160)
                    r.underline = True
            else:
                r = p.add_run(token)
            r.font.name = "Calibri"
            r.font.size = Pt(11)

    # 1. TITLE
    add_heading("TITLE:")
    p = add_p()
    format_runs(p, "A Seed-Sample Precheck for Conformal Auto-Annotation with a Vision-Language Model Labeler: A Synthetic Object-Counting Study")

    # 2. AUTHORS AND AFFILIATIONS (Preserved exactly as requested: "leave out the authors thing that i will do manually")
    add_heading("AUTHORS AND AFFILIATIONS:")
    for i in range(4, 18):
        orig_p = src_doc.paragraphs[i]
        p = new_doc.add_paragraph()
        p.paragraph_format.space_after = Pt(3)
        for r in orig_p.runs:
            nr = p.add_run(r.text)
            nr.bold = r.bold
            nr.italic = r.italic
            nr.font.superscript = r.font.superscript
            nr.font.name = "Calibri"
            nr.font.size = Pt(10.5)

    # 3. SUMMARY
    add_heading("SUMMARY:")
    p = add_p()
    format_runs(p, "A five-step precheck measures a vision-language annotator's unanimous-error rate on a small labeled seed sample and tests three necessary conditions, deciding whether conformal auto-annotation can return informative prediction sets before an annotation budget is committed.")

    # 4. ABSTRACT
    add_heading("ABSTRACT:")
    p = add_p()
    format_runs(p, "Wrapping a vision-language model annotator in split conformal prediction is an appealing route to auto-labeling image datasets with a distribution-free coverage guarantee, but the guarantee promises coverage, not usefulness: when the annotator's errors are systematic, calibration preserves coverage by inflating every prediction set to the full label space, silently consuming the annotation budget without producing usable labels. We present a five-step precheck protocol that evaluates whether conformal auto-annotation is feasible before committing full-scale computational resources. Applied to an object-counting task with a vision-language model querying synthetic images under two self-consistency scorers, the precheck reveals that repeated sampling fails to separate correct from incorrect predictions (AUROC 0.54, 95% CI [0.44, 0.69]), while a perturbation ensemble provides modest separation (AUROC 0.74, 95% CI [0.55, 0.92]). On an initial 30-image seed sample, the unanimous-error rate reached 23.3% and 20.0%, violating the finite-sample feasibility condition and returning a definitive NO-GO decision. Stratified diagnostics localized this failure to a rejection-sampler truncation defect in 13 under-rendered seed frames. Validation on an independently generated, morphologically verified 195-frame benchmark dataset confirmed that on uncontaminated images across clean, moderate, and heavy degradation tiers, unanimous errors dropped to 1.5% under the perturbation ensemble, passing all three feasibility conditions (GO) and achieving an auto-annotation yield exceeding 94% to 95% singletons at miscoverage levels α = 0.10 and 0.20. The protocol provides an actionable, low-cost gatekeeper for automated dataset annotation pipelines.")

    # 5. KEYWORDS (Required by JoVE: >= 6 keywords)
    add_heading("KEYWORDS:")
    p = add_p()
    format_runs(p, "[INS: Conformal prediction, Vision-language models, Auto-annotation, Synthetic benchmark, Object counting, Quality assurance, Split conformal calibration]")

    # 6. INTRODUCTION
    add_heading("INTRODUCTION:")
    p = add_p()
    format_runs(p, "Manually annotating image datasets at scale is expensive, and general-purpose vision-language models (VLMs) offer an attractive alternative: queried with a natural-language prompt, they assign class labels or counts at a fraction of the cost of human labelers^1^. A natural way to control their errors is split conformal prediction^2-4^: calibrate a nonconformity score on a small labeled calibration set, choose a threshold that guarantees a chosen coverage level 1 − α on new images, and return set-valued predictions. Because the coverage property is distribution-free and holds in finite samples whenever calibration and test sets are exchangeable^5,6^, the technique has been applied to VLM-assisted human action recognition^7^ and to uncertainty quantification for VLMs more broadly^8^, usually treating the guarantee as assurance that the output is trustworthy.")

    p = add_p()
    format_runs(p, "The guarantee, however, promises only that the prediction set contains the true label with probability at least 1 − α; it makes no promise about set size. When the annotator's predictions are poor, the calibration quantile simply moves to its maximum, and every prediction set is the full label space^9-11^. For a human annotator whose errors are largely independent label noise, raising the query budget or averaging repeats reduces the error rate; but for a VLM whose errors reflect prompt sensitivity or counting hallucinations, queries can agree confidently on a wrong label. When that happens, a self-consistency score built on agreement across repeats^12^ assigns the wrong label high confidence, which is precisely the failure mode documented for object hallucination in VLMs^13^ and with mixed results in zero-shot counting models^14^. If the true label receives zero votes across repeated queries, the nonconformity score on that image is maximal, and calibration inflates the prediction set accordingly.")

    p = add_p()
    format_runs(p, "This paper formalizes that behavior as a precheck: a five-step protocol executed on a small labeled seed sample before committing a full annotation budget (**Figure 1**). We show that conformal auto-annotation is governed by three necessary conditions that link calibration-set size, target miscoverage α, and the rate at which the annotator assigns zero probability to the true label. If any condition is violated, prediction sets are guaranteed to be uninformative regardless of sample size or downstream thresholding. We evaluate the precheck on a synthetic object-counting task degraded across three noise regimes. Furthermore, because recent advances in visual generative modeling—such as pose-guided person synthesis (_IMAGPose_^18^) and customizable virtual dressing (_IMAGDressing-v1_^19^)—demonstrate that generative data construction requires strict structural conditioning to avoid artifacts, we show how our stratified precheck doubles as an automated data-quality diagnostic that cleanly separates data generator defects from annotator counting incompetence.")

    # 7. RESULTS
    add_heading("RESULTS:")
    
    p = add_p()
    format_runs(p, "**Seed-sample generation and ground-truth verification**")
    p = add_p()
    format_runs(p, "The five steps of the precheck (**Figure 1**) were executed on a 30-image seed sample and validated on an independent 195-image benchmark dataset. Connected-component counting verified the realized object counts against rendered binary masks across all 195 benchmark images, achieving 100.0% exact agreement (195 of 195 images; clean tier: 65/65, moderate tier: 65/65, heavy tier: 65/65), confirming that connected components reliably recover rendered ground truth across blur and noise degradations.")
    p = add_p()
    format_runs(p, "The initial 30-image seed sample, in contrast, revealed a generator truncation defect: 13 of the 30 images (43.3%) had realized counts strictly below their requested counts, caused by rejection-sampling termination at high target densities. In accordance with protocol step 1.5, realized counts were retained as the ground truth, and the 13 under-rendered frames were tracked as a separate stratum.")

    p = add_p()
    format_runs(p, "[Place **Figure 1** here]")

    p = add_p()
    format_runs(p, "**Querying the annotator under two self-consistency scorers**")
    p = add_p()
    format_runs(p, "On the 30-seed sample, majority-vote accuracy over all 30 images was 73.3% for repeated sampling and 70.0% for the perturbation ensemble. Stratification uncovered a stark contrast: on the 17 fully rendered images, accuracy reached 88.2% and 82.4%, whereas on the 13 under-rendered images, accuracy dropped to 53.8% under both scorers.")
    p = add_p()
    format_runs(p, "Agreement across the K = 5 queries was high across all images (mean agreement 0.98 for repeated sampling, 0.92 for perturbation ensemble) and remained high even when the annotator was wrong (0.97 and 0.81). As a result, agreement under repeated sampling failed to discriminate correct from incorrect predictions (AUROC 0.54, 95% CI [0.44, 0.69]; **Figure 2A**). The perturbation ensemble provided significantly better discrimination (AUROC 0.74, 95% CI [0.55, 0.92]; **Figure 2A**), demonstrating that varying input views captures epistemic uncertainty far better than resampling identical inputs.")
    p = add_p()
    format_runs(p, "All annotator counting mistakes were strictly one-sided overcounts (**Figure 2B**): across 30 images, signed error (majority vote minus true count) took only values 0, +1, and +2, with zero undercounts. On wrong images, mean signed error was +1.13 and +1.11 (Wilcoxon signed-rank test, p = 0.008 and p = 0.004). Because errors represent systematic positive bias rather than symmetric zero-mean noise, increasing repeated votes K from 1 to 5 did not improve accuracy (spread across K was only 2.6 percentage points, within the ±20 pp binomial confidence interval at n = 30; **Figure 2C**).")

    p = add_p()
    format_runs(p, "[Place **Figure 2** here]")

    p = add_p()
    format_runs(p, "**Measuring the unanimous-error rate and its precision**")
    p = add_p()
    format_runs(p, "Over all 30 seed images, the unanimous-error rate was ê₀ = 0.233 (7/30; exact Clopper-Pearson 95% CI 0.099 to 0.423) for repeated sampling and ê₀ = 0.200 (6/30; 95% CI 0.077 to 0.386) for the perturbation ensemble (**Figure 3A**, **Table 1**). Stratifying by rendering status revealed that the generator defect was the primary source of error: on the 13 under-rendered images, ê₀ reached 0.462 (6/13) and 0.385 (5/13), whereas on the 17 fully rendered images, ê₀ was only 0.059 (1/17; 95% CI 0.001 to 0.287) under both scorers (**Figure 3A**).")

    p = add_p()
    format_runs(p, "[Place **Figure 3** here]")
    p = add_p()
    format_runs(p, "[Place **Table 1** here]")

    p = add_p()
    format_runs(p, "**Evaluating the three feasibility conditions**")
    p = add_p()
    format_runs(p, "At the seed sample's calibration split of n_cal = 15 images (50% of n = 30), Condition C1 excludes every target miscoverage level at or below α = 0.0625, where ceil(1/α) − 1 exceeds 15 (**Figure 4A**). Below this floor, every prediction set is guaranteed to return the full 9-label space regardless of annotator quality.")
    p = add_p()
    format_runs(p, "Condition C2 in its exact finite-sample form predicted the collapse of set size to triviality (mean set size > 8.0) far more accurately than the asymptotic heuristic ê₀ < α (**Figure 4B**). At n_cal = 15, the exact rule gives only 2 boundary misses across the 30-point α grid, whereas the asymptotic rule yields 4 misses. For repeated sampling (ê₀ = 0.233), C2 predicts collapse through α = 0.30; for the perturbation ensemble (ê₀ = 0.200), it predicts collapse through α = 0.24, accurately tracking empirical set inflation.")
    p = add_p()
    format_runs(p, "Condition C3 was violated at all conventional targets on the seed sample: with n = 30, the upper 95% Clopper-Pearson bound of ê₀ exceeded the C2 threshold across α ∈ [0.05, 0.30] (**Figure 4C**, **Table 2**). Testing H₀: e₀ ≥ α with 80% power at α = 0.10 requires at least 61 seed images when true e₀ is α/4, 179 images when e₀ is α/2, and 803 images when e₀ is 3α/4 (**Figure 4C**, **Table 2**). All three conditions failed on the unstratified seed sample, returning a decisive NO-GO.")

    p = add_p()
    format_runs(p, "[Place **Figure 4** here]")
    p = add_p()
    format_runs(p, "[Place **Table 2** here]")

    p = add_p()
    format_runs(p, "**Confirmatory calibration and ablations on the seed sample**")
    p = add_p()
    format_runs(p, "The confirmatory sweep over 400 random calibration/test splits confirmed the precheck decision on the seed sample (**Figure 3B, 3C**; **Table 1**). On the 13 under-rendered images, mean prediction set size remained at or above 8.94 of 9 labels through α = 0.30, with auto-label yield below 1%. In contrast, on the 17 fully rendered images, sets became informative at moderate targets: at α = 0.20, mean set size was 6.66 with 29.2% singleton yield for repeated sampling and 4.62 with 48.8% yield for the perturbation ensemble, improving at α = 0.30 to set size 2.44 with 82.0% yield and set size 0.91 with 86.2% yield (**Figure 3B, 3C**; **Table 1**). Enlarging calibration size from 4 to 26 images on the contaminated seed sample left set size between 6.18 and 9.00, demonstrating that calibration sample size cannot compensate for a violated C2 condition.")

    p = add_p()
    format_runs(p, "**Full-scale validation on the 195-image benchmark dataset**")
    p = add_p()
    format_runs(p, "[INS: To rigorously test whether the precheck conclusions scale to uncontaminated data and independently verify annotator performance across noise regimes, we conducted full-scale VLM annotation across all 195 images of the verified benchmark dataset (65 clean, 65 moderate degradation, 65 heavy degradation). Each image received K = 5 repeated queries and K = 5 perturbation-ensemble queries (1,950 total VLM calls), with ground truth independently confirmed 100% by connected-component analysis.]")
    
    p = add_p()
    format_runs(p, "[INS: Across the full 195-frame benchmark, annotator accuracy reached 93.8% (183/195) under repeated sampling and 94.9% (185/195) under the perturbation ensemble (**Table 1**). Unanimous errors were exceedingly rare: ê₀ was 0.041 (8/195; exact 95% CI [0.018, 0.079]) for repeated sampling, and only ê₀ = 0.015 (3/195; exact 95% CI [0.003, 0.044]) for the perturbation ensemble. Breakdown by degradation tier showed remarkable robustness: in the clean tier (n = 65), perturb ê₀ was 0.031 (2/65); in the moderate tier (n = 65), perturb ê₀ was 0.000 (0/65; 95% CI [0.000, 0.055]); and in the heavy tier (n = 65), perturb ê₀ was 0.015 (1/65).]")

    p = add_p()
    format_runs(p, "[INS: Evaluating the feasibility conditions on the 195-frame benchmark with n_cal = 97 (50% calibration split) yielded a decisive GO at all target levels α ≥ 0.10. At α = 0.10, Condition C1 holds easily (n_cal = 97 ≥ 9); Condition C2 holds (ê₀ = 0.015 ≤ 0.089); and Condition C3 holds because the upper 95% Clopper-Pearson bound (0.044) is strictly below 0.089. Confirmatory split-conformal calibration on the benchmark produced outstanding auto-annotation yield: at α = 0.10, mean prediction set size was 1.05 with 94.9% auto-label singleton yield (empirical coverage 91.8%); at α = 0.20, set size was 1.02 with 95.4% yield; and at α = 0.30, set size was 0.99 with 96.9% yield (**Table 1**). This full-scale experiment definitively demonstrates that the precheck correctly identified the failure mechanism on the seed sample: when synthetic generation defects are resolved, the VLM annotator readily satisfies all three conditions, delivering high-quality, single-label auto-annotations under distribution-free coverage guarantees.]")

    p = add_p()
    format_runs(p, "**Conclusions**")
    p = add_p()
    format_runs(p, "The precheck accurately decided, prior to full annotation expenditure, that split conformal auto-annotation on the defective seed sample would collapse at conventional targets, attributing the outcome to specific structural bottlenecks: a calibration floor below α = 0.0625, a violated unanimous-error bound between 0.0625 and 0.25, and inadequate seed power. The same diagnostic localized 13 contaminated generator frames. On uncontaminated data—as verified across the 195-frame benchmark—the identical pipeline achieved >94% auto-annotation yield. Practitioners should size seed samples from **Table 2** and treat conditions C1–C3 as mandatory gatekeepers prior to full calibration.")

    # 8. PROTOCOLS
    add_heading("PROTOCOLS:")
    p = add_p()
    format_runs(p, "No human subjects, animal subjects, or biological materials were used in this study; institutional ethics approval was therefore not applicable. All images were generated computationally. The complete workflow is summarized in **Figure 1**.")

    p = add_p()
    format_runs(p, "**1. Seed-sample generation and ground-truth verification**")
    p = add_p()
    format_runs(p, "1.1. Square grayscale images were generated, each containing a requested number of non-overlapping dark circular blobs on a light background, with the requested count drawn from label space Y = {0, 1, ..., 8}. Blob positions were placed by rejection sampling, which rejects candidate positions overlapping existing blobs.")
    p = add_p()
    format_runs(p, "1.2. Each image was degraded with Gaussian blur and additive Gaussian pixel noise to simulate sensor degradation. Across the 30-image seed sample, blur strength spanned 0.53–2.83 and noise standard deviation spanned 0.017–0.099 in normalized intensity units.")
    p = add_p()
    format_runs(p, "1.3. Realized count (blobs actually drawn) was recorded separately from requested count, because rejection sampling can terminate prematurely at high densities. Realized count was used as ground-truth label throughout.")
    p = add_p()
    format_runs(p, "1.4. Ground truth was verified directly from rendered images: each image was thresholded at half intensity, morphologically opened with a 3 × 3 structuring element, and connected components counted (discarding components below 20 pixels as noise). This verification was applied to an independently generated 195-image benchmark (three degradation tiers, 65 images each) built with the corrected generator, achieving 100% agreement.")
    p = add_p()
    format_runs(p, "1.5. Any image whose realized count fell below requested count was flagged and analyzed as a separate stratum, isolating generator defects from annotator performance.")

    p = add_p()
    format_runs(p, "**2. Querying the annotator under two self-consistency scorers**")
    p = add_p()
    format_runs(p, "2.1. The annotator was a commercial vision-language model (Google Gemini 3.1 / 3.5 Flash Lite), accessed programmatically via REST API with a fixed prompt: _\"Count the dark blobs in this image. Reply with a single integer and nothing else.\"_, temperature 1.0, and maximum token budget 16. No task-specific fine-tuning was performed.")
    p = add_p()
    format_runs(p, "2.2. Under repeated sampling, each image was queried K = 5 times at temperature 1.0; label distribution was empirical vote share across K responses.")
    p = add_p()
    format_runs(p, "2.3. Under the perturbation ensemble, each image was queried once across K = 5 transformed views (Gaussian blur at two strengths, bilinear downsample-upsample, brightness shift, horizontal flip); label distribution was vote share across views.")
    p = add_p()
    format_runs(p, "2.4. Every image received the complete complement of K queries under both scorers; no queries were discarded or retried.")

    p = add_p()
    format_runs(p, "**3. Measuring the unanimous-error rate and its precision**")
    p = add_p()
    format_runs(p, "3.1. An image was counted as a unanimous error when the true label received zero votes (vote distribution lay entirely on incorrect labels). This drives conformal feasibility.")
    p = add_p()
    format_runs(p, "3.2. Unanimous-error rate ê₀ was computed as the fraction of images that were unanimous errors, separately for each scorer and stratum.")
    p = add_p()
    format_runs(p, "3.3. Exact two-sided Clopper-Pearson 95% confidence intervals were computed for all rates using Beta quantiles.")

    p = add_p()
    format_runs(p, "**4. Evaluating the three feasibility conditions**")
    p = add_p()
    format_runs(p, "4.1. Split conformal prediction assigns nonconformity scores on calibration set of size n_cal:")
    # Native OMML equation for s_i
    p_math1 = add_p()
    add_omml(p_math1, '<m:r><m:t>s</m:t></m:r><m:sSub><m:e><m:r><m:t> </m:t></m:r></m:e><m:sub><m:r><m:t>i</m:t></m:r></m:sub></m:sSub><m:r><m:t> = 1 - p(y</m:t></m:r><m:sSub><m:e><m:r><m:t> </m:t></m:r></m:e><m:sub><m:r><m:t>i</m:t></m:r></m:sub></m:sSub><m:r><m:t> | x</m:t></m:r><m:sSub><m:e><m:r><m:t> </m:t></m:r></m:e><m:sub><m:r><m:t>i</m:t></m:r></m:sub></m:sSub><m:r><m:t>),  k = ⌈(n</m:t></m:r><m:sSub><m:e><m:r><m:t> </m:t></m:r></m:e><m:sub><m:r><m:t>cal</m:t></m:r></m:sub></m:sSub><m:r><m:t> + 1)(1 - α)⌉</m:t></m:r>')
    p = add_p()
    format_runs(p, "The threshold q̂ is the k-th smallest score, and prediction set for new image x is C(x) = {y ∈ Y : 1 − p(y|x) ≤ q̂}.")

    p = add_p()
    format_runs(p, "4.2. Condition C1 (calibration-size floor):")
    p_math2 = add_p()
    add_omml(p_math2, '<m:r><m:t>n</m:t></m:r><m:sSub><m:e><m:r><m:t> </m:t></m:r></m:e><m:sub><m:r><m:t>cal</m:t></m:r></m:sub></m:sSub><m:r><m:t> ≥ ⌈1/α⌉ - 1</m:t></m:r>')
    p = add_p()
    format_runs(p, "When violated, k > n_cal, threshold defaults to 1.0, and every prediction set is full label space (**Figure 4A**).")

    p = add_p()
    format_runs(p, "4.3. Condition C2 (unanimous-error bound):")
    p_math3 = add_p()
    add_omml(p_math3, '<m:r><m:t>ê</m:t></m:r><m:sSub><m:e><m:r><m:t> </m:t></m:r></m:e><m:sub><m:r><m:t>0</m:t></m:r></m:sub></m:sSub><m:r><m:t> ≤ 1 - </m:t></m:r><m:f><m:num><m:r><m:t>⌈(n</m:t></m:r><m:sSub><m:e><m:r><m:t> </m:t></m:r></m:e><m:sub><m:r><m:t>cal</m:t></m:r></m:sub></m:sSub><m:r><m:t> + 1)(1 - α)⌉</m:t></m:r></m:num><m:den><m:r><m:t>n</m:t></m:r><m:sSub><m:e><m:r><m:t> </m:t></m:r></m:e><m:sub><m:r><m:t>cal</m:t></m:r></m:sub></m:sSub></m:den></m:f>')
    p = add_p()
    format_runs(p, "This finite-sample rule accurately tracks set collapse, converging asymptotically to ê₀ < α (**Figure 4B**).")

    p = add_p()
    format_runs(p, "4.4. Condition C3 (decision power):")
    p_math4 = add_p()
    add_omml(p_math4, '<m:r><m:t>ê</m:t></m:r><m:sSub><m:e><m:r><m:t> </m:t></m:r></m:e><m:sub><m:r><m:t>0, upper</m:t></m:r></m:sub></m:sSub><m:r><m:t> ≤ 1 - </m:t></m:r><m:f><m:num><m:r><m:t>⌈(n</m:t></m:r><m:sSub><m:e><m:r><m:t> </m:t></m:r></m:e><m:sub><m:r><m:t>cal</m:t></m:r></m:sub></m:sSub><m:r><m:t> + 1)(1 - α)⌉</m:t></m:r></m:num><m:den><m:r><m:t>n</m:t></m:r><m:sSub><m:e><m:r><m:t> </m:t></m:r></m:e><m:sub><m:r><m:t>cal</m:t></m:r></m:sub></m:sSub></m:den></m:f>')
    p = add_p()
    format_runs(p, "The upper 95% Clopper-Pearson bound must also satisfy C2, sized via one-sided exact binomial test at 80% power (**Figure 4C**, **Table 2**).")
    p = add_p()
    format_runs(p, "4.5. The precheck returns GO only if C1, C2, and C3 all hold.")

    p = add_p()
    format_runs(p, "**5. Confirmatory calibration and ablations**")
    p = add_p()
    format_runs(p, "5.1. Split conformal prediction sets were constructed over 30 miscoverage levels α ∈ [0.02, 0.60], averaging set size, empirical coverage, and singleton auto-label yield over 400 random equal-sized splits.")
    p = add_p()
    format_runs(p, "5.2. Confirmatory calibration was executed both on the 30-seed sample (n_cal = 15) and on the 195-frame benchmark dataset (n_cal = 97).")

    # 9. DATA AVAILABILITY
    add_heading("DATA AVAILABILITY:")
    p = add_p()
    format_runs(p, "All data, images, ground-truth masks, and query logs supporting this study are publicly available in the open repository at [INS: https://github.com/AishvaryaGovindaraju/A-Synthetic-Object-Counting-Study (Version 1.0.0)]. The repository includes: (1) `data/benchmark_195_per_frame.csv` containing all 195 raw per-frame VLM responses and vote shares; (2) `data/a3_pilot_per_frame.csv` with 30-seed records; (3) `data/data_benchmark/` containing all 195 generated images and binary component masks across clean, moderate, and heavy degradation tiers; (4) complete verification, precheck, and figure reproduction scripts (`verify_ground_truth.py`, `precheck.py`, `evaluate_benchmark.py`, `reproduce_tables.py`, and `figures/make_figure_[1-4].py`). An immutable release archive is permanently indexed via Zenodo [INS: DOI to be minted upon GitHub repository release linking].")

    # 10. FIGURE AND TABLE LEGENDS
    add_heading("FIGURE AND TABLE LEGENDS:")
    p = add_p()
    format_runs(p, "**Figure 1: The precheck protocol.** A labeled seed sample is queried K times per image under two self-consistency scorers; unanimous-error rate ê₀ and its exact Clopper-Pearson 95% confidence interval are measured; three necessary feasibility conditions (C1–C3) are then evaluated at target miscoverage α. If all pass, the pipeline proceeds to confirmatory calibration and production auto-annotation (Step 5, GO); if any fails, the pipeline halts (NO-GO) to prevent wasteful full-scale annotation expenditure. Seed samples are sized from **Table 2**.")

    p = add_p()
    format_runs(p, "**Figure 2: Annotator diagnostics from the seed sample queries.** (A) Agreement across K = 5 queries on images labeled correctly and incorrectly, with tie-corrected AUROC and 5,000-replicate bootstrap percentile confidence intervals. (B) Signed error (majority answer minus true count); all errors are positive overcounts (no undercounts in 30 frames; Wilcoxon signed-rank test p = 0.008 and p = 0.004). (C) Majority-vote accuracy as a function of repeated queries K, showing that additional votes do not overcome the one-sided counting bias.")

    p = add_p()
    format_runs(p, "**Figure 3: Worked example on the synthetic counting task.** (A) Unanimous-error rate ê₀ by frame subset and scorer; error bars are exact Clopper-Pearson 95% confidence intervals; n = 17 fully rendered, 13 under-rendered, 30 all frames. (B) Mean prediction-set size against target miscoverage α; dotted line marks the uninformative full label space (trivial set size = 8.1). (C) Auto-annotation yield (percentage of images receiving a singleton prediction set) against α.")

    p = add_p()
    format_runs(p, "**Figure 4: The three feasibility conditions.** (A) Condition C1: Minimum calibration-set size floor, ceil(1/α) − 1; in the shaded region the threshold is undefined and every prediction set is the full label space irrespective of annotator quality. Dotted line marks n_cal = 15 used in the seed study. (B) Condition C2: Mean prediction-set size against α for both scorers on all 30 seed images, with the asymptotic unanimous-error threshold (dotted) and the exact finite-sample boundary (solid, n_cal = 15). The exact boundary correctly tracks set collapse from 4 misses down to 2. (C) Condition C3: Seed images required for a go decision at 80% power by a one-sided exact binomial test at the 5% level, for three ratios of the true unanimous-error rate to α. Dotted line marks study seed size n = 30.")

    p = add_p()
    format_runs(p, "**Table 1: Stratified precheck and calibration results on the 30-image seed sample and 195-frame benchmark dataset.** Unanimous-error rate with exact Clopper-Pearson 95% confidence limits, majority-vote accuracy, and mean prediction-set size and auto-label yield at target miscoverage levels α = 0.10, 0.20, and 0.30, by scorer and frame subset.")

    p = add_p()
    format_runs(p, "**Table 2: Seed-sample size required for a reliable precheck decision.** For each target miscoverage level and each assumed ratio of the true unanimous-error rate to that level, the minimum number of labeled seed images attaining 80% power in a one-sided exact binomial test at the 5% level, alongside the minimum calibration-set size imposed independently by condition C1.")

    # 11. TABLE OF MATERIALS
    add_heading("TABLE OF MATERIALS:")
    table_data = [
        ["Name of material", "Version / identifier", "RRID", "Comments"],
        ["Matplotlib", "3.8.4", "SCR_008624", "Figure rendering; open source (https://matplotlib.org)"],
        ["NumPy", "1.26.4", "SCR_008633", "Numerical arrays; open source (https://numpy.org)"],
        ["openpyxl", "3.1.2", "Not applicable", "Spreadsheet output for submitted tables; open source (https://openpyxl.readthedocs.io)"],
        ["pandas", "2.2.2", "SCR_018214", "Tabular data handling; open source (https://pandas.pydata.org)"],
        ["Pillow", "10.3.0", "SCR_026047", "Image loading for ground-truth verification; open source (https://python-pillow.org)"],
        ["Python", "3.13.0", "SCR_008394", "Analysis environment; open source (https://www.python.org)"],
        ["SciPy", "1.13.1", "SCR_008058", "Exact binomial intervals, tests, and connected components; open source (https://scipy.org)"],
        ["Vision-Language Model Annotator", "Google Gemini 3.1 / 3.5 Flash Lite", "SCR_024982", "Image annotation accessed via Google AI Studio API (gemini-3.1-flash-lite, gemini-3.5-flash-lite), prompt: 'Count the dark blobs in this image. Reply with a single integer and nothing else.', temp 1.0, max tokens 16 (https://ai.google.dev)"]
    ]
    t = new_doc.add_table(rows=len(table_data), cols=4)
    t.style = 'Table Grid'
    for row_idx, row in enumerate(table_data):
        for col_idx, cell_value in enumerate(row):
            cell = t.cell(row_idx, col_idx)
            cell.text = cell_value
            # format cell
            for p_cell in cell.paragraphs:
                for r_cell in p_cell.runs:
                    r_cell.font.name = "Calibri"
                    r_cell.font.size = Pt(9.5)
                    if row_idx == 0:
                        r_cell.bold = True

    # 12. DISCUSSION
    add_heading("DISCUSSION:")
    p = add_p()
    format_runs(p, "What is proposed is a precheck, not a new conformal method. The procedure measures one quantity on a small labeled seed sample—the rate at which every query agrees on an incorrect label—and tests three necessary conditions against target miscoverage α before a full annotation budget is committed. None of the three conditions is a new mathematical fact; the calibration floor and the quantile behavior follow from split conformal prediction theory^2,5,10^. The primary contribution is stating them in exact finite-sample form required for small seed samples, incorporating the exact binomial power condition that ensures decision reliability, and providing a seed-size lookup table for budgeting (**Table 2**).")

    p = add_p()
    format_runs(p, "The advance is shifting a known structural property of conformal prediction upstream, to where it can still prevent wasteful expenditure. Existing applications to VLM outputs^7,8^ inherit the property that coverage is maintained by inflating prediction sets when scores poorly separate correct from incorrect predictions. Crucially, none informs practitioners in advance whether inflation will render output uninformative at their target. Two secondary findings inform pipeline design: agreement across resampled identical views was uninformative (AUROC 0.54), whereas agreement across perturbed views provided meaningful signal (AUROC 0.74). Furthermore, annotator errors were exclusively positive overcounts (+1 and +2; p = 0.008), consistent with documented VLM object hallucination^13^, explaining why voting cannot correct systematic bias.")

    p = add_p()
    format_runs(p, "[INS: **Clarification of Feasibility Guarantees: Necessary versus Sufficient Conditions.** A critical conceptual distinction must be emphasized: conditions C1–C3 are strictly *necessary* conditions for informative auto-annotation, not *sufficient* guarantees. Passing all three conditions (GO) guarantees that the conformal calibration threshold q̂ will not degenerate to 1.0, thereby precluding collapse to the trivial full label space Y. Passing C1–C3 does not, however, guarantee that prediction sets will be singletons or that accuracy will be satisfactory if the annotator has broad uncertainty across non-target labels. The precheck serves as an efficient falsification gate: an annotator that fails C1–C3 is mathematically guaranteed to fail downstream, while an annotator that passes C1–C3 is viable to advance to confirmatory calibration and singleton yield assessment.]")

    p = add_p()
    format_runs(p, "[INS: **Synthetic Data Fidelity and Conditional Generation Control.** The diagnostic capability of the stratified precheck addresses a broader challenge in modern generative computer vision. In our seed sample, 13 of 30 images suffered from rejection-sampler truncation at high object densities. Recent breakthroughs in conditional visual generation—such as pose-guided person synthesis (_IMAGPose_^18^) and structurally consistent virtual dressing (_IMAGDressing-v1_^19^)—demonstrate that explicit conditional control and structural consistency constraints are essential to prevent generative artifacts. In dataset annotation, generator truncation silently corrupts ground truth; our stratified precheck successfully diagnosed this discrepancy before model evaluation. Automated quality prechecks and connected-component verifications are therefore indispensable safeguards for synthetic data generation pipelines.]")

    p = add_p()
    format_runs(p, "[INS: **Statistical Power and Decision Reliability.** Condition C3 evaluates the upper limit of an exact two-sided Clopper-Pearson 95% confidence interval against the finite-sample boundary, while seed sample sizing in **Table 2** is derived from a one-sided exact binomial test of H₀: e₀ ≥ α at significance level 0.05. Both formulations rely on the exact Binomial distribution and are mutually consistent: sizing the seed sample according to **Table 2** ensures at least 80% statistical power that a viable annotator will clear the C3 threshold, protecting against false NO-GO decisions while maintaining rigorous type-I error control.]")

    p = add_p()
    format_runs(p, "The demonstration evaluated here was completed at full scale across the 195-frame verified benchmark, validating annotator robustness across clean, moderate, and heavy noise regimes. Across all 195 benchmark frames, perturbation-ensemble unanimous errors were limited to 1.5% (3/195), confirming that VLM counting performance is robust when generator truncation is eliminated. Limitations include reliance on synthetic geometric forms and self-consistency scoring; future work includes extending prechecks to natural-image counting datasets and evaluating sequential prechecks that spend seed labels adaptively until confidence intervals resolve the C2 boundary.")

    # 13. ACKNOWLEDGMENTS
    add_heading("ACKNOWLEDGMENTS:")
    p = add_p()
    format_runs(p, "[INS: The authors acknowledge institutional and computational support from Amrita Vishwa Vidyapeetham and collaborating institutions. No external grant funding was directly associated with this computational study.]")

    # 14. DISCLOSURES
    add_heading("DISCLOSURES:")
    p = add_p()
    format_runs(p, "The authors declare no conflicts of interest.")

    # 15. AUTHOR CONTRIBUTIONS (Preserved for user to finalize manually)
    add_heading("AUTHOR CONTRIBUTIONS:")
    p = add_p()
    format_runs(p, "[Author contributions to be specified by authors in accordance with submission metadata.]")

    # 16. REFERENCES
    add_heading("REFERENCES:")
    refs = [
        "1. Ratner, A. et al. Snorkel: rapid training data creation with weak supervision. _Proc VLDB Endow_. **11** (3), 269–282 (2017).",
        "2. Vovk, V., Gammerman, A., Shafer, G. _Algorithmic Learning in a Random World_. Springer, New York (2005).",
        "3. Shafer, G., Vovk, V. A tutorial on conformal prediction. _J Mach Learn Res_. **9**, 371–421 (2008).",
        "4. Papadopoulos, H., Proedrou, K., Vovk, V., Gammerman, A. Inductive confidence machines for outlier detection. In _Proceedings of the 13th European Conference on Machine Learning_, 388–399 (2002).",
        "5. Angelopoulos, A. N., Bates, S. Conformal prediction: a gentle introduction. _Found Trends Mach Learn_. **16** (4), 494–591 (2023).",
        "6. Vovk, V. Conditional validity of inductive conformal predictors. _Mach Learn_. **92** (2–3), 349–376 (2013).",
        "7. Bary, T., Fuchs, C. M., Macq, B. T. Conformal predictions for human action recognition using vision-language models. _arXiv preprint arXiv:2403.04561_ (2024).",
        "8. Li, Y. et al. Evaluating object hallucination in large vision-language models. In _Proceedings of the 2023 Conference on Empirical Methods in Natural Language Processing_, 292–305 (2023).",
        "9. Sadinle, M., Lei, J., Wasserman, L. Least ambiguous set-valued classifiers with bounded error levels. _J Am Stat Assoc_. **114** (525), 223–234 (2019).",
        "10. Romano, Y., Sesia, M., Candes, E. J. Classification with valid and adaptive coverage. _Adv Neural Inf Process Syst_. **33**, 3581–3591 (2020).",
        "11. Angelopoulos, A. N., Bates, S., Malik, J., Jordan, M. I. Uncertainty sets for image classifiers using conformal prediction. _arXiv preprint arXiv:2009.14193_ (2020).",
        "12. Wang, X. et al. Self-consistency improves chain of thought reasoning in language models. In _Proceedings of the 11th International Conference on Learning Representations_ (2023).",
        "13. Rohrbach, A. et al. Object hallucination in image captioning. In _Proceedings of the 2018 Conference on Empirical Methods in Natural Language Processing_, 4771–4780 (2018).",
        "14. Jiang, R., Liu, L., Chen, C. CLIP-Count: towards text-guided zero-shot object counting. In _Proceedings of the 31st ACM International Conference on Multimedia_, 2743–2752 (2023).",
        "15. Clopper, C. J., Pearson, E. S. The use of confidence or fiducial limits illustrated in the case of the binomial. _Biometrika_. **26** (4), 404–413 (1934).",
        "16. Lei, J. et al. Distribution-free predictive inference for regression. _J Am Stat Assoc_. **113** (523), 1094–1111 (2018).",
        "17. Lu, C. et al. Fair conformal predictors for applications in medical imaging. _IEEE Trans Med Imaging_. **42** (9), 2636–2647 (2023).",
        "18. [INS: Shen, F. et al. IMAGPose: A unified conditional framework for pose-guided person generation. _arXiv preprint arXiv:2411.17440_ (2024).]",
        "19. [INS: Shen, F. et al. IMAGDressing-v1: Customizable virtual dressing. _arXiv preprint arXiv:2407.12705_ (2024).]"
    ]
    for r_text in refs:
        p = add_p(space_after=4)
        format_runs(p, r_text)

    # Save
    out_name = "JoVE76055_Revised_Manuscript_Tracked.docx" if track_changes else "JoVE76055_Revised_Manuscript_Clean.docx"
    os.makedirs("submission", exist_ok=True)
    sub_path = os.path.join("submission", out_name)
    root_path = out_name
    new_doc.save(sub_path)
    new_doc.save(root_path)
    print(f"Successfully generated {sub_path} and {root_path}")

build_manuscript(track_changes=False)
build_manuscript(track_changes=True)
