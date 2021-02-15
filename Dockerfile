FROM tensorflow/tensorflow:1.11.0-gpu
MAINTAINER CLOFIT.ME (ceo@clofit.me)

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

# Install dependencies
RUN apt-get update && apt-get install -y \
    libsm6 \
    libxext6 \
    libxrender-dev \
    python-tk \
    ffmpeg

COPY . /code/
RUN pip install -r /code/requirements.txt
WORKDIR /code