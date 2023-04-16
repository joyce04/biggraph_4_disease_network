#!/bin/bash

python 01_preprocess_homog.py homogeneous --db_path=./db/disgenet_2020.db --out_path=./homg/

python validation.py find --emb_json=/Users/grace/workspace/biggraph/entity/entity_names_disease_0.json --emb_5=/Users/grace/workspace/biggraph/models/embeddings_disease_0.v30.h5 --node_id=7897
