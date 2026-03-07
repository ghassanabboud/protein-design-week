# RFdiffusion3 - Docker Build

Container image for RFdiffusion3 protein structure generation.

## Prerequisites

- Docker with `--platform linux/amd64` support
- Access to the RCP container registry (`registry.rcp.epfl.ch`)

## Build

Build from the `rfd3/docker/` directory using `Dockerfile.rfd3`:

```bash
cd rfd3/docker

docker build --platform linux/amd64 \
  -t registry.rcp.epfl.ch/proteindesign-containers/rfd3:2026.1 \
  -f Dockerfile.rfd3 .
```

## Push to RCP Registry

```bash
docker login registry.rcp.epfl.ch
docker push registry.rcp.epfl.ch/proteindesign-containers/rfd3:2026.1
```

## Image Details

- **Base image:** `nvidia/cuda:12.4.1-devel-ubuntu22.04`
- **Python:** 3.12
- **Key packages:** `rc-foundry[all]`, RFdiffusion3 (installed via foundry)
- **Model weights:** Bundled in image at `/root/.foundry/checkpoints/rfd3_latest.ckpt`
- **CCD mirror:** Downloaded during build to `/opt/ccd_mirror/components.cif`
