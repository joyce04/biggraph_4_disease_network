import h5py, json, os
import numpy as np
import sqlite3
import pandas as pd


def read_embedding(emb_json, 
                    emb_5):
    with open(emb_json, 'r') as f:
        node_names = list(map(lambda x: x.replace('\n', '').strip(), json.load(f)))

    with h5py.File(emb_5, 'r') as g:
        embeddings = g['embeddings'][:]
        print(type(embeddings))

    return np.array(node_names), embeddings


def get_disease_2_genes(db_path:str) -> pd.DataFrame:
    # Connect to the SQLite database
    conn = sqlite3.connect(db_path)
    
    df_gd = pd.read_sql_query("SELECT * FROM geneDiseaseNetwork", conn)
    df_target = df_gd.loc[~pd.isna(df_gd.EL)][['diseaseNID', 'geneNID', 'NID']]
    print(f'target datarows : {df_target.shape[0]}')
    df_unique = df_target.drop_duplicates(subset=['diseaseNID', 'geneNID'], inplace=False)
    print(f'target datarows : {df_unique.shape[0]}')
    
    conn.close()
    return df_target


def initialize_folders(out_path:str) -> None:
    train_path = f'{out_path}/train'
    test_path = f'{out_path}/test'
    if not os.path.exists(train_path):
        os.makedirs(train_path)
    if not os.path.exists(test_path):
        os.makedirs(test_path)
    return train_path+'/edges', test_path+'/edges'

