# AlphaFold 3 - Docker Build

Container image for AlphaFold 3 biomolecular structure prediction.

## Prerequisites

- Docker with `--platform linux/amd64` support
- Access to the RCP container registry (`registry.rcp.epfl.ch`)

## Build

Build from the `af3/docker/` directory:

```bash
cd af3/docker

docker build --platform linux/amd64 \
  -t registry.rcp.epfl.ch/proteindesign-containers/af3:2026.1 .
```

## Push to RCP Registry

```bash
docker login registry.rcp.epfl.ch
docker push registry.rcp.epfl.ch/proteindesign-containers/af3:2026.1
```

## Image Details

- **Base image:** `nvidia/cuda:12.6.3-base-ubuntu24.04`
- **Python:** 3.12 (managed via uv)
- **Key packages:** AlphaFold 3 (cloned from GitHub at build time)
- **Model weights:** NOT included -- each user must download their own from Google

## Environment Variables Set in Image

| Variable | Value | Purpose |
|----------|-------|---------|
| `XLA_FLAGS` | `--xla_gpu_enable_triton_gemm=false` | XLA GPU config |
| `XLA_PYTHON_CLIENT_PREALLOCATE` | `false` | Don't preallocate GPU memory |
| `TF_FORCE_UNIFIED_MEMORY` | `1` | Enable unified memory |
| `XLA_CLIENT_MEM_FRACTION` | `1.5` | Allow memory oversubscription |
