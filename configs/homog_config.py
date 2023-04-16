def get_torchbiggraph_config():

    config = dict(  # noqa
        # I/O data
        entity_path="/Users/grace/workspace/biggraph/entity",
        edge_paths=["/Users/grace/workspace/biggraph/homg/train", 
                    "/Users/grace/workspace/biggraph/homg/test"],
        checkpoint_path="/Users/grace/workspace/biggraph/models",
        # Graph structure
        entities={"disease": {"num_partitions": 1}},
        relations=[
            {"name": "common_gene", 
            "lhs": "disease", 
            "rhs": "disease", 
            "operator": "none"}
        ],
        # Scoring model
        dynamic_relations=False,        
        dimension=512,
        global_emb=False,
        comparator="dot",
        # Training
        num_epochs=30,
        lr=0.1,
        num_uniform_negs=10,
        loss_fn="softmax",
        # eval
        eval_fraction=0,
        # Misc
        hogwild_delay=2,
    )

    return config