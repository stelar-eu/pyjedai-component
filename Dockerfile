FROM aiteamuoa/pyjedai:0.1.5
WORKDIR /app
COPY . /app/
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
ENTRYPOINT ["python3", "main.py"]


# docker run -d -p 9059:9000 -p 9060:9001 
#     -v .:/data 
#         -e MINIO_ROOT_USER=minio_admin 
#         -e MINIO_ROOT_PASSWORD=minio_admin 
#         -e MINIO_SERVER_URL="https://minio.stelar.di.uoa.gr" 
#         -e MINIO_BROWSER_REDIRECT_URL="https://minio-console.stelar.di.uoa.gr" 
#         --name minio minio/minio server /data 
#         --console-address ":9001"