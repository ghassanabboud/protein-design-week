# LigandMPNN - Docker Build

Container image for LigandMPNN protein sequence design.

## Prerequisites

- Docker with `--platform linux/amd64` support
- Access to the RCP container registry (`registry.rcp.epfl.ch`)

## Build

Build from the `ligandmpnn/docker/` directory:

```bash
cd ligandmpnn/docker

docker build --platform linux/amd64 \
  -t registry.rcp.epfl.ch/proteindesign-containers/ligandmpnn:2026.1 .
```

## Push to RCP Registry

```bash
docker login registry.rcp.epfl.ch
docker push registry.rcp.epfl.ch/proteindesign-containers/ligandmpnn:2026.1
```

## Image Details

- **Base image:** `nvidia/cuda:11.8.0-runtime-ubuntu22.04`
- **Python:** 3.10
- **Key packages:** LigandMPNN (cloned from GitHub), torch, prody, biopython
- **Model weights:** Downloaded during build to `/opt/LigandMPNN/model_params/`
