ARG BUILD_FROM=ghcr.io/hassio-addons/base-python:12.0.2
FROM ${BUILD_FROM}

ENV LANG C.UTF-8
ENV HOME=/app

RUN mkdir -p $HOME
WORKDIR ${HOME}

# Set shell
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

# Copy Python requirements file
COPY requirements.txt /tmp/requirements.txt

# Copy data for add-on
COPY ./ $HOME/

RUN /usr/local/bin/pip3 --version
RUN /usr/local/bin/python3 --version

RUN \
    apt-get update \
    \
    && apt-get install -y --no-install-recommends \
        python3-dev=3.11.2-1+b1 \
        python3=3.11.2-1+b1 \
    && curl https://bootstrap.pypa.io/get-pip.py | python3 \
    && update-alternatives \
        --install /usr/bin/python python /usr/bin/python3 10 \
    \
    && pip3 install --no-cache-dir -r /tmp/requirements.txt

RUN chmod a+x /$HOME/run.sh

CMD [ "/app/run.sh" ]
