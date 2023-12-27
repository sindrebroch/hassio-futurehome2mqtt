ARG BUILD_FROM
FROM $BUILD_FROM

ENV LANG C.UTF-8
ENV HOME=/app

RUN mkdir -p $HOME
WORKDIR ${HOME}

# Set shell
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

RUN apk add --no-cache --virtual python3 py3-pip && \
    pip3 install --upgrade pip

# Copy data for add-on
COPY ./ $HOME/

RUN pip3 install -r requirements.txt
RUN chmod a+x /$HOME/run.sh


CMD [ "/app/run.sh" ]
