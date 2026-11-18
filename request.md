We are investigating lineage commitment during early myeloid differentiation using single-cell transcriptomics data stored in `data/myeloid_clean.h5ad`. Using the `cellrank` toolkit provided in `repo/`, identify the primary lineage driver gene and its quantitative association with the differentiation trajectory toward terminal state "0".

Begin by preprocessing the raw count data according to standard single-cell quality control protocols: filter out lowly expressed genes with fewer than 10 cells (`min_cells=10`), apply library-size normalization followed by log-transformation (`sc.pp.log1p`), and identify the top 1,000 highly variable genes (`n_top_genes=1000`). Construct cell representations and the neighborhood graph using `random_state=0` (`n_neighbors=15`, `n_pcs=20`).

Using diffusion pseudotime rooted at index 0 (`adata.uns['iroot'] = 0`), model the continuous transition dynamics toward the 3 primary mature macrostates/terminal fates (`random_state=0`). Determine the top lineage driver gene governing commitment toward terminal state "0" and its Pearson correlation value.

Save your final results to `output/answer.json` formatted as:
```json
{
  "terminal_state": "0",
  "top_driver_gene": "<gene_symbol>",
  "correlation": <float_correlation>
}
```
