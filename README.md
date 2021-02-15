## Part Grouping Network (PGN)

### Introduction

This repo is a fork of [PGN official repository](https://github.com/Engineering-Course/CIHP_PGN.git)

PGN is a state-of-art deep learning methord for semantic part segmentation, instance-aware edge detection and instance-level human parsing.

This distribution provides a publicly available implementation for the key model ingredients reported in [Instance-level Human Parsing (ECCV 2018 paper)](http://openaccess.thecvf.com/content_ECCV_2018/papers/Ke_Gong_Instance-level_Human_Parsing_ECCV_2018_paper.pdf).

### Pre-trained models

Authors have released trained models of PGN on CIHP dataset at [google drive](https://drive.google.com/open?id=1Mqpse5Gen4V4403wFEpv3w3JAsWw2uhk).

### Prepare
```bash
# Load model checkpoint
mkdir checkpoint && cd checkpoint
```
Download here checkpoint
```
unzip CIHP_PGN.zip
rm CIHP_PGN.zip
cd ..
```

### Build docker image
```
docker build -t clofit/multiview_segmentation:latest .
docker run --gpus all --rm --name infer_multiview_segmentation -v ${data_path}:/data/ clofit/multiview_segmentation:latest /bin/bash
```

### Inference
```
python batch_inference.py --data_dir /data/${frames_dir} --output /data/segmentation/ --checkpoint /code/checkpoint/CIHP_pgn
```
Masked source images will as well as resized masks will be written to `{OUTPUT_DIR}/overlay` 