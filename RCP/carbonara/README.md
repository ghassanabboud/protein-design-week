# CARBonAra

Protein sequence design tool from EPFL (LBM lab). Designs amino acid sequences conditioned on protein backbone structures.

- **GitHub**: https://github.com/LBM-EPFL/CARBonAra
- **Container**: `registry.rcp.epfl.ch/proteindesign-containers/carbonara:2026.1`
- **Model weights**: Pre-downloaded in the container image (cached in `~/.cache/huggingface`)

> For building and pushing the Docker image, see [docker/README.md](docker/README.md).

## Launch on RunAI

```bash
runai submit carbonara-gXX \
  --project <your-project> \
  -i registry.rcp.epfl.ch/proteindesign-containers/carbonara:2026.1 \
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
carbonara --help
```

### Run a prediction

```bash
mkdir -p /mnt/scratch/carbonara-demo
cd /mnt/scratch/carbonara-demo

# Run CARBonAra on a PDB file (args: pdb_filepath output_dir)
carbonara /mnt/scratch/carbonara-demo/input.pdb \
          /mnt/scratch/carbonara-demo/output
```

### Python API

```python
from carbonara import CARBonAra

model = CARBonAra(device_name='cuda')
# See CARBonAra documentation for API usage
```

## References

- [CARBonAra GitHub](https://github.com/LBM-EPFL/CARBonAra)
