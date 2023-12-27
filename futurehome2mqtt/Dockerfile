ARG BUILD_FROM=ghcr.io/hassio-addons/base-python:11.0.0
FROM $BUILD_FROM

# Copy Python requirements file
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY run.sh .
RUN chmod a+x run.sh

# Copy data for add-on
COPY . .

CMD [ "/run.sh" ]
