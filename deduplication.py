import pandas as pd
import pyjedai
from pyjedai.datamodel import Data
from pyjedai.utils import (
    text_cleaning_method,
    print_clusters,
    print_blocks,
    print_candidate_pairs
)
from pyjedai.evaluation import Evaluation
from pyjedai.vector_based_blocking import EmbeddingsNNBlockBuilding
from pyjedai.clustering import ConnectedComponentsClustering, UniqueMappingClustering

from tqdm import tqdm

incidents = "./data/incidents.csv"
d1 = pd.read_csv(incidents, sep=',', na_filter=False)
num_of_entities = d1.shape[0]
data = Data(dataset_1=d1, id_column_name_1='Unnamed: 0')

data.print_specs()

d1_without_exact_dups = d1.drop_duplicates(subset = d1.columns.difference(['Unnamed: 0']))
print("Number of exact duplicates: ",  num_of_entities - d1_without_exact_dups.shape[0])

data_without_exact_dups = Data(dataset_1=d1_without_exact_dups, id_column_name_1='Unnamed: 0')
num_of_entities = d1_without_exact_dups.shape[0]
data_without_exact_dups.print_specs()

from pyjedai.vector_based_blocking import EmbeddingsNNBlockBuilding

emb = EmbeddingsNNBlockBuilding(vectorizer='st5',
                                similarity_search='faiss')

blocks, g = emb.build_blocks(data_without_exact_dups,
                             top_k=1,
                             similarity_distance='euclidean',
                             load_embeddings_if_exist=True,
                             save_embeddings=True,
                             with_entity_matching=True)

from pyjedai.clustering import ConnectedComponentsClustering, CenterClustering
ccc = CenterClustering()
clusters = ccc.process(g, data_without_exact_dups, similarity_threshold=0.9)

# print(clusters)
nn_pairs_df = ccc.export_to_df(clusters)

unique_incidents = []
print("Number of unique incidents: ", len(clusters))
print("Entities dropped: ", num_of_entities - len(clusters))
for cluster in clusters:
    lcluster = list(cluster)
    if len(lcluster) > 0:
        unique_incidents.append(d1.iloc[lcluster[0]])

unique_incidents = pd.DataFrame(unique_incidents , columns=d1.columns)
unique_incidents.drop(columns=['Unnamed: 0'], inplace=True)
unique_incidents = unique_incidents.reset_index(drop=True)
unique_incidents.to_csv("unique_incidents.csv", index=False)

unique_incidents = pd.read_csv("unique_incidents.csv")
print(unique_incidents.head())
