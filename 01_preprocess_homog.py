# preprocess DisGeNET(Disease-Gene) dataset into biggraph edge format
import random, os
from datetime import datetime
from fire import Fire
from common import get_disease_2_genes, initialize_folders


# homogeneous weighted disease graph
# simple plain version
def prep_homg_graph(db_path:str, out_path:str)-> None:
    start_time = datetime.now()
    df_target = get_disease_2_genes(db_path) 

    train_path, test_path = initialize_folders(out_path)
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

                    with open(f'{target_set}/edges', 'a') as write_file:
                        write_file.write(','.join([str(nodes[i]), str(nodes[j])])+'\n')
                                        
    print(f'train :: {train_cnt}, test :: {test_cnt}')
    print('TOTAL TIME TAKEN', datetime.now() - start_time, sep='\t')


if __name__ == '__main__':
    Fire({
        'homogeneous': prep_homg_graph
    })