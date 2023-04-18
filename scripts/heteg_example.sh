#!/bin/bash

export tmux_session=0

tmux send-keys -t ${tmux_session} "python 02_preprocess_heteg.py ./db/disgenet_2020.db ./heteg/ &wait" C-m
tmux send-keys -t ${tmux_session} "python train_n_eval.py heterogeneous /Users/grace/workspace/biggraph/heteg/ /Users/grace/workspace/biggraph/configs/heterg_config.py &wait" C-m
tmux send-keys -t ${tmux_session} "python validation.py find --emb_json=/Users/grace/workspace/biggraph/entity/entity_names_disease_0.json --emb_5=/Users/grace/workspace/biggraph/models/embeddings_disease_0.v30.h5 --node_id=7897 &wait" C-m