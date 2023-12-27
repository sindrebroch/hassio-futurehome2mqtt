ARG BUILD_FROM
FROM $BUILD_FROM

ENV LANG C.UTF-8
ENV HOME=/app

RUN mkdir -p $HOME
WORKDIR ${HOME}

# Set shell
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

# Copy data for add-on
COPY ./ $HOME/

RUN apk add --no-cache --virtual py3-pip

RUN apk add --no-cache python3 

# RUN pip3 install --upgrade pip

RUN pip3 install -r requirements.txt

RUN chmod a+x /$HOME/run.sh

CMD [ "/app/run.sh" ]
