# preprocess DisGeNET(Disease-Gene) dataset into biggraph edge format
import random, os, sys
from datetime import datetime
import pandas as pd

from multiprocessing import Process, Manager, Queue
from joblib import Parallel, delayed

from common import get_disease_2_genes, initialize_folders


def get_data(df_data:pd.DataFrame)-> tuple:
    for idx, row in df_data[['geneNID', 'diseaseNID']].iterrows():
        yield (row[0], row[1])


def prep_edges(dis_gene_pair:tuple):
    rand_float = random.random()

    if rand_float <= 0.2:
        test_queue.put(dis_gene_pair)
        ns.test_cnt += 1
    else:
        train_queue.put(dis_gene_pair)
        ns.train_cnt += 1


def save_edge_file(q, out_path, n):
    with open(out_path, 'a') as out:
        while True:            
            val = q.get()
            if val is None: 
                break
            
            out.write(','.join([str(val[0]), 'gene_2_dis', str(val[1])])+'\n')


def initialize_edge_file(target_path):
    with open(target_path, 'w') as out:
        pass


# heterogeneous weighted disease graph
# multi-processing version
# joblib conflicts with python-fire 
if __name__ == '__main__':
    db_path = sys.argv[1]
    out_path = sys.argv[2]

    start_time = datetime.now()

    df_target = get_disease_2_genes(db_path) 

    train_path, test_path = initialize_folders(out_path)
    initialize_edge_file(train_path)
    initialize_edge_file(test_path)
    
    train_queue, test_queue = Queue(), Queue()
    manager = Manager()
    ns = manager.Namespace()
    ns.train_cnt = 0
    ns.test_cnt = 0
    
    train_save_process = Process(target=save_edge_file, args=(train_queue, train_path, ns))
    test_save_process = Process(target=save_edge_file, args=(test_queue, test_path, ns))
    
    train_save_process.start()
    test_save_process.start()
        
    Parallel(n_jobs=-1, backend='threading')(delayed(prep_edges)(r) for r in get_data(df_target))
    
    train_queue.put(None) # to flag the end of the queue
    test_queue.put(None) 
    
    train_save_process.join()
    test_save_process.join()

    print('TOTAL TRAIN ROWS PROCSSED', ns.train_cnt, sep='\t')
    print('TOTAL TEST ROWS PROCSSED', ns.test_cnt, sep='\t')
    print('TOTAL TIME TAKEN', datetime.now() - start_time, sep='\t')