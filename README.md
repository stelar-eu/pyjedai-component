# pyjedai-component
Dockerized pyJedAI for integration into the KLMS.

To build the docker image:
```
docker build --no-cache -t stelar_pyjedai .
```

and to execute
```
docker run -v <local-path-with-logs>:/app/logs/ -v <local-path-with-data>:/app/data/ stelar_pyjedai:latest input.json output.json
```
