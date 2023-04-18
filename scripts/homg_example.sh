#!/bin/bash

export tmux_session=0

tmux send-keys -t ${tmux_session} "python 01_preprocess_homog.py homogeneous --db_path=./db/disgenet_2020.db --out_path=./homg/ &wait" C-m
tmux send-keys -t ${tmux_session} "python train_n_eval.py homogeneous /Users/grace/workspace/biggraph/homg/ /Users/grace/workspace/biggraph/configs/homog_config.py &wait" C-m
tmux send-keys -t ${tmux_session} "python validation.py find --emb_json=/Users/grace/workspace/biggraph/entity/entity_names_disease_0.json --emb_5=/Users/grace/workspace/biggraph/models/embeddings_disease_0.v30.h5 --node_id=7897 &wait" C-m

