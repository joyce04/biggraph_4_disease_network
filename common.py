import h5py
import json 
import numpy as np


def read_embedding(emb_json, 
                    emb_5):
    with open(emb_json, 'r') as f:
        node_names = list(map(lambda x: x.replace('\n', '').strip(), json.load(f)))

    with h5py.File(emb_5, 'r') as g:
        embeddings = g['embeddings'][:]
        print(type(embeddings))

    return np.array(node_names), embeddings