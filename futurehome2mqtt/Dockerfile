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

RUN pip --version
RUN pip3 --version
RUN python --version
RUN python3 --version

RUN pip3 install --no-cache-dir -r /tmp/requirements.txt

RUN chmod a+x /$HOME/run.sh

CMD [ "/app/run.sh" ]
