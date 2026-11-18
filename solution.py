import os
import sys
import json
from pathlib import Path

# Ensure repo/src is on sys.path if running against the local repository
repo_src = Path(__file__).resolve().parent / "repo" / "src"
if repo_src.exists():
    sys.path.insert(0, str(repo_src))

import scanpy as sc
import cellrank as cr

def run_golden_solution():
    base_dir = Path(__file__).resolve().parent
    data_path = base_dir / "data" / "myeloid_clean.h5ad"
    if not data_path.exists():
        raise FileNotFoundError(f"Input data not found at {data_path}.")
        
    adata = sc.read_h5ad(data_path)
    
    # 1. Preprocessing
    sc.pp.filter_genes(adata, min_cells=10)
    sc.pp.normalize_total(adata)
    sc.pp.log1p(adata)
    sc.pp.highly_variable_genes(adata, n_top_genes=1000)
    
    # 2. Dimensional reduction & Neighborhood graph
    sc.pp.pca(adata, random_state=0)
    sc.pp.neighbors(adata, n_neighbors=15, n_pcs=20, random_state=0)
    
    # 3. Diffusion Map & Pseudotime
    sc.tl.diffmap(adata)
    adata.uns['iroot'] = 0
    sc.tl.dpt(adata)
    
    # 4. CellRank Pseudotime Kernel
    pk = cr.kernels.PseudotimeKernel(adata, time_key='dpt_pseudotime')
    pk.compute_transition_matrix()
    
    # 5. GPCCA Estimator
    g = cr.estimators.GPCCA(pk)
    g.compute_schur(n_components=10)
    g.compute_macrostates(n_states=3)
    g.predict_terminal_states()
    g.compute_fate_probabilities()
    
    # 6. Lineage Drivers for Terminal State 0
    drivers = g.compute_lineage_drivers(lineages='0')
    top_gene = str(drivers.index[0])
    top_corr = float(drivers['0_corr'].iloc[0])
    
    print(f"[Golden Solution Result] Terminal State '0' Top Driver: {top_gene}, Correlation: {top_corr:.4f}")
    
    output_dir = base_dir / "output"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_payload = {
        "terminal_state": "0",
        "top_driver_gene": top_gene,
        "correlation": round(top_corr, 4)
    }
    
    with open(output_dir / "answer.json", "w") as f:
        json.dump(output_payload, f, indent=2)
        
    return output_payload

if __name__ == "__main__":
    run_golden_solution()
