# pyJedAI as a component
Dockerized pyJedAI for integration into the KLMS. 

To build the docker image:
```
docker build --no-cache -t stelar_pyjedai .
```

and to execute
```
docker run -v <local-path-with-logs>:/app/logs/ -v <local-path-with-data>:/app/data/ stelar_pyjedai:latest input.json output.json
```

# Input JSON format [NOT FINAL]

```json
{
    "input": [
        "/app/data/abt.csv",
        "/app/data/buy.csv",
        "/app/data/gt.csv"
    ],
    "parameters": {
        "separator": "|",
        "engine" : "python",
        "output_file": "prediction.csv",
        "id_column_name_1" : "id",
        "id_column_name_2" : "id",
        "vectorizer": "st5",
        "similarity_search": "faiss",
        "top_k": 5,
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


