FROM nvidia/cuda:12.6.3-base-ubuntu24.04

#####################################
# Environment
#####################################
ENV DEBIAN_FRONTEND=noninteractive \
    PATH="/opt/alphafold3_venv/bin:/root/.local/bin:${PATH}" \
    XLA_FLAGS="--xla_gpu_enable_triton_gemm=false" \
    XLA_PYTHON_CLIENT_PREALLOCATE=false \
    TF_FORCE_UNIFIED_MEMORY=1 \
    XLA_CLIENT_MEM_FRACTION=1.5 \
    UV_PROJECT_ENVIRONMENT=/opt/alphafold3_venv \
    UV_NO_SYNC=1 \
    UV_COMPILE_BYTECODE=0 \
    XDG_CACHE_HOME=/tmp/cache

#####################################
# System packages + Python 3.12
#####################################
RUN set -eux; \
    umask 0000; \
    apt-get update --quiet && \
    apt-get install --yes --quiet --no-install-recommends \
        curl \
        python3.12 \
        python3.12-dev \
        git \
        wget \
        gcc \
        g++ \
        make \
        zlib1g-dev \
        zstd \
        ca-certificates && \
    rm -rf /var/lib/apt/lists/*

#####################################
# Install uv (pinned version)
#####################################
RUN curl -LsSf https://astral.sh/uv/0.9.24/install.sh | sh

#####################################
# Clone AlphaFold 3 source
#####################################
RUN git clone https://github.com/google-deepmind/alphafold3.git /opt/alphafold3

#####################################
# Create venv and install deps
#####################################
RUN uv venv $UV_PROJECT_ENVIRONMENT && \
    cd /opt/alphafold3 && \
    UV_LINK_MODE=copy uv sync --frozen --all-groups --no-editable

#####################################
# Build chemical components database
#####################################
RUN cd /opt/alphafold3 && \
    uv run build_data

#####################################
# Permissions (world-writable for multi-user)
#####################################
RUN mkdir -p /tmp/cache && \
    chmod -R 777 /opt /tmp /root

#####################################
# Default user / workdir
# Weights are NOT included — each user uploads
# their own to /mnt/scratch or binds them at runtime.
#####################################
WORKDIR /root
CMD ["/bin/bash"]
