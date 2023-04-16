'''
linux only 
pip install scann
'''
import scann
import os
import tensorflow as tf
from fire import Fire
import numpy as np
from common import read_embedding


def serialize_scann(embeddings,
        searcher_folder):
    
    print(f'SAVING SEARCHER INDEX FILES to {searcher_folder}')
    
    os.makedirs(searcher_folder, exist_ok=True)
      
    searcher = scann.scann_ops_pybind.builder(embeddings, 10, "dot_product").tree(
        num_leaves=2500, num_leaves_to_search=150, training_sample_size=embeddings.shape[0]).score_ah(
    2, anisotropic_quantization_threshold=0.2).reorder(100).build()
    searcher.serialize(searcher_folder)
    
    tf.saved_model.save(searcher, searcher_folder)


def serialize(emb_json,
              emb_5,
              searcher_path):
    # read embedding files
    print('READING EMBEDDING FILEs')
    ids, embs = read_embedding(emb_json, emb_5)
    print(embs[:2, :])
    print('SERIALIZE SCANN')
    print(len(ids))
    serialize_scann(embs, searcher_path)


def scann_search(candidate_ids, s_searcher, query_emb):
    neighbors, distances = s_searcher.search(query_emb, final_num_neighbors=len(candidate_ids), 
                                        leaves_to_search=150, pre_reorder_num_neighbors=len(candidate_ids))
    similar_cand_indx = np.where(distances >= 15) #raw threshold
    return list(zip(candidate_ids[neighbors[similar_cand_indx]], distances[similar_cand_indx]))


if __name__ == '__main__':  
    Fire({
            'serialize_scann':serialize,
            'search':scann_search
        })