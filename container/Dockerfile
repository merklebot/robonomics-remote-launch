FROM ros:melodic-ros-base-bionic

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN DEBIAN_FRONTEND=noninteractive apt-get -yqq update && \
    apt-get install -yqq software-properties-common && \
    add-apt-repository ppa:deadsnakes/ppa && \
    apt-get -yqq update && \
    apt-get install -yqq --no-install-recommends \
        build-essential \
        ca-certificates \
        curl \
        git \
        ssh \
        libssl-dev \
        pkg-config \
        python3.8 \
        python3-pip \
        ffmpeg  \
        libsm6 \
        xvfb \
        freeglut3 \
        freeglut3-dev \
        libxext6 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

ENV RUSTUP_HOME=/rust
ENV CARGO_HOME=/cargo
ENV PATH=/cargo/bin:/rust/bin:$PATH

RUN echo "(curl https://sh.rustup.rs -sSf | sh -s -- -y --default-toolchain nightly --no-modify-path) && rustup default nightly" > /install-rust.sh && chmod 755 /install-rust.sh
RUN /install-rust.sh
ENV PATH="/root/.cargo/bin:${PATH}"


COPY requirements.txt requirements.txt
RUN python3.8 -m pip install --upgrade pip
RUN python3.8 -m pip install -r requirements.txt

