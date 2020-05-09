FROM tensorflow/tensorflow:1.11.0-gpu
LABEL maintainer="arseniy.poyezzhayev@gmail.com"

# Install dependencies
RUN apt-get update && apt-get install -y \
    libsm6 \
    libxext6 \
    libxrender-dev \
    python-tk

RUN pip install --upgrade pip
# To always get non-cached version of requirements.txt
COPY requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt
COPY . /tmp/
