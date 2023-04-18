## PyTorch BigGraph Practice

This repository contains practice code for working with PyTorch BigGraph (PBG), a tool for training and serving large-scale graph embeddings.

### Getting Started
Install required packages then
```
pip install -r requirements.txt
```

To use this code, you will need to have PyTorch BigGraph installed on your system. You can follow the installation instructions provided in the PBG documentation: <https://github.com/facebookresearch/PyTorch-BigGraph#installation>
```
git clone https://github.com/facebookresearch/PyTorch-BigGraph.git
cd PyTorch-BigGraph/
pip install .
```

### Dataset

- [DisGeNET Disease-Gene](https://www.disgenet.org/home/ : download sqlite.db.gz file and decompress under /db folder > ./db/disgenet_2020.db.


### TO RUN
```
# preprocess dataset
## generate edge files for biggraph

## homogeneous weighted graph
mkdir ./homg/
python 01_preprocess.py homogeneous --db_path=./db/disgenet_2020.db --out_path=./homg/

## heterogeneous weighted graph
mkdir ./heteg/
python 02_preprocess_heteg.py ./db/disgenet_2020.db ./heteg/

# train biggraph
mkdir ./entity
mkdir ./models

## homogeneous
python train_n_eval.py homogeneous ./homg/ ./configs/homog_config.py

## heterogeneous
python train_n_eval.py heterogeneous ./heteg/ ./configs/heterg_config.py


# validate with specific diseaseNID
python validation.py find --emb_json={path_to_entity_names.json_file} --emb_5={path_to_embeddings_h5_file} --node_id={seed_node_id}

python validation.py find --emb_json=./entity/entity_names_disease_0.json --emb_5=./models/embeddings_disease_0.v30.h5 --node_id=7897

```

### Trials

- with homogeneous graph, similar disease based on graph embeddings to (diseaseName: Frontotemporal dementia diseaseNID: 7898) are (above threshold 0.5):
[(diseaseNID, similarity_score, diseaseName, definition from internet)
('135', 0.9221433997154236, 'Amyotrophic Lateral Sclerosis', 'a progressive nervous system disease that affects nerve cells in the brain and spinal cord, causing loss of muscle control[1]'),
('18872', 0.8477824330329895, 'AMYOTROPHIC LATERAL SCLEROSIS 1'),
('18229', 0.7463338375091553, 'POLYCYSTIC LIPOMEMBRANOUS OSTEODYSPLASIA WITH SCLEROSING LEUKOENCEPHALOPATHY', 'Polycystic lipomembranous osteodysplasia with sclerosing leukoencephalopathy (PLOSL) is characterized by fractures (resulting from radiologically demonstrable polycystic osseous lesions), frontal lobe syndrome, and progressive presenile dementia beginning in the fourth decade.[2]'),
('29816', 0.623500406742096, 'POLYCYSTIC LIPOMEMBRANOUS OSTEODYSPLASIA WITH SCLEROSING LEUKOENCEPHALOPATHY 1'),
('10142', 0.6186094284057617, 'Dementia'),
('27499', 0.6068183183670044, 'FRONTOTEMPORAL DEMENTIA AND/OR AMYOTROPHIC LATERAL SCLEROSIS 4'),
('11577', 0.5620030760765076, 'Frontotemporal Lobar Degeneration')]


- with heterogeneous graph, similar disease based on graph embeddings to (diseaseName: Frontotemporal dementia diseaseNID: 7898) are (above threshold 0.5):
[('135', 0.6195142269134521, 'Amyotrophic Lateral Sclerosis'), 
('18229', 0.5204249620437622, 'POLYCYSTIC LIPOMEMBRANOUS OSTEODYSPLASIA WITH SCLEROSING LEUKOENCEPHALOPATHY')]


[1] <https://www.mayoclinic.org/diseases-conditions/amyotrophic-lateral-sclerosis/symptoms-causes/syc-20354022#:~:text=Amyotrophic%20lateral%20sclerosis%20(a%2Dmy>,who%20was%20diagnosed%20with%20it.
[2]