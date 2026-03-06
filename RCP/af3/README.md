# AlphaFold 3

Biomolecular structure prediction from Google DeepMind. Predicts the 3D structure of protein complexes, nucleic acids, ligands, and more.

- **GitHub**: https://github.com/google-deepmind/alphafold3
- **Container**: `registry.rcp.epfl.ch/proteindesign-containers/af3:2026.1`
- **Important**: Model weights must be downloaded individually by each user from Google. They are **NOT** included in the container image.

> For building and pushing the Docker image, see [docker/README.md](docker/README.md).

## Obtaining Model Weights

Each user must request and download AlphaFold 3 weights from Google:

1. Request access at https://forms.gle/svvpY4u2jsHEwWYS6
2. Once approved, download the model parameters
3. Upload the weights to your scratch storage:

```bash
rsync -av --no-group af3_weights/ \
  <gaspar>@jumphost.rcp.epfl.ch:/mnt/hackathon-proteindesign/hackathon-proteindesign-gXX/scratch-gXX/af3_weights/

rsync af3.bin.zst <gaspar>@jumphost.rcp.epfl.ch:/mnt/hackathon-proteindesign/hackathon-proteindesign-gXX/scratch-gXX/<af3-folder>
```

## Launch on RunAI

```bash
runai submit af3-gXX \
  --project <your-project> \
  -i registry.rcp.epfl.ch/proteindesign-containers/af3:2026.1 \
  --interactive \
  --attach \
  --node-pools default \
  -g 1 \
  --existing-pvc claimname=hackathon-proteindesign-scratch-gXX,path=/mnt/scratch \
  --existing-pvc claimname=hackathon-proteindesign-shared-ro,path=/mnt/shared-ro \
  --command -- /bin/bash
```

Replace `gXX` with your group number and `<your-project>` with your RunAI project name.

## Getting Started

### 1. Create an input JSON

```bash
mkdir -p /mnt/scratch/af3-demo
cd /mnt/scratch/af3-demo

cat > input.json << 'EOF'
{
  "name": "test_prediction",
  "dialect": "alphafold3",
  "version": 2,
  "modelSeeds": [1],
  "sequences": [
    {
      "protein": {
        "id": ["A"],
        "sequence": "MNIFEMLRIDEGLRLKIYKDTEGYYTIGIGHLLTKSPSLNAAKSELDKAIGRNTGVITKDEAEKLFNQDVTAAAEELGLTQWPMFVVIIAKSATSAAHEEVKPSLL",
        "unpairedMsa": "",
        "pairedMsa": "",
        "templates": []
      }
    }
  ]
}
EOF
```

### 2. Run AlphaFold 3

```bash
python /opt/alphafold3/run_alphafold.py \
  --json_path /mnt/scratch/af3-demo/input.json \
  --model_dir /mnt/scratch/af3-demo/weights \
  --output_dir /mnt/scratch/af3-demo/output \
  --jax_compilation_cache_dir /mnt/scratch/af3-demo/jax_cache \
  --norun_data_pipeline
```

## Key Flags

| Flag | Description |
|------|-------------|
| `--json_path` | Path to input JSON file |
| `--model_dir` | Path to downloaded model weights |
| `--output_dir` | Where to write predictions |
| `--jax_compilation_cache_dir` | JAX cache dir (speeds up subsequent runs) |

## GPU Requirements

- Recommended: A100 80GB
- Reuse the same `jax_cache` directory across runs -- JAX compilation cache significantly speeds up repeated runs

## References

- [AlphaFold 3 GitHub](https://github.com/google-deepmind/alphafold3)
- [AlphaFold 3 paper](https://doi.org/10.1038/s41586-024-07487-w)
