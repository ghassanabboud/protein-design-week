# AlphaFold 3 — MSA & Templates Pipeline Guide

This guide explains how to **split** the AF3 workflow into two stages:

1. **Data pipeline only** — generate MSAs and templates (CPU-heavy, no GPU needed for the search itself but the container requires GPU allocation)
2. **Inference only** — fold using pre-computed MSAs and templates (GPU-heavy)

This is useful when you want to:
- Run the data pipeline once, then reuse the MSA/templates across multiple folding runs
- Provide custom MSAs or templates from external sources
- Skip the slow database search when re-folding with different seeds or parameters

> **Cluster database path:** `/mnt/shared-ro/models/af3_db/af3_db/`

---

## Stage 1: Generate MSA & Templates Only

### Submit the job

```bash
runai submit af3-msa-gXX \
  --project hackathon-proteindesign-<gaspar> \
  -i registry.rcp.epfl.ch/proteindesign-containers/af3:2026.1 \
  --interactive --attach --node-pools default -g 1 \
  --existing-pvc claimname=hackathon-proteindesign-scratch-gXX,path=/mnt/scratch \
  --existing-pvc claimname=hackathon-proteindesign-shared-ro,path=/mnt/shared-ro \
  --command -- /bin/bash
```

### Create your input JSON

```bash
mkdir -p /mnt/scratch/<your_project>/af3_msa
cd /mnt/scratch/<your_project>/af3_msa

cat > input.json << 'EOF'
{
  "name": "my_protein",
  "dialect": "alphafold3",
  "version": 2,
  "modelSeeds": [42],
  "sequences": [
    {
      "protein": {
        "id": ["A"],
        "sequence": "MNIFEMLRIDEGLRLKIYKDTEGYYTIGIGHLLTKSPSLNAAKSELDKAIGRNTGVITKDEAEKLFNQDVTAAAEELGLTQWPMFVVIIAKSATSAAHEEVKPSLL"
      }
    }
  ]
}
EOF
```

> **Note:** Do NOT include `"unpairedMsa": ""`, `"pairedMsa": ""`, or `"templates": []` here — leaving them out tells AF3 to run the data pipeline and search the databases to populate them.

### Run the data pipeline only (no inference)

```bash
python /opt/alphafold3/run_alphafold.py \
  --json_path /mnt/scratch/<your_project>/af3_msa/input.json \
  --model_dir /mnt/scratch/af3_weights \
  --db_dir /mnt/shared-ro/models/af3_db/af3_db \
  --output_dir /mnt/scratch/<your_project>/af3_msa/output \
  --jax_compilation_cache_dir /mnt/scratch/af3_jax_cache \
  --norun_inference
```

The key flag is **`--norun_inference`** — this runs only the data pipeline (MSA search + template search) and skips the model prediction step.

### What gets produced

After the data pipeline completes, you will find a `_data.json` file in the output directory:

```
output/my_protein/my_protein_data.json
```

This file is an enriched version of your input JSON. It contains the same structure but with the `unpairedMsa`, `pairedMsa`, and `templates` fields now populated with the search results from the databases.

### Clean up

```bash
exit
runai delete job af3-msa-gXX
```

---

## Stage 2: Fold Using Pre-computed MSA & Templates

Now you can use the `_data.json` from Stage 1 as input, skipping the data pipeline entirely.

### Submit a new job

```bash
runai submit af3-fold-gXX \
  --project hackathon-proteindesign-<gaspar> \
  -i registry.rcp.epfl.ch/proteindesign-containers/af3:2026.1 \
  --interactive --attach --node-pools default -g 1 \
  --existing-pvc claimname=hackathon-proteindesign-scratch-gXX,path=/mnt/scratch \
  --existing-pvc claimname=hackathon-proteindesign-shared-ro,path=/mnt/shared-ro \
  --command -- /bin/bash
```

### Run inference only (skip data pipeline)

```bash
python /opt/alphafold3/run_alphafold.py \
  --json_path /mnt/scratch/<your_project>/af3_msa/output/my_protein/my_protein_data.json \
  --model_dir /mnt/scratch/af3_weights \
  --output_dir /mnt/scratch/<your_project>/af3_fold/output \
  --jax_compilation_cache_dir /mnt/scratch/af3_jax_cache \
  --norun_data_pipeline
```

The key flag is **`--norun_data_pipeline`** — this skips the MSA/template search and goes straight to structure prediction using whatever is already in the JSON.

### Verify outputs

```bash
ls /mnt/scratch/<your_project>/af3_fold/output/my_protein/seed-42_sample-*/
# Expect: *_model.cif, *_confidences.json, *_summary_confidences.json
```

---

## Using Custom / External MSAs and Templates

You can also manually provide your own MSA and templates in the input JSON, then fold with `--norun_data_pipeline`. Here is the full JSON format:

```json
{
  "name": "my_protein_custom_msa",
  "dialect": "alphafold3",
  "version": 2,
  "modelSeeds": [42],
  "numDiffusionSamples": 5,
  "sequences": [
    {
      "protein": {
        "id": ["A"],
        "sequence": "MNIFEMLRIDEGLRLKIYKDTEGYYTIGIGHLLTKSPSLNAAKSELDKAIGRNTGVITKDEAEKLFNQDVTAAAEELGLTQWPMFVVIIAKSATSAAHEEVKPSLL",
        "unpairedMsa": ">query\nMNIFEMLRIDEGLRLKIYKDTEGYYTIGIGHLLTKSPSLNAAKSELDKAIGRNTGVITKDEAEKLFNQDVTAAAEELGLTQWPMFVVIIAKSATSAAHEEVKPSLL\n>hit1\nMNIFEMLRIDEGLRLKIYKDTEGYYTIGIGHLLTKSPSLNAAKSELDKAIGRNTGVITKDEAEKLFNQDVTAAAEELGLTQWPMFVVIIAKSATSAAHEEVKPSLL\n",
        "pairedMsa": "",
        "templates": []
      }
    }
  ]
}
```

### MSA format

- **`unpairedMsa`**: A2M/FASTA format string. The first sequence MUST be the query sequence. Each entry is `>header\nSEQUENCE\n`. Gaps are represented as `-`. Insertions (lowercase) are allowed.
- **`pairedMsa`**: Same format, used for multi-chain complexes where sequences are paired across chains. Leave as `""` for monomers.
- Set both to `""` (empty string) to fold with **no MSA** (single-sequence mode — useful for designed proteins).

### Templates format

```json
"templates": [
  {
    "mmcifPath": "/mnt/scratch/<your_project>/templates/4hhb.cif",
    "queryIndices": [0, 1, 2, 3, 4],
    "templateIndices": [0, 1, 2, 3, 4]
  }
]
```

- **`mmcifPath`**: Path to a template structure in mmCIF format.
- **`queryIndices`**: 0-based residue indices in your query sequence that align to the template.
- **`templateIndices`**: Corresponding 0-based residue indices in the template structure.
- Set to `[]` (empty list) to fold with **no templates**.

---

## Quick Reference — Key Flags

| Flag | What it does |
|------|-------------|
| `--norun_inference` | Run data pipeline only (MSA + templates search). No GPU prediction. |
| `--norun_data_pipeline` | Skip data pipeline. Use MSA/templates already in the JSON. |
| `--db_dir` | Path to AF3 genetic databases (needed for data pipeline). On this cluster: `/mnt/shared-ro/models/af3_db/af3_db` |
| `--model_dir` | Path to model weights |
| `--json_path` | Input JSON (or `_data.json` from a previous data pipeline run) |
| `--jax_compilation_cache_dir` | JAX cache (reuse across runs for faster startup) |

---

## Typical Two-Stage Workflow Summary

```
┌─────────────────────────────────────────────────┐
│  Stage 1: Data Pipeline (--norun_inference)      │
│                                                   │
│  input.json ──► MSA search + template search     │
│                  against databases at             │
│                  /mnt/shared-ro/models/af3_db/    │
│                                                   │
│  Output: my_protein_data.json                     │
│          (input + populated MSA & templates)      │
└──────────────────────┬──────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────┐
│  Stage 2: Inference (--norun_data_pipeline)       │
│                                                   │
│  my_protein_data.json ──► Structure prediction    │
│                                                   │
│  Output: *_model.cif, *_confidences.json,         │
│          *_summary_confidences.json                │
└─────────────────────────────────────────────────┘
```

---

*Developed by [Benedikt Singer](mailto:benedikt.singer@epfl.ch) with [Claude Opus 4.6](https://www.anthropic.com) (Anthropic).*
