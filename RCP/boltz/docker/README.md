# Boltz - Docker Build

Container image for Boltz biomolecular structure prediction.

## Prerequisites

- Docker with `--platform linux/amd64` support
- Access to the RCP container registry (`registry.rcp.epfl.ch`)

## Build

Build from the `boltz/docker/` directory:

```bash
cd boltz/docker

docker build --platform linux/amd64 \
  -t registry.rcp.epfl.ch/proteindesign-containers/boltz:2026.1 .
```

## Push to RCP Registry

```bash
docker login registry.rcp.epfl.ch
docker push registry.rcp.epfl.ch/proteindesign-containers/boltz:2026.1
```

## Image Details

- **Base image:** `nvidia/cuda:12.4.1-devel-ubuntu22.04`
- **Python:** 3.11
- **Key packages:** `boltz[cuda]`
- **Model weights:** Automatically downloaded on first run to `$BOLTZ_CACHE_DIR` (`/opt/boltz_cache`)
