#!/usr/bin/env python
# coding: utf-8
import pandas as pd
from sqlalchemy import create_engine
from time import time
import argparse
import os
import requests
import math

def download_file(url, output_file):
    response = requests.get(url)
    with open(output_file, 'wb') as file:
        file.write(response.content)
    print(f"File downloaded as {output_file}")

def main(params):
    user = params.user
    password = params.password
    host = params.host
    port = params.port
    db = params.db
    table_name = params.table_name
    url = params.url
    file_name = 'output.parquet'
    csv_name = 'outpout.csv'

    # create engine to connect to postgres
    engine = create_engine(f'postgresql+psycopg2://{user}:{password}@{host}:{port}/{db}')

    # download data
    file_name = "output.parquet"
    download_file(url, file_name)
    print('Data downloaded.')

    df = pd.read_parquet(file_name, engine='pyarrow')
    df.to_csv(csv_name)
    print(f'Dataframe has {df.shape[0]} rows ')

    # chunk dataframe
    chunk_size = 100*1e3
    df_iter = pd.read_csv(csv_name, iterator=True, chunksize=chunk_size)
    chunk_count = math.ceil(df.shape[0] / chunk_size)
    print(f'Total chunks: {chunk_count}')

    # create table (only header)
    df = next(df_iter)
    df = df.drop('Unnamed: 0', axis=1)
    df.head(n=0).to_sql(name=table_name, con=engine, if_exists='replace')
    df.to_sql(name=table_name, con=engine, if_exists='replace', index=False)
    
    for _ in range(chunk_count):
        t_start = time()
        
        try:
            df = next(df_iter)
        except StopIteration:
            print("No more data to read, ending ingestion.")
            break

        if 'Unnamed: 0' in df.columns:
            df = df.drop('Unnamed: 0', axis=1)
            
        df.to_sql(name=table_name, con=engine, if_exists='append', index=False)
        t_end = time()
        print(f"Inserted another chunk! Took {t_end - t_start} second(s).")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
                        prog='ingest_data_to_postgres',
                        description='Ingest pandas dataframe to postgres'
                        )
    parser.add_argument('--user')
    parser.add_argument('--password')
    parser.add_argument('--host')
    parser.add_argument('--port')
    parser.add_argument('--db')
    parser.add_argument('--table_name')
    parser.add_argument('--url')

    args = parser.parse_args()

    main(args)
