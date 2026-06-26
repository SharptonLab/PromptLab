# Test Results: statistics/assumption-checking.md

> ⚠️  Raw model output captured automatically by the cross-model test harness on 2026-06-25.
> This output is **not yet verified**. An author must read the output and set the
> assessment below before this counts as a tested result (see CLAUDE.md, Hard Rules).

## Test Metadata
- **Prompt:** statistics/assumption-checking.md
- **Model:** nemotron-3-super-120b
- **Model ID (pinned):** Nemotron-3-Super-120B-A12B-NVFP4
- **Endpoint:** https://copilot-dev.cqls.oregonstate.edu/llm/nemotron3-super-120b-nvfp4/v1
- **Date:** 2026-06-25
- **Tester:** cross-model-harness
- **Assembly strategy:** test-only
- **Temperature:** 0.0

## Test Input Used
Standard test input from prompt file (`## Test Input`).

## Filled Prompt
````
Context: I plan to use PERMANOVA to analyze my data. I need to verify the assumptions are met.

Analysis details:
- Test/model: PERMANOVA (adonis2 in vegan package)
- Outcome variable: Bray-Curtis distance matrix of microbiome community composition
- Predictors: Treatment group (3 levels), Time (2 levels), Treatment × Time interaction
- Sample size: 60 samples (10 per group-time combination)
- Software: R with vegan package

Data characteristics I've noticed:
- Groups have different spread on PCoA plots (dispersion looks unequal)
- One treatment group clusters more tightly than others
- Sample sizes are equal across groups

Task: Provide a complete assumption-checking workflow:

1. **List all assumptions** for this test, in order of importance (which violations are most problematic)

2. **For each assumption**:
   - What it means in plain language
   - How to test it (formal tests and/or visual diagnostics)
   - How to interpret the results
   - What to do if violated (robust alternatives, transformations, or when it's okay to proceed)

3. **Code examples** for the assumption checks in R with vegan

4. **Decision summary**: A flowchart or decision tree for how to proceed based on results

Constraints:
- Be practical—focus on violations that meaningfully affect inference
- Note when minor violations are unlikely to matter
- Acknowledge that some assumption tests have their own limitations
````

## Model Output
````


Below is a **practical, step‑by‑step workflow** for checking the assumptions that matter most when you run a PERMANOVA with `vegan::adonis2()` on a Bray‑Curtis distance matrix.  
I have ordered the assumptions by the severity of their impact on Type I error (false‑positive rate) and power, and for each one I give:

* a plain‑language description,  
* how to test it (formal test + visual check),  
* how to interpret the output,  
* what to do if the assumption is violated (robust alternatives, transformations, or when it’s safe to ignore),  
* ready‑to‑run R code (vegan ≥ 2.5‑0, base R, and a few helper packages).

---

## 1. Assumptions – ranked by importance  

| Rank | Assumption | Why it matters most | Typical symptom in your data |
|------|------------|---------------------|------------------------------|
| **1** | **Exchangeability (independence) under the null** | PERMANOVA builds its null distribution by permuting residuals. If observations are not exchangeable (e.g., repeated measures, spatial/temporal autocorrelation, nested design), the permutation scheme is wrong → inflated Type I error. | Samples from the same subject over time, or samples that are spatially clustered, show similar Bray‑Curtis distances beyond what treatment explains. |
| **2** | **Homogeneity of multivariate dispersion (variance) across groups** | PERMANOVA tests for differences in *location* (centroids). If groups differ in spread, the test can become significant even when centroids are identical → false positives. | One treatment group looks tightly clustered on PCoA while others are scattered (as you observed). |
| **3** | **Adequate number of permutations / sufficient sample size for stable p‑values** | With too few unique permutations the p‑value is granular (e.g., only 0.05, 0.10, …) and may be unreliable. | < 1000 unique permutations when you have ≤ 20 samples per stratum. |
| **4** | **Correct model specification (including interaction terms)** | Miss‑specifying the model (e.g., omitting a needed interaction) can bias the test of the terms you keep. | You suspect a Treatment × Time interaction but fit only additive terms. |
| **5** | **Choice of distance metric is appropriate for the ecological question** | Not a formal assumption, but a poor metric can mask real effects or create spurious ones. | Bray‑Curtis is fine for abundance data; if you have many zeros, consider Jaccard or Hellinger‑transformed Euclidean. |

> **Bottom line:** If #1 or #2 fails, the PERMANOVA p‑values are not trustworthy. #3–#5 are “nice‑to‑have” checks that affect precision or interpretability but rarely overturn a clear result.

---

## 2. Detailed assumption‑checking guide  

### 2.1. Exchangeability (Independence)

| What it means | How to test | Interpretation | What to do if violated |
|---------------|-------------|----------------|------------------------|
| Under the null hypothesis, the residuals (or the raw data under a reduced model) can be freely shuffled without changing their joint distribution. In practice this requires that observations are **independent** and that any known blocking structure (e.g., repeated measures on the same subject, spatial clusters) is accounted for. | • **Design check** – write out your sampling scheme. <br>• If you have repeated measures, compute a **within‑subject correlation** on the distance matrix (e.g., using `vegan::mantel` with a subject‑ID distance matrix). <br>• For spatial/temporal autocorrelation, compute **Moran’s I** or a **variogram** on the PCoA axes (`spdep::moran.test`). | • No significant correlation → independence plausible. <br>• Significant positive correlation → observations are more similar than exchangeability assumes. | • **Stratified permutations**: supply a `strata` argument to `adonis2()` (e.g., `strata = SubjectID`). <br>• **Blocked PERMANOVA** (`adonis2(..., permutations = how(blocks = SubjectID, within = WithinBlock))`). <br>• If the dependence is complex (e.g., crossed random effects), consider a **distance‑based linear mixed model** (`lme4::lmer` on PCoA axes) or **PERMANOVA+** (PRIMER‑E) with a restricted permutation scheme. <br>• As a last resort, move to a **multivariate GLMM** (e.g., `mvabund::manyglm` or `glmmTMB` on a multinomial/Dirichlet‑multinomial). |

**R code**

```r
## 1. Check design -------------------------------------------------
head(df)                     # df must contain: SampleID, SubjectID, Treatment, Time, etc.

## 2. Within‑subject correlation (if repeated measures) ----------
if ("SubjectID" %in% names(df)) {
  # distance matrix of samples
  dist_bc <- vegdist(df[, microbe_cols], method = "bray")
  # subject‑ID distance (0 = same subject, 1 = different)
  subj_dist <- as.matrix(dist(df$SubjectID, method = "manhattan")) > 0
  mantel_res <- mantel(dist_bc, subj_dist, permutations = 9999, method = "pearson")
  mantel_res
}

## 3. Spatial/temporal autocorrelation on PCoA axes -------------
pcoa <- cmdscale(dist_bc, k = 2, eig = TRUE)   # first two PCoA axes
scores <- as.data.frame(pcoa$points)
colnames(scores) <- c("PCoA1", "PCoA2")
scores$SubjectID <- df$SubjectID   # or any grouping factor

# Moran's I (requires a spatial weights matrix; here we use a simple
# Euclidean distance threshold as an example)
library(spdep)
coords <- as.matrix(scores[, c("PCoA1", "PCoA2")])
knn <- knearneigh(coords, k = 4)          # 4 nearest neighbours
nb   <- knn2nb(knn)
listw <- nb2listw(nb, style = "W")
moran.test(scores$PCoA1, listw)   # repeat for PCoA2
```

---

### 2.2. Homogeneity of multivariate dispersion (PERMDISP)

| What it means | How to test | Interpretation | What to do if violated |
|---------------|-------------|----------------|------------------------|
| The spread (average distance to group centroid) of the multivariate data is similar across all levels of each factor (and across interaction cells if you test them). | **`betadisper()`** (PERMDISP) on the same distance matrix, followed by `anova()` or `permutest()`. <br>Visual: boxplots of distances to centroid, or overlay of group ellipses on a PCoA plot. | • **Non‑significant** (p > 0.05) → dispersion not different → PERMANOVA safe. <br>• **Significant** → at least one group differs in spread → PERMANOVA may be conflating location & dispersion effects. | 1. **Report both** PERMANOVA (location) and PERMDISP (dispersion) results; interpret cautiously. <br>2. If the research question is *purely* about centroids, you can **adjust for dispersion** by including the distance-to-centroid as a covariate in a **distance‑based linear model (distLM)** (`vegdist → capscale`). <br>3. Use a **test that separates location and dispersion**, e.g., **PERMANOVA of residuals after removing dispersion effects** (`betadisper` residuals) or **ANOVA‑like permutation test on the dispersion statistics** themselves. <br>4. If dispersion differences are large and biologically interesting, consider **modeling them directly** (e.g., `glmmTMB` with a beta‑dispersion family on proportional abundances, or `mvabund` with mean‑variance modeling). <br>5. As a last resort, switch to a **method that is insensitive to dispersion**, such as **ANOSIM** (though it also has limits) or **distance‑based redundancy analysis (dbRDA)** with permutation of residuals under a reduced model *and* reporting dispersion separately. |

**R code**

```r
## 1. PERMDISP (betadisper) ---------------------------------------
# Using the same Bray‑Curtis matrix as for adonis2
disp <- betadisper(dist_bc, df$Treatment)   # replace Treatment with any factor or interaction
anova(disp)                                 # parametric ANOVA on distances to centroid
permutest(disp, pairwise = TRUE, permutations = 9999)   # permutation test + pairwise

## 2. Visual check ------------------------------------------------
# Boxplot of distances to centroid
boxplot(disp, xlab = "Treatment", ylab = "Distance to centroid",
        main = "Multivariate dispersion (PERMDISP)")

# PCoA plot with group ellipses
library(ggplot2)
pcoa_df <- as.data.frame(scores)
pcoa_df$Treatment <- df$Treatment
ggplot(pcoa_df, aes(PCoA1, PCoA2, colour = Treatment)) +
  geom_point(size = 2) +
  stat_ellipse(type = "norm", level = 0.95) +
  theme_minimal() +
  labs(title = "PCoA of Bray‑Curtis distances")
```

---

### 2.3. Number of permutations / sample size

| What it means | How to test | Interpretation | What to do if violated |
|---------------|-------------|----------------|------------------------|
| The permutation reference distribution must have enough *unique* permutations to give a granular p‑value (e.g., steps of 0.001). With very small groups you may run out of distinct permutations. | Check `choose(n, n_per_group)` or simply look at the output of `adonis2(..., permutations = 9999)` – it reports the number of **actual** permutations used. | If the reported number is far below the requested number (e.g., you asked for 9999 but only 123 unique permutations exist), the p‑value is coarse. | • Increase the number of permutations **only if** the design allows it (e.g., use `permutations = how(nperm = 9999)`). <br>• If you truly have too few permutations, consider **exact tests** (e.g., `permute::permTS` with `exact = TRUE`) or switch to a **model‑based approach** (GLMM, Bayesian). <br>• For very small samples, report the **exact permutation p‑value** and note the limited resolution. |

**R code**

```r
## adonis2 with permutation control ---------------------------------
library(permute)   # for how()
ctrl <- how(blocks = df$SubjectID,   # if you have a blocking factor
            within = Within(type = "free"),
            nperm = 9999)

adonis_res <- adonis2(dist_bc ~ Treatment * Time,
                      data = df,
                      permutations = ctrl)
adonis_res
# Look at the line: "Permutations: 9999" (or lower if limited)
```

---

### 2.4. Model specification

| What it means | How to test | Interpretation | What to do if violated |
|---------------|-------------|----------------|------------------------|
| The formula you give to `adonis2()` must contain all terms you wish to test (main effects, interactions, covariates). Omitting a needed term can bias the test of the remaining terms. | • Compare nested models with `anova()` (or `adonis2()` with `by = "terms"`). <br>• Use **variance partitioning** (`varpart`) to see how much each term explains. | • If adding a term substantially changes the R² or p‑value of another term, the original model was miss‑specified. | • Re‑fit the model with the correct structure (e.g., include `Treatment:Time` interaction). <br>• If you are unsure, start with a **saturated model** (all interactions) and then drop non‑significant terms using a hierarchical testing strategy (respecting marginality). |

**R code**

```r
## Full model (including interaction) -------------------------------
full <- adonis2(dist_bc ~ Treatment * Time, data = df, permutations = ctrl)

## Reduced model (no interaction) ----------------------------------
red  <- adonis2(dist_bc ~ Treatment + Time, data = df, permutations = ctrl)

## Compare ---------------------------------------------------------
anova(full, red)   # tests whether the interaction adds significant explanatory power
```

---

### 2.5. Choice of distance metric (practical note)

| What it means | How to test | Interpretation | What to do if violated |
|---------------|-------------|----------------|------------------------|
| The distance should reflect the ecological dissimilarity you care about. Bray‑Curtis is sensitive to abundant taxa; Jaccard focuses on presence/absence; Hellinger‑transformed Euclidean down‑weights double zeros. | • Run PERMANOVA with two alternative distances (e.g., `vegdist(..., method = "jaccard")` and `vegdist(..., method = "euclidean")` after Hellinger transform). <br>• Compare effect sizes (R²) and significance. | • If conclusions change dramatically, the result is **distance‑dependent** → interpret with caution. | • Choose the metric that matches your hypothesis (e.g., abundance‑weighted vs. presence/absence). <br>• Report sensitivity analysis: “Results were robust to Bray‑Curtis, Jaccard, and Hellinger‑Euclidean distances.” |

**R code**

```r
## Bray‑Curtis (original) -----------------------------------------
bc_res <- adonis2(vegdist(df[microbe_cols], method = "bray") ~ Treatment * Time,
                  data = df, permutations = ctrl)

## Jaccard (presence/absence) ------------------------------------
jac_res <- adonis2(vegdist(df[microbe_cols], method = "jaccard") ~ Treatment * Time,
                   data = df, permutations = ctrl)

## Hellinger‑transformed Euclidean -------------------------------
hell <- decostand(df[microbe_cols], method = "hellinger")
euc_res <- adonis2(vegdist(hell, method = "euclidean") ~ Treatment * Time,
                   data = df, permutations = ctrl)

list(BrayCurtis = bc_res, Jaccard = jac_res, HellingerEucl = euc_res)
```

---

## 3. Decision flowchart (textual version you can turn into a diagram)

```
Start
│
├─► 1️⃣ Check Exchangeability / Independence
│     ├─► Any known blocking/repeated measures? 
│     │     ├─► Yes → use `strata=` or `how(blocks=…)` in adonis2()
│     │     └─► No → proceed
│     └─► Test for residual autocorrelation (Mantel, Moran’s I)
│           ├─► Significant? → dependence present
│           │     ├─► If blockable → stratified permutations
│           │     └─► If not blockable → consider mixed‑model / GLMM
│           └─► Non‑significant → independence OK
│
├─► 2️⃣ Check Homogeneity of D
````

## Assessment

_Machine-suggested (UNCONFIRMED) — drafted by Claude Opus 4.7 on 2026-06-26 to speed T4 review. An author must independently read the Model Output above and set the real Recommendation. Anything labeled here is triage, not domain expert review._

**Machine triage:** Output is **TRUNCATED** mid-decision-tree (inside ASCII diagram at "Check Homogeneity of D"). Cross-model: 3 of 6 truncated on this prompt.

**Suggested verdict (UNCONFIRMED):** Needs revision

**What still needs human verification:**
- Confirm capture-side token cap; re-run with higher max-tokens
- Whether the ASCII decision tree format would render cleanly
- That the captured priority ordering (independence > dispersion) matches peer ordering

## Overall Assessment
- **Recommendation:** PENDING AUTHOR REVIEW
- **Notes:**

## Verification Steps Tested
_Which verification requirements from the prompt were checked, and results._
