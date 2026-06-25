# Test Results: few-shot-learning.md

## Test Metadata
- **Prompt:** fundamentals/few-shot-learning.md
- **Model:** Claude Opus 4 (claude-opus-4-5-20251101)
- **Date:** 2026-02-04
- **Tester:** Claude Code (automated testing)

## Test Input Used
Standard test input from prompt file (FMT clinical trial abstract extraction)

## Filled Prompt
```
I need to extract structured metadata from microbiome study abstracts. Extract only information explicitly stated in the abstract.

Here are examples of the format I need:

**Example 1:**
Input: "The gut microbiome plays a crucial role in host metabolism. We performed 16S rRNA gene sequencing on fecal samples from 120 participants (60 with type 2 diabetes, 60 healthy controls) recruited from three clinical sites. Using QIIME2 and LEfSe analysis, we identified 23 differentially abundant taxa, with Akkermansia muciniphila significantly depleted in diabetic patients (p < 0.001). Our findings suggest potential therapeutic targets for metabolic disease."

Output:
- Study type: Case-control
- Disease/condition: Type 2 diabetes
- Sample type: Fecal
- Sample size: 120 (60 cases, 60 controls)
- Sequencing: 16S rRNA gene
- Analysis tools: QIIME2, LEfSe
- Key finding: Akkermansia muciniphila depleted in diabetic patients
- Organism: Human

**Example 2:**
Input: "Early-life antibiotic exposure may have lasting effects on the developing microbiome. We followed 85 infants from birth to 24 months, collecting monthly stool samples. Shotgun metagenomic sequencing revealed that antibiotic-exposed infants (n=42) showed reduced bacterial diversity and delayed maturation of metabolic pathways compared to unexposed controls (n=43). Machine learning models predicted antibiotic exposure history with 89% accuracy based on 12-month microbiome profiles."

Output:
- Study type: Longitudinal cohort
- Disease/condition: Antibiotic exposure (not disease)
- Sample type: Stool
- Sample size: 85 infants (42 exposed, 43 controls)
- Sequencing: Shotgun metagenomics
- Analysis tools: Machine learning (not specified further)
- Key finding: Antibiotic exposure reduces diversity and delays metabolic pathway maturation
- Organism: Human (infant)

Now process the following using the same format:

Input: "Fecal microbiota transplantation (FMT) shows promise for recurrent Clostridioides difficile infection. This randomized controlled trial enrolled 68 patients with recurrent CDI, assigning them to FMT (n=34) or vancomycin (n=34). Stool samples were analyzed using shotgun metagenomics with MetaPhlAn3. At 8 weeks, FMT achieved 91% cure rate versus 62% for vancomycin (p=0.008). FMT recipients showed rapid engraftment of donor Bacteroidetes species and restoration of secondary bile acid metabolism."

Output:
```

## Model Output
```
- Study type: Randomized controlled trial
- Disease/condition: Recurrent Clostridioides difficile infection
- Sample type: Stool
- Sample size: 68 (34 FMT, 34 vancomycin)
- Sequencing: Shotgun metagenomics
- Analysis tools: MetaPhlAn3
- Key finding: FMT achieved 91% cure rate vs 62% for vancomycin; FMT recipients showed donor Bacteroidetes engraftment and restoration of secondary bile acid metabolism
- Organism: Human
```

## Overall Assessment

- **Recommendation:** Pass
- **Notes:** The few-shot learning prompt successfully guided metadata extraction with perfect format adherence. The model correctly identified study type as "Randomized controlled trial" (matching the pattern of Example 3 in the training examples but adapted appropriately), captured the clinical nature of the study, and included both primary outcome (cure rate) and secondary findings (engraftment, bile acid metabolism) in the key finding.

## Verification Steps Tested
- [x] Output matches demonstrated format exactly
- [x] All extracted information present in source abstract
- [x] No information inferred or fabricated
- [x] Study type correctly classified as RCT (not just "clinical trial")
