# Chai-1 - Docker Build

Container image for Chai-1 multi-modal biomolecular structure prediction.

## Prerequisites

- Docker with `--platform linux/amd64` support
- Access to the RCP container registry (`registry.rcp.epfl.ch`)

## Build

Build from the `chai/docker/` directory:

```bash
cd chai/docker

docker build --platform linux/amd64 \
  -t registry.rcp.epfl.ch/proteindesign-containers/chai:2026.1 .
```

## Push to RCP Registry

```bash
docker login registry.rcp.epfl.ch
docker push registry.rcp.epfl.ch/proteindesign-containers/chai:2026.1
```

## Image Details

- **Base image:** `nvidia/cuda:12.4.1-runtime-ubuntu22.04`
- **Python:** 3.10 (managed via uv)
- **Key packages:** `chai_lab`
- **Model weights:** Loaded at runtime from `$CHAI_DOWNLOADS_DIR` (default: `/mnt/shared-ro/weights/chai/chai-weights`)
