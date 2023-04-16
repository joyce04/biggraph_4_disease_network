from torchbiggraph.config import ConfigFileLoader, add_to_sys_path
from torchbiggraph.converters.importers import TSVEdgelistReader, convert_input_data
from torchbiggraph.train import train
from torchbiggraph.eval import do_eval
from torchbiggraph.util import SubprocessInitializer
from torchbiggraph.util import set_logging_verbosity, setup_logging
from torchbiggraph.config import parse_config

import attr
from pathlib import Path
import pkg_resources
import tensorflow as tf
import os


def graph_train(data_folder:str,
                config_py:str):
    files = [f'{data_folder}/train/retweet_edges', f'{data_folder}/test/retweet_edges']

    loader = ConfigFileLoader()
    config = loader.load_config(config_py, None)
    # config = parse_config(get_torchbiggraph_config())

    subprocess_init = SubprocessInitializer()
    subprocess_init.register(setup_logging, config.verbose)

    output_train_path, output_test_path = config.edge_paths
    data_dir = Path('./')
    data_dir.mkdir(parents=True, exist_ok=True)
    input_edge_paths = [data_dir / name for name in files]

    convert_input_data(
            config.entities,
            config.relations,
            config.entity_path,
            config.edge_paths,
            input_edge_paths,
            TSVEdgelistReader(lhs_col=0, rel_col=None, rhs_col=1, delimiter=','),
            dynamic_relations=config.dynamic_relations,
        )

    train_config = attr.evolve(config, edge_paths=[output_train_path])
    train(train_config)

    eval_config = attr.evolve(train_config, edge_paths=[output_test_path])
    eval = do_eval(eval_config)
    print(eval)


## due to dataset size > need to run with tmux
if __name__ == '__main__':
    graph_train(data_folder='/Users/grace/workspace/biggraph/homg/', 
                config_py='/Users/grace/workspace/biggraph/configs/homog_config.py')


'''
[2023-04-11 22:53:01.896790] Using the 1 relation types given in the config            
[2023-04-11 22:53:01.896858] Searching for the entities in the edge files...           
[2023-04-11 22:54:02.179949] Entity type disease:                                      
[2023-04-11 22:54:02.179996] - Found 5750 entities                                     
[2023-04-11 22:54:02.180005] - Removing the ones with fewer than 1 occurrences...      
[2023-04-11 22:54:02.181210] - Left with 5750 entities
[2023-04-11 22:54:02.181238] - Shuffling them...[2023-04-11 22:54:02.184931] Preparing counts and dictionaries for entities and relation types:
[2023-04-11 22:54:02.185099] - Writing count of entity type disease and partition 0[2023-04-11 22:54:02.188014] Preparing edge path /Users/grace/workspace/biggraph/homg/train, out of the edges found in /Users/grace/workspace/biggraph/homg/train/retweet_edges
[2023-04-11 22:54:02.188081] - Edges will be partitioned in 1 x 1 buckets.
[2023-04-11 22:54:02.649806] - Processed 100000 edges so far...
'''
