FROM nvidia/cuda:11.8.0-runtime-ubuntu22.04

#####################################
# Environment
#####################################
ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1 \
    PATH="/opt/venv/bin:${PATH}" \
    XDG_CACHE_HOME=/tmp/cache \
    USER=user

#####################################
# System packages
#####################################
RUN set -eux; \
    umask 0000; \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        python3.10 \
        python3.10-venv \
        python3-pip \
        git \
        wget \
        ca-certificates && \
    rm -rf /var/lib/apt/lists/*

#####################################
# Python venv + pip
#####################################
RUN python3.10 -m venv /opt/venv && \
    /opt/venv/bin/pip install --upgrade pip setuptools wheel

#####################################
# Install CARBonAra from GitHub
#####################################
RUN git clone https://github.com/LBM-EPFL/CARBonAra.git /opt/CARBonAra && \
    /opt/venv/bin/pip install --no-cache-dir /opt/CARBonAra

#####################################
# Pre-download model weights
# Weights are cached in ~/.cache/huggingface
#####################################
RUN /opt/venv/bin/python -c "from carbonara import CARBonAra; model = CARBonAra(device_name='cpu')"

#####################################
# Permissions (world-writable for multi-user)
#####################################
RUN chmod -R 777 /opt /tmp /root

#####################################
# Default user / workdir
#####################################
WORKDIR /root
CMD ["/bin/bash"]
