import pandas as pd
# import pytokenjoin as ptj
from minio import Minio
import json
import uuid
import sys

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


def prep_df(input_file, separator, engine, minio):
    """
    Prepare DataFrame from input file.
    """
    if input_file.startswith('s3://'):
        bucket, key = input_file.replace('s3://', '').split('/', 1)
        client = Minio(minio['endpoint_url'], access_key=minio['id'], secret_key=minio['key'])
        df = pd.read_csv(client.get_object(bucket, key), header=None)
    else:
        df = pd.read_csv(input_file, sep=separator, engine=engine, na_filter=False)
    return df

def run(j):
    try:
        inputs = j['input']
        params = j['parameters']
        minio = j['minio']
        
        output_file = params['output_file']
        
        d1 = prep_df(inputs[0], params['separator'], params['engine'], j['minio']).astype(str)
        
        if len(inputs) == 2:
            gt = prep_df(inputs[1], params['separator'], params['engine'], j['minio'])
        elif len(inputs) == 3:
            d2 = prep_df(inputs[1], params['separator'], params['engine'], j['minio']).astype(str)
            gt = prep_df(inputs[2], params['separator'], params['engine'], j['minio'])
        else:
            raise ValueError("input is wrongly formatted.")
        
        data = Data(dataset_1=d1,
                    id_column_name_1=params['id_column_name_1'],
                    dataset_2=d2,
                    id_column_name_2=params['id_column_name_2'],
                    ground_truth = gt)

        data.print_specs()

        emb = EmbeddingsNNBlockBuilding(vectorizer=params['vectorizer'],
                                        similarity_search=params['similarity_search'])
        blocks, g = emb.build_blocks(data,
                        top_k=params['top_k'],
                        similarity_distance='euclidean',
                        load_embeddings_if_exist=False,
                        save_embeddings=False,
                        with_entity_matching=True)
        ccc = UniqueMappingClustering()
        clusters = ccc.process(g, data, similarity_threshold=params['similarity_threshold'])
        nn_pairs_df = ccc.export_to_df(clusters)
        results = ccc.evaluate(clusters, with_classification_report=True)
        nn_pairs_df.to_csv(output_file)

        perfomance_dict = {"f1": results['F1 %'],
                           "precision": results['Precision %'],
                           "recall" : results['Recall %']}

        # ----- MINIO ----- #
        # basename = output_file.split('/')[-1]
        basename = str(uuid.uuid4()) + "." + output_file.split('.')[-1]
        client = Minio(minio['endpoint_url'], access_key=minio['id'], secret_key=minio['key'])
        result = client.fput_object(minio['bucket'], basename, output_file)
        object_path = f"s3://{result.bucket_name}/{result.object_name}"

        return {'message': 'pyJedAI project executed successfully!',
                'output': [{'name': 'List of predicted duplicates', 'path': object_path}], 
                'metrics': perfomance_dict, 
                'status': 200}
                
    except Exception as e:
        return {
            'message': 'An error occurred during data processing.',
            'error': str(e),
            'status': 500
        }
    
if __name__ == '__main__':
    if len(sys.argv) != 3:
        raise ValueError("Please provide 2 files.")
    with open('./logs/'+sys.argv[1]) as o:
        j = json.load(o)
    response = run(j)
    with open('./logs/'+sys.argv[2], 'w') as o:
        o.write(json.dumps(response, indent=4))