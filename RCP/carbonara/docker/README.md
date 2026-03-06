# CARBonAra - Docker Build

Container image for CARBonAra protein sequence design.

## Prerequisites

- Docker with `--platform linux/amd64` support
- Access to the RCP container registry (`registry.rcp.epfl.ch`)

## Build

Build from the `carbonara/docker/` directory:

```bash
cd carbonara/docker

docker build --platform linux/amd64 \
  -t registry.rcp.epfl.ch/proteindesign-containers/carbonara:2026.1 .
```

## Push to RCP Registry

```bash
docker login registry.rcp.epfl.ch
docker push registry.rcp.epfl.ch/proteindesign-containers/carbonara:2026.1
```

## Image Details

- **Base image:** `nvidia/cuda:11.8.0-runtime-ubuntu22.04`
- **Python:** 3.10
- **Key packages:** CARBonAra (cloned from GitHub at build time)
- **Model weights:** Pre-downloaded during build (cached in `~/.cache/huggingface`)
