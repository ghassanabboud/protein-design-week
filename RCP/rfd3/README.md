# RFdiffusion3

Protein structure generation via diffusion models. Uses the [RosettaCommons Foundry](https://github.com/RosettaCommons/foundry) toolchain.

- **Container**: `registry.rcp.epfl.ch/proteindesign-containers/rfd3:2026.1`

> For building and pushing the Docker image, see [docker/README.md](docker/README.md).

## Launch on RunAI

```bash
runai submit rfd3-gXX \
  --project <your-project> \
  -i registry.rcp.epfl.ch/proteindesign-containers/rfd3:2026.1 \
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
which rfd3
rfd3 --help
foundry list-installed
```

### Run a design job

```bash
mkdir -p /mnt/scratch/rfd3-demo
cd /mnt/scratch/rfd3-demo

# Create a simple input JSON
cat > demo.json << 'EOF'
{
  "uncond_monomer": {
    "dialect": 2,
    "length": [80, 100]
  }
}
EOF

# Run RFdiffusion3
rfd3 design \
  out_dir=/mnt/scratch/rfd3-demo/out \
  inputs=/mnt/scratch/rfd3-demo/demo.json \
  ckpt_path=${CKPT_PATH} \
  n_batches=1 \
  diffusion_batch_size=4
```

## Key Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `CKPT_PATH` | `/root/.foundry/checkpoints/rfd3_latest.ckpt` | Model checkpoint (bundled in image) |
| `CCD_MIRROR_PATH` | `/opt/ccd_mirror` | Chemical component dictionary |

### Override checkpoint at runtime

If weights are on the shared volume:

```bash
rfd3 design \
  out_dir=/mnt/scratch/out \
  inputs=/mnt/scratch/input.json \
  ckpt_path=/mnt/shared-ro/models/rfd3_latest.ckpt
```

## Transferring Files to RCP

```bash
rsync -av --no-group inputs/ \
  <gaspar>@jumphost.rcp.epfl.ch:/mnt/hackathon-proteindesign/hackathon-proteindesign-gXX/scratch-gXX/rfd3/
```

## References

- [Foundry GitHub](https://github.com/RosettaCommons/foundry)
- [RFdiffusion3 docs](https://subseq.bio/docs/rfdiffusion3)
- [Foundry Docker Hub](https://hub.docker.com/r/rosettacommons/foundry)
