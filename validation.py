import torch
from common import read_embedding
from fire import Fire

def cos_similarity(user_ids,
                    node_emb,
                    user_id):
    
    full_emb = torch.from_numpy(node_emb)
    user_idx = list(filter(lambda x: x[1]==str(user_id), [(idx, k) for idx, k in enumerate(user_ids)]))#[0][0]
    if len(user_idx)==0:
        print('seed user not found')
        return 
    
    user_idx = user_idx[0][0]
    
    full_emb=torch.nn.functional.normalize(full_emb, p=2, dim=1)
    full_emb=torch.transpose(full_emb, 0, 1)

    cos_scores = torch.matmul(full_emb[:, user_idx],  #torch.from_numpy(node_emb[str(user_id)]),
                                full_emb)
    
    idx = (cos_scores>0).nonzero()
    non_seed_idx = idx.flatten()[(idx.flatten() != user_idx)]
    idx_cos = {user_ids[ni.item()]:cos_scores[ni].item() for ni in non_seed_idx}
    sorted_idx_cos = sorted(idx_cos.items(), key=lambda x: x[1], reverse=True)
    
    return list(filter(lambda x: x[1] > 0.5, sorted_idx_cos)) # take every above 0.5


def find_similar_nodes(emb_json,
                       emb_5,
                       node_id):
    # emb_json = '/Users/grace/workspace/biggraph/entity/entity_names_disease_0.json'
    # emb_5 = '/Users/grace/workspace/biggraph/models/embeddings_disease_0.v30.h5'
    ids, embs = read_embedding(emb_json, emb_5)
    
    sim_diease = cos_similarity(ids, embs, node_id)
    print(f'For node {node_id} >>> \n similar nodes are : {sim_diease}')


if __name__ == '__main__': 
    Fire({'find':find_similar_nodes})
    