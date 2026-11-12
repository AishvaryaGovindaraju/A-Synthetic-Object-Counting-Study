Dear Dr. BARAKABITZE,

Your manuscript, JoVE76055 "A Seed-Sample Precheck for Conformal Auto-Annotation with a Vision-Language Model Labeler: A Synthetic Object-Counting Study," has been editorially and peer reviewed, and the comments below need to be addressed. This includes following the journal’s formatting requirements.

Please track changes within the manuscript to identify all of the edits. When done, log in to the JoVE submission site as an author and upload your revised submission under the heading "Submission Needing Revision". Additionally, upload a rebuttal document that addresses each comment individually.

Your revision is due by Nov 18, 2026.
 
Note that the corresponding author in Editorial Manager is the point of contact during the review.

Best,

Chenwei Xie, Ph.D.

​chenwei.xie@jove.com
Follow us: Facebook | Twitter | LinkedIn
About JoVE
____________________________________



Editorial comments:
General Formatting
• Remove duplicate figure and table legends currently embedded in the Results and retain one complete set under FIGURE AND TABLE LEGENDS.
• Format every in-text Figure and Table citation in bold.
• Remove spaces before superscript reference numbers and place superscript citations before punctuation.
• Complete a final consistency and copyediting check after the scientific revisions are complete.

Authors and Affiliations
• Synchronize all author names, author order, corresponding-author designations, and affiliation markers between the manuscript and submission metadata.
• Resolve the discrepancy between Razaullah Ullah and Razaullah Hafiz Ullah.
• Resolve the discrepancy between Alcardo Alex Alex BARAKABITZE and Alcardo Alex Barakabitze.
• Confirm whether Ateeq Ur Rehman is also a corresponding author and revise the manuscript and submission metadata consistently.
• Provide an institutional email address for Salil Bharany. If an institutional email address is unavailable, explain the exception to the editorial office.

Keywords
• Add at least one relevant indexing term so that the manuscript and submission metadata contain at least six keywords.

Methods
• Use Word’s equation feature for the calibration-threshold equation and the C1–C3 expressions rather than inserting them as malformed plain text.

Results
• After correcting the submitted figure numbering, verify every Results citation against the panel that actually contains the described result.
• In particular, revise the current citation to Figure 3B, 4C for mean set size and auto-label yield so that it points to the correct worked-example and feasibility panels in the final figure set.
• Verify the calibration sample size used in the feasibility analysis and reconcile the conflicting n_cal = 21 and n_cal = 15 values across the Methods, Results, figure, and figure legend.

Data Availability
• Replace ARCHIVED RELEASE DOI, VERSION, and all related placeholders with the final archived release information and an immutable DOI, accession number, or persistent repository identifier.
• Identify the exact repository contents and filenames.

Figures
• Correct the submitted figure attachments so that:
o the annotator-diagnostics image corresponds to Figure 2;
o the worked-example image corresponds to Figure 3;
o the feasibility-conditions image corresponds to Figure 4.
• Update the attachment labels, filenames, panel citations, and legends together so that no mismatches remain.
• In Figure 1, replace both directions to Table 1 with Table 2 if Table 2 contains the intended seed-size requirements.
• Reconcile the four numbered stages shown in Figure 1 with the manuscript’s five-step description by adding, combining, or relabeling the relevant stage so that the schematic and text describe the same workflow.

Tables
• Use the α symbol consistently throughout the tables and manuscript.

Table of Materials
• Replace broad software-version ranges with the exact versions used in the final reported analyses.
• Replace every RRID instruction or placeholder with a verified RRID where one exists or Not applicable where appropriate.
• Remove all bracketed prompts and instructional text.
• Add stable source/vendor URLs for applicable software, APIs, models, and computational resources.

Supplementary Files
• Upload the cited Supplemental File 1 containing the reference implementation.
• Verify that the in-text citation and supplementary-file label exactly match the uploaded file.

Acknowledgments
• Add a standalone ACKNOWLEDGMENTS section after the Discussion.
• List all applicable funding, institutional support, technical assistance, and other acknowledgments.
• If there are no acknowledgments and no specific funding, state this explicitly.

Author Contributions
• Add a standalone AUTHOR CONTRIBUTIONS section after DISCLOSURES and before REFERENCES.
• Describe the specific contributions of all 11 authors.
• Use the full byline names consistently.
• State that all authors approved the final manuscript and accept accountability for the work.

References
• Reformat references 13, 16, and 17 using the first author followed by “et al.” because each reference has five authors.
• Remove extra spaces before superscript in-text reference citations.

____________________________________
Reviewers' comments:
Reviewer #1:

This paper proposes a Seed-Sample Precheck method for automatic annotation of visual language models (VLM). By estimating the consistency error rate, calibrating the sample size constraint and statistically testing the efficacy, it can determine in advance whether Conformal Prediction can generate a prediction set with practical value. The research questions in the paper have certain significance, and the method design is relatively clear. However, the sufficiency of the experiments, statistical reliability and reproducibility still need to be strengthened.

First, the scale of the experiment is limited. The current core experiment only contains 30 synthetic images, among which 13 have the problem of insufficient generation quantity. It is recommended to complete the full experiment on the existing 195 validation images to enhance the reliability of the conclusion.

Second, the generalization ability lacks verification. The paper only evaluates the synthetic target counting task of a single VLM. It is suggested to add different visual language models and the automatic annotation task of real images to verify the universality of the pre-checking mechanism.

Thirdly, the statistical judgment mechanism needs further clarification. The current three conditions are mainly used to determine whether the prediction set may have information volume, but meeting the necessary conditions does not mean that the actual quality of automatic annotation can be guaranteed. It is suggested to clarify the distinction between necessary conditions and sufficient conditions, and supplement the sensitivity analysis of statistical power and determination thresholds.

Fourth, the relationship between data generation defects and model errors requires a more in-depth analysis. The actual number of targets generated from the 13 images is less than the preset number, but the paper uses the actual number as the true label. It is suggested to further analyze the independent influence of target density, actual quantity and image degradation degree on the error rate, and avoid directly equating the two.

Fifth, reproducibility and related work need to be improved. The paper has not yet provided the complete VLM names and versions, and the original images and query records have not been retained either. It is suggested to supplement the specific experimental configuration and code archiving information. Furthermore, if the author wishes to expand the research background of visual generative data construction, it is advisable to appropriately discuss IMAGPose [1] and IMAGDressing v1 [2], and introduce the relevant research on conditional control and structural consistency in generative visual tasks.


References

[1] IMAGPose: A Unified Conditional Framework for Pose-Guided Person Generation.

[2] IMAGDressing-v1: Customizable Virtual Dressing.


Reviewer #2:

1. Limited experimental validation and generalizability

The central experimental demonstration relies on only 30 synthetic images containing simple geometric objects. Although this setup provides controlled ground truth, it does not adequately establish whether the proposed precheck is useful for realistic VLM-assisted annotation tasks.

The manuscript also introduces a corrected benchmark of 195 images, but the complete VLM annotation experiment was not conducted on this benchmark. The partial extension involving 21 images is insufficient to address this limitation.

I encourage the authors to validate the procedure on a larger, independently generated dataset and, ideally, at least one natural-image annotation task. Evaluating multiple VLM annotators would also help establish whether the observed behavior is specific to the selected model or reflects a broader limitation of self-consistency-based annotation.

2. Dependence on a defective synthetic data generator

A significant concern is that 13 of the 30 seed images contained fewer objects than originally requested. Although the authors correctly distinguish requested counts from realized counts and use the latter as ground truth, this generation defect affects a substantial fraction of the experimental sample.

The stratified results suggest that the under-rendered images account for much of the observed annotation difficulty. Consequently, it is difficult to separate the general effectiveness of the proposed precheck from the characteristics of this particular defective dataset.

The identification of this issue is a useful diagnostic observation, but it should not substitute for evaluation on correctly generated data. I strongly recommend repeating the main experiments on the corrected benchmark and reporting whether the precheck decisions remain consistent.

Furthermore, the manuscript attributes much of the error to the generator defect, but the causal relationship between under-rendering and annotator mistakes is not fully established. The authors should clarify whether the observed difference may also be explained by object-count distributions or image difficulty.

3. Clarification of the feasibility guarantees

The manuscript presents three necessary conditions for obtaining informative conformal prediction sets. However, satisfying these conditions does not necessarily guarantee that the resulting prediction sets will be sufficiently informative for practical auto-annotation.

In particular, the unanimous-error criterion addresses a specific mechanism through which the calibration threshold reaches its maximum value. Passing this criterion does not guarantee small prediction sets, high singleton rates, or acceptable annotation accuracy.

The manuscript should more clearly distinguish between detecting conditions that necessarily produce trivial sets and predicting that an annotation pipeline will achieve useful performance.

I suggest explicitly defining what a "go" decision guarantees, what it does not guarantee, and how the feasibility conditions relate to practical quantities such as singleton yield and prediction-set size.

4. Statistical power and uncertainty estimation

The manuscript provides useful sample-size calculations, but several aspects of the statistical evaluation require clarification.

First, condition C3 is described using the upper limit of a two-sided Clopper-Pearson confidence interval, whereas the sample-size calculations are based on a one-sided exact binomial test. The authors should explain how these two procedures relate and whether they produce consistent go/no-go decisions.

Second, the confirmatory evaluation averages results over 400 random calibration/test splits of the same small dataset. These repetitions are not independent experimental samples and do not eliminate uncertainty associated with the original 30 images. The manuscript should distinguish split-induced variability from dataset-level uncertainty and, where possible, provide uncertainty estimates based on independent test observations.

Finally, the proposed decision rule should be evaluated in terms of its false-go and false-no-go behavior. This would make the claimed reliability of the precheck more directly interpretable.

5. Reproducibility and incomplete methodological details

The manuscript acknowledges that the original seed images, generating random seed, original generation scripts, and raw per-query responses were not retained. Although reconstructed scripts and aggregated results are provided, these materials cannot reproduce the original experiment exactly.

In addition, the specific commercial VLM used for annotation is not identified in the submitted materials table, and several software or release identifiers remain as placeholders.

For a study whose central contribution is a practical evaluation protocol, reproducibility is particularly important. The authors should provide the model name and version, API settings, complete prompts, sampling parameters, and exact implementation details. The corrected benchmark should also be accompanied by complete per-image evaluation records.

A new reproducible run on the corrected benchmark would substantially strengthen the manuscript.