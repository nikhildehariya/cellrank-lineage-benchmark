# Grading Rules

1. **Output Existence & Schema Compliance:**
   - **Pass:** `output/answer.json` exists, is valid JSON, and contains keys `"terminal_state"`, `"top_driver_gene"`, and `"correlation"`.
   - **Fail:** File missing, invalid JSON syntax, or missing any of the required keys.

2. **Categorical Driver Gene Verification:**
   - **Pass:** `"top_driver_gene"` is `"Id2"`.
   - **Fail (Discrete Cluster Trap):** `"top_driver_gene"` is `"Ccl5"` (indicates using static differential expression `sc.tl.rank_genes_groups` on terminal cells instead of continuous trajectory lineage driver correlation).
   - **Fail (Global Pseudotime Trap):** `"top_driver_gene"` is `"Cd74"` (indicates correlating gene expression directly against global diffusion pseudotime rather than lineage-specific fate absorption probabilities).
   - **Fail (General):** Any other gene symbol.

3. **Quantitative Correlation Tolerance:**
   - **Pass:** `"correlation"` is between **0.74** and **0.78** (inclusive).
   - **Fail:** Correlation is approximately 0.48 (global pseudotime shortcut) or falls outside the [0.74, 0.78] tolerance interval.
