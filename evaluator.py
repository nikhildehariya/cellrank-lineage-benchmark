import os
import json
import sys
from pathlib import Path

def evaluate(answer_file=None):
    results = {
        "score": 0.0,
        "passed_all": False,
        "rule_1_schema": False,
        "rule_2_gene": False,
        "rule_3_correlation": False,
        "failure_reason": None,
        "details": {}
    }
    
    # Locate answer file across common candidate paths
    if answer_file is None:
        base_dir = Path(__file__).resolve().parent
        candidates = [
            base_dir / "output" / "answer.json",
            Path.cwd() / "output" / "answer.json",
            base_dir / "answer.json",
            Path.cwd() / "answer.json",
        ]
        for c in candidates:
            if c.exists():
                answer_file = c
                break
        if answer_file is None:
            answer_file = candidates[0]
    else:
        answer_file = Path(answer_file)
        
    if not answer_file.exists():
        results["failure_reason"] = f"Answer file '{answer_file}' does not exist."
        return results
        
    try:
        with open(answer_file, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        results["failure_reason"] = f"Failed to parse JSON: {e}"
        return results
        
    if not isinstance(data, dict):
        results["failure_reason"] = "Root JSON element must be an object."
        return results
        
    required_keys = ["terminal_state", "top_driver_gene", "correlation"]
    for k in required_keys:
        if k not in data:
            results["failure_reason"] = f"Missing required key '{k}'."
            return results
            
    results["rule_1_schema"] = True
    results["details"]["parsed_data"] = data
    
    # Rule 2: Top Driver Gene Check (case-insensitive for robustness)
    gene_raw = str(data["top_driver_gene"]).strip()
    gene_norm = gene_raw.lower()
    
    if gene_norm == "id2":
        results["rule_2_gene"] = True
    elif gene_norm == "ccl5":
        results["failure_reason"] = "Trap 1 (Static Differential Expression): Reported 'Ccl5' (used static sc.tl.rank_genes_groups on terminal clusters instead of continuous trajectory lineage driver correlation)."
        return results
    elif gene_norm == "cd74":
        results["failure_reason"] = "Trap 2 (Global Pseudotime Shortcut): Reported 'Cd74' (correlated expression directly against global 1D pseudotime instead of lineage-specific fate absorption probabilities)."
        return results
    else:
        results["failure_reason"] = f"Incorrect top driver gene '{gene_raw}'. Expected 'Id2'."
        return results
        
    # Rule 3: Quantitative Correlation Check
    try:
        corr = float(data["correlation"])
    except (ValueError, TypeError):
        results["failure_reason"] = f"Correlation value '{data.get('correlation')}' is not a valid float."
        return results
        
    if 0.74 <= corr <= 0.78:
        results["rule_3_correlation"] = True
        results["passed_all"] = True
        results["score"] = 1.0
        return results
    elif 0.45 <= corr <= 0.50:
        results["failure_reason"] = f"Trap 2 Quantitative Match: Correlation {corr} matches global 1D pseudotime (~0.477), not lineage fate absorption correlation."
        return results
    else:
        results["failure_reason"] = f"Correlation {corr} is outside the tolerance interval [0.74, 0.78]."
        return results

if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else None
    res = evaluate(target)
    print(json.dumps(res, indent=2))
    if not res["passed_all"]:
        sys.exit(1)
    sys.exit(0)
