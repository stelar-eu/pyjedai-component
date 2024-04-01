import pandas as pd
from pyjedai.datamodel import Data
from pyjedai.vector_based_blocking import EmbeddingsNNBlockBuilding
from pyjedai.clustering import CenterClustering

from minio import Minio
import uuid
import traceback
import sys
import json


def prep_df(input_file, separator, minio):
    """
    Prepare DataFrame from input file.
    """
    if input_file.startswith('s3://'):
        bucket, key = input_file.replace('s3://', '').split('/', 1)
        client = Minio(minio['endpoint_url'], access_key=minio['id'], secret_key=minio['key'])
        df = pd.read_csv(client.get_object(bucket, key), sep=separator, na_filter=False)
    else:
        df = pd.read_csv(input_file, sep=separator, na_filter=False)
    return df

def run(j):
    try:
        # incidents = "./data/incidents.csv"
        # d1 = pd.read_csv(incidents, sep=',', na_filter=False)
        parameters = j['parameters']
        minio = j['minio']
        d1 = prep_df(j['input'][0], separator=parameters['separator'], minio=minio)
        print(d1.head(5))
        print(d1.shape)
        print(d1.columns)
        num_of_entities = d1.shape[0]
        data = Data(dataset_1=d1, id_column_name_1=parameters['id_column_name_1'])
        
        data.print_specs()
        
        d1_without_exact_dups = d1.drop_duplicates(subset = d1.columns.difference([parameters['id_column_name_1']]))
        print("Number of exact duplicates: ",  num_of_entities - d1_without_exact_dups.shape[0])
        
        data_without_exact_dups = Data(dataset_1=d1_without_exact_dups, id_column_name_1=parameters['id_column_name_1'])
        num_of_entities = d1_without_exact_dups.shape[0]
        data_without_exact_dups.print_specs()
        
        emb = EmbeddingsNNBlockBuilding(vectorizer=parameters['vectorizer'],
                                        similarity_search=parameters['similarity_search'])
        
        blocks, g = emb.build_blocks(data_without_exact_dups,
                                     top_k=parameters['top_k'],
                                     similarity_distance='euclidean',
                                     load_embeddings_if_exist=True,
                                     save_embeddings=True,
                                     with_entity_matching=True)
        
        
        ccc = CenterClustering()
        clusters = ccc.process(g, data_without_exact_dups, similarity_threshold=parameters['similarity_threshold'])
        
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
        #unique_incidents.drop(columns=['Unnamed: 0'], inplace=True)
        #unique_incidents = unique_incidents.reset_index(drop=True)
        output_file = 'unique_incidents.csv'
        unique_incidents.to_csv(output_file, index=False)
        
        print(unique_incidents.head(5))
        
        perfomance_dict = {"no_duplicates": num_of_entities - len(clusters),
                           "f_duplicates": (num_of_entities - len(clusters)) / num_of_entities}
        print(perfomance_dict)

        # ----- MINIO ----- #
        # basename = output_file.split('/')[-1]
        basename = str(uuid.uuid4()) + "." + output_file.split('.')[-1]
        client = Minio(minio['endpoint_url'], access_key=minio['id'], secret_key=minio['key'])
        result = client.fput_object(minio['bucket'], basename, output_file)
        object_path = f"s3://{result.bucket_name}/{result.object_name}"

        return {'message': 'pyJedAI project executed successfully!',
                'output': [{'name': 'Deduplicated dataframe', 'path': object_path}], 
                'metrics': perfomance_dict, 
                'status': 200}
        
    except Exception:
        return {
            'message': 'An error occurred during data processing.',
            'error': traceback.format_exc(),
            'status': 500
        }
    
if __name__ == '__main__':
    print("test")
    if len(sys.argv) != 3:
        raise ValueError("Please provide 2 files.")
    with open(sys.argv[1]) as o:
        j = json.load(o)
    response = run(j)
    with open(sys.argv[2], 'w') as o:
        o.write(json.dumps(response, indent=4))     
