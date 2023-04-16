# preprocess DisGeNET(Disease-Gene) dataset into biggraph edge format
import pandas as pd
import sqlite3
from fire import Fire
import random, os

# homogeneous weighted disease graph
def prep_homg_graph(db_path:str, out_path:str)-> None:
    # Connect to the SQLite database
    conn = sqlite3.connect('./db/disgenet_2020.db')
    
    df_gd = pd.read_sql_query("SELECT * FROM geneDiseaseNetwork", conn)
    df_target = df_gd.loc[~pd.isna(df_gd.EL)][['diseaseNID', 'geneNID', 'NID']]
    print(f'target datarows : {df_target.shape[0]}')
    df_unique = df_target.drop_duplicates(subset=['diseaseNID', 'geneNID'], inplace=False)
    print(f'target datarows : {df_unique.shape[0]}')

    train_path = f'{out_path}/train'
    test_path = f'{out_path}/test'
    if not os.path.exists(train_path):
        os.makedirs(train_path)
    if not os.path.exists(test_path):
        os.makedirs(test_path)
    train_cnt, test_cnt = 0, 0

    for gr, rows in df_target.groupby(['geneNID']):
        nodes = rows['diseaseNID'].values
        
        for i in range(len(nodes)-1):
            for j in range(1, len(nodes)):
                if nodes[i]!=nodes[j]:
                    rand_float = random.random()
                
                    if rand_float <= 0.2:
                        target_set = test_path
                        test_cnt += 1
                    else:
                        target_set = train_path
                        train_cnt += 1

                    with open(f'{target_set}/retweet_edges', 'a') as write_file:
                        write_file.write(','.join([str(nodes[i]), str(nodes[j])])+'\n')
                                        
    print(f'train :: {train_cnt}, test :: {test_cnt}')

    conn.close()


if __name__ == '__main__':
    Fire({
        'homogeneous': prep_homg_graph
    })