# Test Results: statistics/assumption-checking.md

> ⚠️  Raw model output captured automatically by the cross-model test harness on 2026-06-23.
> This output is **not yet verified**. An author must read the output and set the
> assessment below before this counts as a tested result (see CLAUDE.md, Hard Rules).

## Test Metadata
- **Prompt:** statistics/assumption-checking.md
- **Model:** nemotron-3-super-120b
- **Model ID (pinned):** Nemotron-3-Super-120B-A12B-NVFP4
- **Endpoint:** https://copilot-dev.cqls.oregonstate.edu/llm/nemotron3-super-120b-nvfp4/v1
- **Date:** 2026-06-23
- **Tester:** cross-model-harness
- **Assembly strategy:** concat
- **Temperature:** 0.0

## Test Input Used
Standard test input from prompt file (`## Test Input`).

## Filled Prompt
```
Context: I plan to use {STATISTICAL_TEST_OR_MODEL} to analyze my data. I need to verify the assumptions are met.

Analysis details:
- Test/model: {SPECIFIC_TEST: e.g., "two-way ANOVA," "logistic regression," "Wilcoxon rank-sum"}
- Outcome variable: {type and name}
- Predictor(s): {type and names}
- Sample size: {n or n per group}
- Software: {what you're using}

Data characteristics I've noticed:
- {ANY_OBSERVATIONS: e.g., "outcome looks skewed," "several outliers visible," "one group has higher variance"}

Task: Provide a complete assumption-checking workflow:

1. **List all assumptions** for this test, in order of importance (which violations are most problematic)

2. **For each assumption**:
   - What it means in plain language
   - How to test it (formal tests and/or visual diagnostics)
   - How to interpret the results
   - What to do if violated (robust alternatives, transformations, or when it's okay to proceed)

3. **Code examples** for the assumption checks in {SOFTWARE}

4. **Decision summary**: A flowchart or decision tree for how to proceed based on results

Constraints:
- Be practical—focus on violations that meaningfully affect inference
- Note when minor violations are unlikely to matter
- Acknowledge that some assumption tests have their own limitations

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
```

## Model Output
```


**PERMANOVA (adonis2) – Assumption‑checking workflow**  
*Outcome*: Bray‑Curtis distance matrix of microbiome community composition  
*Predictors*: Treatment (3 levels), Time (2 levels), Treatment × Time interaction  
*Software*: R ≥ 4.0, **vegan** package (adonis2, betadisper, etc.)  

---

## 1.  Assumptions – ranked by impact on inference  

| Rank | Assumption | Why it matters most | Typical symptom if violated |
|------|------------|---------------------|-----------------------------|
| **1** | **Independence of observations** (exchangeability under the null) | PERMANOVA permutes rows of the distance matrix; if observations are not exchangeable (e.g., repeated measures, spatial/temporal clustering) the p‑value is invalid. | Pseudoreplication, nested design, longitudinal samples from the same subject, batch effects. |
| **2** | **Homogeneity of multivariate dispersion** (equal spread / variance‑covariance across groups) | PERMANOVA tests for differences in *location* (centroids). If groups differ in spread, a significant result may reflect dispersion rather than location, inflating Type I error. | One group forms a tight cluster while others are scattered; betadisper shows significant differences. |
| **3** | **Appropriateness of the distance metric** (Bray‑Curtis reflects ecological dissimilarity) | PERMANOVA is a *distance‑based* test; if the distance does not faithfully represent the ecological question, the test may lack power or give misleading results. | Many zeros, highly skewed count data, or use of a metric that is not bounded (e.g., Euclidean on raw counts). |
| **4** | **Adequate sample size / balance** (helps with permutation precision) | Not a formal assumption, but very small or highly unbalanced designs reduce the number of unique permutations and can make the test conservative/anti‑conservative. | <5 replicates per cell, extreme imbalance. |

> **Note** – PERMANOVA does **not** require multivariate normality, linearity, or homoscedasticity in the classical ANOVA sense. The main vulnerabilities are independence and dispersion.

---

## 2.  How to check each assumption  

### 2.1 Independence  

| What it means | How to assess | Interpretation | What to do if violated |
|---------------|---------------|----------------|------------------------|
| Each sample provides an independent piece of information about the underlying community. The permutation scheme must be able to shuffle labels without breaking any dependence structure. | • Review study design (are samples from the same subject, same cage, same batch?).<br>• If repeated measures exist, create a *strata* variable (e.g., SubjectID) and use `adonis2(..., strata = SubjectID)`.<br>• Plot residuals from a distance‑based redundancy analysis (dbRDA) to look for patterns (e.g., temporal trends). | No obvious clustering or temporal trend in residuals → independence plausible.<br>Significant stratification effect (e.g., `adonis2` with `strata` changes p‑value markedly) → dependence present. | • Use **restricted permutations** (`strata` argument) to permute within blocks.<br>• If the dependence is hierarchical (e.g., subjects → time points), consider a **distance‑based linear mixed model** (`lme4::lmer` on PCoA axes) or **PERMANOVA+** (adonis2 with `strata` + `by = "terms"`).<br>• As a last resort, collapse to a summary per independent unit (e.g., subject‑level averages) and test with a simpler design. |

**R code (independence check)**  

```r
library(vegan)

# Bray‑Curtis distance matrix (already computed)
dist_bc <- vegdist(otu_table, method = "bray")

# Basic adonis2 (no restriction)
adon <- adonis2(dist_bc ~ Treatment * Time, data = meta, permutations = 999)

# If you have a blocking factor (e.g., SubjectID)
adon_str <- adonis2(dist_bc ~ Treatment * Time,
                    data = meta,
                    strata = meta$SubjectID,   # restrict permutations within subjects
                    permutations = 999)

adon
adon_str
```

Compare the p‑values; a large change signals dependence.

---

### 2.2 Homogeneity of multivariate dispersion  

| What it means | How to assess | Interpretation | What to do if violated |
|---------------|---------------|----------------|------------------------|
| The average distance of each sample to its group centroid (i.e., spread) is the same across all groups. PERMANOVA assumes that any significant effect is due to differences in centroids, not in spread. | • **betadisper()** (PERMDISP) → computes distances to centroids.<br>• **permutest(betadisper)** → tests equality of dispersions (ANOVA‑like on those distances).<br>• Visual: boxplot of distances to centroid, or overlay on PCoA plot (colour by group, size = distance to centroid). | *Non‑significant* (p > 0.05) → no evidence of heterogeneity → assumption tenable.<br>*Significant* (p ≤ 0.05) → at least one group differs in spread → PERMANOVA p‑value may be confounded. | • If dispersion differs **but** sample sizes are equal (as in your design) and the effect you care about is large, many authors consider the test still interpretable (Anderson 2006).<br>• **Transform the data** before computing distances (e.g., Wisconsin double‑standardization, Hellinger, or log‑(x+1)) to reduce heterogeneity.<br>• Use **PERMANOVA+** (adonis2 with `by = "terms"` and `strata`) and report both location and dispersion results.<br>• Consider a **test of location only** such as **PERMANOVA on residuals from a dispersion model** (`betadisper` → residuals → adonis2) or **distance‑based test of location (e.g., `anosim` is also sensitive to dispersion, so not ideal).<br>• As a robust alternative, fit a **generalized linear mixed model (GLMM)** on the raw counts (e.g., `glmmTMB` with a negative binomial family) and include random effects for subject/batch. |

**R code (dispersion check)**  

```r
library(vegan)

# 1. Compute distances to centroids for each group combination
disp <- betadisper(dist_bc, interaction(meta$Treatment, meta$Time))

# 2. Test homogeneity of dispersion
perm_disp <- permutest(disp, pairwise = TRUE, permutations = 999)

# 3. Visualise
boxplot(disp, xlab = "Treatment-Time", ylab = "Distance to centroid")
# or overlay on PCoA
pcoa <- cmdscale(dist_bc, eig = TRUE, k = 2)
scores <- as.data.frame(pcoa$points)
colnames(scores) <- c("PCoA1", "PCoA2")
scores$Group <- interaction(meta$Treatment, meta$Time)
scores$DistToCent <- disp$distances   # distance to its own centroid

ggplot(scores, aes(PCoA1, PCoA2, colour = Group, size = DistToCent)) +
  geom_point(alpha = 0.7) +
  scale_size_continuous(range = c(1, 4)) +
  theme_minimal() +
  labs(title = "PCoA with dispersion (size = distance to centroid)")
```

Check `perm_disp$tab` for the overall p‑value and the pairwise table for which groups differ.

---

### 2.3 Appropriateness of the distance metric  

| What it means | How to assess | Interpretation | What to do if violated |
|---------------|---------------|----------------|------------------------|
| Bray‑Curtis should reflect ecologically meaningful dissimilarity given the data type (usually count or relative abundance). | • Examine the raw OTU/ASV table: proportion of zeros, library size distribution.<br>• Compare Bray‑Curtis to alternatives (e.g., Jaccard, unweighted UniFrac, weighted UniFrac, Hellinger‑transformed Euclidean) using a **Mantel test** or **Procrustes analysis** to see if conclusions change.<br>• Check for strong library‑size effects: plot Bray‑Curtis vs. total reads per sample. | If Bray‑Curtis correlates strongly (>0.8) with another metric and gives similar PERMANOVA results, the choice is robust.<br>If Bray‑Curtis is driven by library size differences (high correlation with total reads) → consider transformation. | • **Transform abundances** before distance calculation: <br> – Wisconsin double‑standardization (`decostand(otu, method = "wisconsin")`)<br> – Hellinger (`decostand(otu, method = "hellinger")`)<br> – Log‑(x+1) (`log1p(otu)`) <br>• If phylogenetic information is available and you suspect it matters, use **UniFrac** distances.<br>• Report sensitivity analysis: run adonis2 with at least two distances and note whether the inference changes. |

**R code (distance‑metric check)**  

```r
library(vegan)

# Raw count table (samples x taxa)
otu_raw <- otu_table   # replace with your object

# 1. Bray‑Curtis on raw counts
bc_raw <- vegdist(otu_raw, method = "bray")

# 2. Hellinger‑transformed Euclidean (often recommended for count data)
otu_hell <- decostand(otu_raw, method = "hellinger")
dist_hell <- vegdist(otu_hell, method = "euclidean")

# 3. Jaccard (presence/absence)
otu_pa <- decostand(otu_raw, method = "pa")
dist_jac <- vegdist(otu_pa, method = "jaccard")

# Mantel test to see similarity among distance matrices
mantel(bc_raw, dist_hell, permutations = 999)   # Bray vs Hellinger
mantel(bc_raw, dist_jac, permutations = 999)   # Bray vs Jaccad

# Run PERMANOVA on each distance to see if conclusions differ
adon_bc  <- adonis2(bc_raw  ~ Treatment * Time, data = meta, permutations = 999)
adon_hell<- adonis2(dist_hell ~ Treatment * Time, data = meta, permutations = 999)
adon_jac <- adonis2(dist_jac  ~ Treatment * Time, data = meta, permutations = 999)

list(BC = adon_bc, Hellinger = adon_hell, Jaccard = adon_jac)
```

If the p‑values and effect sizes (R²) are qualitatively similar across metrics, you can be confident the choice of Bray‑Curtis is not driving the result.

---

### 2.4 Sample size / balance (practical note)

| What it means | How to assess | Interpretation | What to do if violated |
|---------------|---------------|----------------|------------------------|
| Enough permutations to obtain a stable p‑value; balanced designs improve power and reduce bias. | • Count replicates per factor combination (`table(meta$Treatment, meta$Time)`).<br>• Compute number of unique permutations possible (`choose(N, n_per_group)` or use `permutations = max(1000, factorial(N))`). | If any cell has < 5 replicates, permutation distribution may be coarse → p‑values can be unstable.<br>Severe imbalance can bias the test toward larger groups. | • Increase number of permutations (e.g., `permutations = 9999`) to improve resolution.<br>• If imbalance is severe, consider **stratified permutations** (`strata`) or **weighted PERMANOVA** (`adonis2(..., by = "terms", type = "terms")`).<br>• As a last resort, collapse to a higher level (e.g., average per subject) to achieve balance. |

**R code (balance check)**  

```r
tab <- table(meta$Treatment, meta$Time)
tab   # should show 10 in each cell for your design
min(tab)   # smallest cell size
```

If `min(tab) >= 5` you are fine; otherwise note the limitation.

---

## 3.  Putting it together – Decision flowchart (textual)

```
Start
│
├─► 1️⃣ Check Independence
│     • Are there repeated measures, batches, or other clustering?
│     ├─ Yes → Define blocking variable (e.g., SubjectID, Batch)
│     │      → Use adonis2(..., strata = block)  (restricted permutations)
│     │      → Re‑run PERMANOVA; note change in p‑value.
│     └─ No  → Proceed (no restriction needed)
│
├─► 2️⃣ Check Homogeneity of Dispersion
│     • Run betadisper + permutest on the (possibly restricted) distance matrix.
│     ├─ Significant dispersion difference? (p ≤ 0.05)
│     │     ├─ Are group sizes equal? (your design: yes)
│     │     │     ├─ If effect size (R²) is large and you are mainly interested in location,
│     │     │     │   → Consider PERMANOVA still interpretable, but report dispersion test.
│     │     │     │   → Optionally: transform data (hellinger, wisconsin) and re‑test.
│     │     │     └─ If you want a test robust to dispersion:
│     │     │         → Use PERMANOVA on residuals from betadisper
│     │     │         → Or fit a GLMM on raw counts (e.g., glmmTMB) with same fixed effects.
│     │     └─ Unequal sizes → more cautious; consider transformation or mixed model.
│     └─ Non‑significant → Assumption satisfied; continue.
│
├─► 3️⃣ Check Distance Metric Appropriateness
│     • Examine zero‑inflation, library‑size bias.
│     • Run Mantel tests between Bray‑Curtis and alternatives (Hellinger, Jaccard, UniFrac).
│     • If alternatives give divergent PERMANOVA results:
│           → Choose the metric that best matches your ecological question
│           → Report sensitivity analysis.
│     └─ Otherwise, keep Bray‑Curtis.
│
├─► 4️⃣ Sample Size / Balance Check
│     • Any cell < 5? → increase permutations, note limited resolution.
│     • Otherwise, proceed.
│
└─► Final Model
      adonis2(dist ~ Treatment * Time,
              data = meta,
              strata = <block if needed>,
              permutations = 9999)   # or higher for small cells
      → Report:
          * Pseudo‑F, R², p‑value
          * Betadisper results (dispersion test)
          * Any transformations or alternative distances examined
          * Note on independence (design) and any restrictions used
```

---

## 4.  Example R script (complete workflow)

```r
## -------------------------------------------------
## 0. Packages
## -------------------------------------------------
library(vegan)
library(ggplot2)

## -------------------------------------------------
## 1. Load data
## -------------------------------------------------
# otu_table: samples x taxa (counts or relative abundances)
# meta: data.frame with columns SampleID, Treatment, Time, SubjectID (if any)
otu_raw   <- read.csv("otu_counts.csv", row.names = 1)
meta      <- read.csv("metadata.csv",   row.names = 1)

## -------------------------------------------------
## 2. Independence check (design)
## -------------------------------------------------
# Example: repeated measures on the same subject over Time
if ("SubjectID" %in% names(meta)) {
  block_var <- meta$SubjectID
  use_strata <- TRUE
} else {
  block_var <- NULL
  use_strata <- FALSE
}

## -------------------------------------------------
## 3. Distance matrix (with optional transformation)
## -------------------------------------------------
# Option A: raw Bray
```

## Overall Assessment
- **Recommendation:** Pass
- **Notes:**
## Verification Steps Tested
_Which verification requirements from the prompt were checked, and results._
