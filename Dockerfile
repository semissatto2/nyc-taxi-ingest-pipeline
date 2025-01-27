FROM python:3.9

RUN pip install --default-timeout=180 pandas==1.5.3 numpy==1.23.5 sqlalchemy requests psycopg2 pyarrow


WORKDIR /app
COPY ./scripts/ingest.py ingest.py

ENTRYPOINT [ "python", "ingest.py"]
