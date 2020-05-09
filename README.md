## Part Grouping Network (PGN)

### Introduction

This repo is a fork of [PGN official repository](https://github.com/Engineering-Course/CIHP_PGN.git)

PGN is a state-of-art deep learning methord for semantic part segmentation, instance-aware edge detection and instance-level human parsing.

This distribution provides a publicly available implementation for the key model ingredients reported in [Instance-level Human Parsing (ECCV 2018 paper)](http://openaccess.thecvf.com/content_ECCV_2018/papers/Ke_Gong_Instance-level_Human_Parsing_ECCV_2018_paper.pdf).

### Pre-trained models

Authors have released trained models of PGN on CIHP dataset at [google drive](https://drive.google.com/open?id=1Mqpse5Gen4V4403wFEpv3w3JAsWw2uhk).
Copy on our servers: [OneDrive](https://cohevo9-my.sharepoint.com/:u:/g/personal/m68714_vip365s_com/EazRtwf3IvlPiDaIEB5LMi8BW0LYXGbvZxQFIzW0gtlKkw?e=owYnzN).

### Prepare
```bash
git clone https://github.com/apoezzhaev/CIHP_PGN.git
cd CIHP_PGN

# Load model checkpoint
mkdir checkpoint && cd checkpoint
wget -O CIHP_PGN.zip https://cohevo9-my.sharepoint.com/:u:/g/personal/m68714_vip365s_com/EazRtwf3IvlPiDaIEB5LMi8BW0LYXGbvZxQFIzW0gtlKkw?donwload=1
unzip CIHP_PGN.zip
rm CIHP_PGN.zip
cd ..

# Build docker image
docker image build -t fitting_room/segmentation:latest .
docker run --runtime=nvidia -it --name cihp_testing -v .:/code fitting_room/segmentation:test /bin/bash
```

### Inference
```
python batch_inference.py --data_dir /data/images/ --output /data/segmentations/ --checkpoint ./checkpoint/CIHP_pgn
```
Masked source images will as well as resized masks will be written to `{OUTPUT_DIR}/overlay` 


