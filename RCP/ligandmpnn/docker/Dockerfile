FROM nvidia/cuda:11.8.0-runtime-ubuntu22.04

#####################################
# Environment
#####################################
ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1 \
    PATH="/opt/venv/bin:${PATH}" \
    XDG_CACHE_HOME=/tmp/cache

#####################################
# System packages
#####################################
RUN set -eux; \
    umask 0000; \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        python3.10 \
        python3.10-venv \
        python3.10-dev \
        python3-pip \
        build-essential \
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
# Clone LigandMPNN and install deps
#####################################
RUN git clone https://github.com/dauparas/LigandMPNN.git /opt/LigandMPNN && \
    cd /opt/LigandMPNN && \
    /opt/venv/bin/pip install --no-cache-dir \
        torch \
        "numpy<1.24" \
        prody \
        biopython \
        ml-collections \
        dm-tree

#####################################
# Download model weights
#####################################
RUN cd /opt/LigandMPNN && \
    bash get_model_params.sh /opt/LigandMPNN/model_params

#####################################
# Permissions (world-writable for multi-user)
#####################################
RUN chmod -R 777 /opt /tmp /root

#####################################
# Default user / workdir
#####################################
WORKDIR /opt/LigandMPNN
CMD ["/bin/bash"]
