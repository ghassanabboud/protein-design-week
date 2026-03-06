# Chai-1

Multi-modal biomolecular structure prediction for proteins, small molecules, DNA, RNA, and glycosylations.

- **GitHub**: https://github.com/chaidiscovery/chai-lab
- **Container**: `registry.rcp.epfl.ch/proteindesign-containers/chai:2026.1`
- **License**: Apache 2.0 (code and weights)

> For building and pushing the Docker image, see [docker/README.md](docker/README.md).

## Launch on RunAI

```bash
runai submit chai-gXX \
  --project <your-project> \
  -i registry.rcp.epfl.ch/proteindesign-containers/chai:2026.1 \
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

### Check installation

```bash
python3 -c "from chai_lab.chai1 import run_inference; print('OK')"
```

### Run a fold prediction

```bash
mkdir -p /mnt/scratch/chai-demo
cd /mnt/scratch/chai-demo

# Create a FASTA input file
cat > input.fasta << 'EOF'
>protein|name=example
MNIFEMLRIDEGLRLKIYKDTEGYYTIGIGHLLTKSPSLNAAKSELDKAIGRNTGVITKDEAEKLFNQDVTAAAEELGLTQWPMFVVIIAKSATSAAHEEVKPSLL
EOF

# Run Chai-1 fold
python3 << 'PYEOF'
from pathlib import Path
from chai_lab.chai1 import run_inference

candidates = run_inference(
    fasta_file=Path("/mnt/scratch/chai-demo/input.fasta"),
    output_dir=Path("/mnt/scratch/chai-demo/output"),
    num_trunk_recycles=3,
    num_diffn_timesteps=200,
    seed=42,
)
PYEOF
```

## Model Weights

Model weights are loaded from the shared volume at `/mnt/shared-ro/weights/chai/chai-weights` (configured via `$CHAI_DOWNLOADS_DIR` in the container).

To use a different weights location:

```bash
export CHAI_DOWNLOADS_DIR=/mnt/scratch/chai-weights
```

## GPU Requirements

- Recommended: A100 80GB or H100 80GB
- Also works on: L40S 48GB, RTX 4090, A10, A30 (for smaller complexes)

## References

- [Chai-lab GitHub](https://github.com/chaidiscovery/chai-lab)
