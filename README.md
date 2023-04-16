## PyTorch BigGraph Practice

This repository contains practice code for working with PyTorch BigGraph (PBG), a tool for training and serving large-scale graph embeddings.

### Getting Started
Install required packages then
```
pip install -r requirements.txt
```

To use this code, you will need to have PyTorch BigGraph installed on your system. You can follow the installation instructions provided in the PBG documentation: <https://github.com/facebookresearch/PyTorch-BigGraph#installation>
```
git clone https://github.com/facebookresearch/PyTorch-BigGraph.git
cd PyTorch-BigGraph/
pip install .
```

### Dataset

- [DisGeNET Disease-Gene](https://www.disgenet.org/home/ : download sqlite.db.gz file and decompress under /db folder > ./db/disgenet_2020.db.


### TO RUN
```
# homogeneous weighted graph
## generate edge files for biggraph
mkdir ./homg/
python 01_preprocess.py homogeneous --db_path=./db/disgenet_2020.db --out_path=./homg/

## train biggraph
mkdir ./entity
mkdir ./models

python train_n_eval.py

## validate with specific diseaseNID

python validation.py find --emb_json={path_to_entity_names.json_file} --emb_5={path_to_embeddings_h5_file} --node_id={seed_node_id}

```