# Assumption Checking Prompt

## Task Description

Generate a workflow for checking the assumptions of a statistical test, including what to check, how to check it, and what to do if assumptions are violated.

## When to Use

- Before running a statistical analysis to verify assumptions are met
- When interpreting results and wondering if assumption violations affect conclusions
- When learning what assumptions a test requires
- When reviewers question whether your analysis assumptions were verified

## When NOT to Use

- As the sole guide for complex analyses (consult a statistician)
- When you don't have the data to actually perform the checks
- When assumption checking would be post-hoc rationalization for choosing tests

## The Prompt

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
```

## Prompt Components Explained

| Component | Purpose |
|-----------|---------|
| **Specific test** | Determines which assumptions apply |
| **Data characteristics** | Flags likely issues to focus on |
| **Software** | Provides runnable code |
| **Decision focus** | Makes output actionable |

## Example Input

```
Context: I plan to use a linear mixed model to analyze my data. I need to verify the assumptions are met.

Analysis details:
- Test/model: Linear mixed effects model (lmer in R) with random intercept
- Outcome variable: Shannon diversity index (continuous)
- Predictors: Treatment (2 levels, fixed), Time (continuous, fixed), Treatment × Time interaction
- Random effect: Mouse ID (repeated measures on same mice)
- Sample size: 30 mice, 4 timepoints each = 120 observations
- Software: R with lme4

Data characteristics I've noticed:
- Diversity values range from 2.5 to 5.0
- Possibly slight right skew in one treatment group
- One mouse has consistently lower values than others
```

## Example Output

## Linear Mixed Model Assumptions: Checking Workflow

### Assumptions Ranked by Importance

1. **Independence of observations (conditional on random effects)** — Most critical
2. **Linearity of fixed effects** — Important for interpretation
3. **Homoscedasticity (constant residual variance)** — Affects standard errors
4. **Normality of residuals** — Less critical for larger samples
5. **Normality of random effects** — Usually robust to mild violations

---

### 1. Independence of Observations

**What it means**: After accounting for the random effects (mouse), the residual errors should be independent. Observations from the same mouse can be correlated (that's why you have the random effect), but the model assumes it's captured by the random intercept.

**How to check**:
- Primarily a design issue—verify your random effects structure matches your data structure
- If you suspect temporal autocorrelation within mice (beyond what random intercept captures), check residuals over time

**What to look for**:
- Are there additional sources of non-independence not modeled? (e.g., mice from same litter, cage effects)
- Do residuals show patterns within mouse over time?

**If violated**:
- Add additional random effects (e.g., cage, litter)
- Consider random slopes if trajectories differ
- For temporal autocorrelation: use correlation structures (nlme) or generalized models

**Code**:
```r
# Check if residuals show patterns within mouse over time
library(ggplot2)

# Add residuals to data
data$resid <- residuals(model)

# Plot residuals over time, faceted by mouse
ggplot(data, aes(x = time, y = resid)) +
  geom_point() +
  geom_smooth(method = "loess", se = FALSE) +
  facet_wrap(~mouse_id, scales = "free_y") +
  labs(title = "Residuals over time by mouse",
       y = "Residual", x = "Time")
```

---

### 2. Linearity of Fixed Effects

**What it means**: The relationship between continuous predictors (Time) and the outcome should be linear. For categorical predictors (Treatment), this isn't an issue.

**How to check**:
- Plot residuals vs. fitted values (should show no pattern)
- Plot residuals vs. continuous predictors (should be random scatter)
- Plot observed vs. predicted values

**What to look for**:
- Curved patterns in residual plots suggest non-linearity
- Systematic over/under prediction at certain predictor values

**If violated**:
- Transform predictor (log, polynomial terms)
- Add polynomial or spline terms
- Use generalized additive mixed models (gamm4)

**Code**:
```r
# Residuals vs. fitted
plot(model, type = c("p", "smooth"),
     main = "Residuals vs Fitted")

# Residuals vs. time
ggplot(data, aes(x = time, y = residuals(model))) +
  geom_point(alpha = 0.5) +
  geom_smooth(method = "loess", color = "red") +
  geom_hline(yintercept = 0, linetype = "dashed") +
  labs(title = "Residuals vs Time", y = "Residual", x = "Time")
```

---

### 3. Homoscedasticity (Constant Variance)

**What it means**: The spread of residuals should be similar across all levels of predictors and fitted values.

**How to check**:
- Plot residuals vs. fitted values (spread should be constant)
- Plot residuals by group (spread should be similar)
- Levene's test (formal test, but sensitive to non-normality)

**What to look for**:
- Fan or funnel shapes in residual plots
- Noticeably different spread between treatment groups

**If violated**:
- Transform the outcome (log, sqrt)
- Use weighted regression
- Use robust standard errors (clubSandwich package)
- Use heteroscedasticity-robust models

**Code**:
```r
# Residuals vs fitted (check for fanning)
plot(model)  # Default lmer plot

# Compare variance by treatment group
ggplot(data, aes(x = treatment, y = residuals(model))) +
  geom_boxplot() +
  labs(title = "Residuals by Treatment Group")

# Formal test
library(car)
leveneTest(residuals(model) ~ data$treatment)
```

---

### 4. Normality of Residuals

**What it means**: Residual errors should be approximately normally distributed.

**Why less critical**: For sample sizes like yours (n=120 observations), inference is fairly robust to non-normality due to the Central Limit Theorem.

**How to check**:
- Q-Q plot of residuals (points should follow diagonal)
- Histogram of residuals (should be bell-shaped)
- Shapiro-Wilk test (formal test, but overly sensitive for large n)

**What to look for**:
- Severe skewness (long tail in one direction)
- Heavy tails (too many extreme values)
- Bimodality (two peaks)

**If violated**:
- Mild violations: Likely okay to proceed
- Moderate violations: Consider transformation (log, sqrt) or robust methods
- Severe violations: Consider generalized linear mixed models

**Code**:
```r
# Q-Q plot
qqnorm(residuals(model))
qqline(residuals(model), col = "red")

# Histogram
hist(residuals(model), breaks = 20, main = "Residual Distribution",
     xlab = "Residual")

# Shapiro-Wilk (if you want formal test)
# Note: Will often reject with large n even for trivial departures
shapiro.test(residuals(model))
```

---

### 5. Normality of Random Effects

**What it means**: The random intercepts for each mouse should be approximately normally distributed.

**How to check**:
- Q-Q plot of predicted random effects (BLUPs)
- Histogram of random effects

**What to look for**:
- Severe outliers (that one mouse with consistently low values)
- Skewness in random effects distribution

**If violated**:
- With 30 mice, mild violations usually okay
- Consider whether outlier mice should be investigated or excluded
- Robust estimation methods exist but are more complex

**Code**:
```r
# Extract random effects
re <- ranef(model)$mouse_id$`(Intercept)`

# Q-Q plot
qqnorm(re, main = "Q-Q Plot: Random Effects")
qqline(re, col = "red")

# Histogram
hist(re, breaks = 10, main = "Distribution of Random Intercepts",
     xlab = "Random Effect")

# Identify any extreme random effects
data.frame(mouse_id = rownames(ranef(model)$mouse_id),
           random_effect = re) %>%
  arrange(desc(abs(random_effect)))
```

---

### Decision Summary

```
START
  |
  v
Check Independence: Is your random effects structure appropriate?
  |
  +-- No → Add missing random effects (cage, litter, etc.)
  |
  +-- Yes
        |
        v
      Check Linearity: Residuals vs. predictors show no pattern?
        |
        +-- Curved pattern → Add polynomial/spline terms or transform
        |
        +-- Random scatter → Continue
              |
              v
            Check Homoscedasticity: Residual spread constant?
              |
              +-- Clear fanning/heteroscedasticity → Transform outcome or use robust SE
              |
              +-- Roughly constant → Continue
                    |
                    v
                  Check Residual Normality: Q-Q plot reasonable?
                    |
                    +-- Severe departure → Transform or use GLM
                    |
                    +-- Mild departure + n>50 → OK to proceed
                          |
                          v
                        Check Random Effects: Any extreme outliers?
                          |
                          +-- Yes → Investigate those subjects
                          |
                          +-- No → Proceed with analysis
                                |
                                v
                              REPORT: Which checks done, results, any actions taken
```

---

### For Your Specific Data

Based on what you've noticed:
- **Slight right skew**: Check Q-Q plot. If mild and only in one group, likely okay with n=120.
- **One mouse consistently lower**: Check random effects plot. This mouse will have a large negative random effect, which is fine—that's what random effects capture. Only worry if it's so extreme it distorts estimation.

## Test Input

Use the following scenario to test this prompt:

```
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
```

**Expected output should include:**
- Key assumptions: multivariate homogeneity of dispersions (most critical for PERMANOVA), adequate sample size
- betadisper() explained as the dispersion homogeneity test
- Discussion of PERMANOVA sensitivity to dispersion differences
- Code examples for betadisper and permutest
- Guidance on interpretation if dispersion differs significantly
- Alternatives if assumptions violated (consider dispersion as outcome)

**Verification points:**
- Correctly identifies dispersion homogeneity as key assumption
- Provides betadisper code in R
- Explains that significant PERMANOVA with unequal dispersion could mean location OR dispersion difference
- Practical guidance given observed unequal spread

## Failure Modes

- **Wrong assumptions listed**: May list assumptions for a different test
- **Over-emphasis on normality**: May overstate importance of normality for large samples
- **Test limitations not noted**: Formal assumption tests have their own assumptions and limitations
- **Cookbook approach**: May not emphasize that judgment is required
- **Missing field conventions**: Some fields have specific preferences for handling violations

## Verification Requirements

1. **Verify assumptions are correct for your test**: Cross-reference with textbooks
2. **Actually run the checks**: Don't just take the code—run it on your data
3. **Use judgment**: Understand that some violations matter more than others
4. **Document what you did**: Report assumption checks in your methods

## Variations

### Pre-analysis focus
```
Additional context: I haven't run the model yet and want to check assumptions before proceeding.
Task: Provide checks I can run on the raw data before fitting the model.
```

### Specific violation follow-up
```
I've found that {SPECIFIC_ASSUMPTION} is violated. What are my options and what do you recommend?
```

### Reporting template
```
Additional request: Provide template text for reporting assumption checks in a methods section.
```

## Model Notes

```
Tested across the panel; verdicts set by human review.

- Claude Opus 4 (claude-opus-4-5-20251101) (2026-02-04): Pass
- claude-opus-4.7 (2026-06-23): Pass
- claude-sonnet-4.6 (2026-06-23): Pass
- gemini-2.5-pro (2026-06-23): Pass
- gpt-5.5 (2026-06-23): Pass
- nemotron-3-super-120b (2026-06-23): Pass
- step-3.7-flash (2026-06-23): Pass

Full per-model raw outputs and reviewer notes: tests/statistics/assumption-checking/
```

## Cross-References

- For selecting appropriate tests, see `statistics/test-selection.md`
- For experimental design review, see `statistics/design-review.md`
- For implementing analysis in R, see `code/r-script-generation.md`
