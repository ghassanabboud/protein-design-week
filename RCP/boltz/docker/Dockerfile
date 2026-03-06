FROM nvidia/cuda:12.4.1-devel-ubuntu22.04

#####################################
# Environment
#####################################
ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1 \
    PATH="/opt/venv/bin:${PATH}" \
    BOLTZ_CACHE_DIR=/opt/boltz_cache \
    XDG_CACHE_HOME=/tmp/cache

#####################################
# System packages + Python 3.11
#####################################
RUN set -eux; \
    umask 0000; \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        software-properties-common \
        wget \
        curl \
        git \
        build-essential \
        ca-certificates \
        python3-pip && \
    add-apt-repository ppa:deadsnakes/ppa && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        python3.11 \
        python3.11-venv \
        python3.11-dev && \
    rm -rf /var/lib/apt/lists/*

#####################################
# Python venv + pip
#####################################
RUN python3.11 -m venv /opt/venv && \
    /opt/venv/bin/pip install --upgrade pip setuptools wheel

#####################################
# Install Boltz with CUDA support
#####################################
RUN /opt/venv/bin/pip install --no-cache-dir "boltz[cuda]"

#####################################
# Cache and working directories
# World-writable for multi-user access
#####################################
RUN mkdir -p /opt/boltz_cache /tmp/cache && \
    chmod -R 777 /opt /tmp

#####################################
# Default user / workdir
# No fixed UID/GID — RunAI overrides at runtime
#####################################
WORKDIR /root
CMD ["/bin/bash"]
