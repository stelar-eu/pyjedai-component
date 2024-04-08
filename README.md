# pyJedAI as a component
Dockerized pyJedAI for integration into the KLMS. 

# Code 

Find all source code [here](https://github.com/AI-team-UoA/pyJedAI/tree/main/src/pyjedai).

# Documentation

Find all documentation [here](https://pyjedai.readthedocs.io/).

# Overview​

pyJedAI is a python framework, aiming to offer experts and novice users, robust and fast solutions for multiple types of Entity Resolution problems. It is builded using state-of-the-art python frameworks. pyJedAI constitutes the sole open-source Link Discovery tool that is capable of exploiting the latest breakthroughs in Deep Learning and NLP techniques, which are publicly available through the Python data science ecosystem. This applies to both blocking and matching, thus ensuring high time efficiency, high scalability as well as high effectiveness, without requiring any labelled instances from the user.

# Input format​ [NOT FINAL]

```json
{
    "input": [
        "s3://agroknow-bucket/incidents.csv"
    ],
    "parameters": {
        "separator": ",",
        "id_column_name_1" : "Unnamed: 0",
        "vectorizer": "st5",
        "similarity_search": "faiss",
        "top_k": 1,
        "similarity_threshold": 0.9
    },
    "minio": {
        "endpoint_url": "XXXXXXXXX",
        "id": "XXXXXXXXX",
        "key": "XXXXXXXXX",
        "bucket": "XXXXXXXXX"
    }
}
```


# Output JSON format [NOT FINAL]

```json
{
        "message": "pyJedAI project executed successfully!",
    "output": [
        {
            "name": "List of predicted duplicates",
            "path": null
        }
    ],
    "metrics": {
        "f1": 6.294964028776979,
        "precision": 97.22222222222221,
        "recall": 3.2527881040892193
    },
    "status": 200
}
```


# Parameters​

- "separator": File separator,
- "id_column_name_1" : Coilumn containing ids,
- "vectorizer": Language model,
- "similarity_search": Similarity search framework,
- "top_k": Number of NNs,
- "similarity_threshold": Threshold for determing duplicates

# Metrics​

- "f1": F1 score
- "precision": Precision
- "recall": Recall

# Installation & Usage instructions​

## General

### PyPI
Install the latest version of pyjedai __[requires python >= 3.8]__:
```
pip install pyjedai
```
More on [PyPI](https://pypi.org/project/pyjedai).

### Git

Set up locally:
```
git clone https://github.com/AI-team-UoA/pyJedAI.git
```
go to the root directory with `cd pyJedAI` and type:
```
pip install .
```

### Docker

Available at [Docker Hub](https://hub.docker.com/r/aiteamuoa/pyjedai), or clone this repo and:
```
docker build -f Dockerfile
```

## STELAR KLMS Docker

To build the docker image:
```
docker build --no-cache -t stelar_pyjedai .
```

and to execute
```
docker run -v <local-path-with-logs>:/app/logs/ -v <local-path-with-data>:/app/data/ stelar_pyjedai:latest input.json output.json
```

# License & Acknowledgments​

Released under the Apache-2.0 license (see [LICENSE.txt](https://github.com/AI-team-UoA/pyJedAI/blob/main/LICENSE)).




