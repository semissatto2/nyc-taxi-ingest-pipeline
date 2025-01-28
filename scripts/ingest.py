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
    print(f'Downloading data from {url}')
    response = requests.get(url)
    with open(output_file, 'wb') as file:
        file.write(response.content)
    print(f'File downloaded as {output_file}')

def main(params):
    user = params.user
    password = params.password
    host = params.host
    port = params.port
    db = params.db
    table_name1 = params.table_name1
    url1 = params.url1
    table_name2 = params.table_name2
    url2 = params.url2

    # create engine to connect to postgres
    engine = create_engine(f'postgresql+psycopg2://{user}:{password}@{host}:{port}/{db}')

    # download first table - parquet data
    file_name = 'output.parquet'
    csv_name = 'outpout.csv'
    download_file(url1, file_name)
    df = pd.read_parquet(file_name, engine='pyarrow')
    df.to_csv(csv_name, index=False)
    print(f'Dataframe has {df.shape[0]} rows')

    # chunk dataframe
    chunk_size = 100*1e3
    df_iter = pd.read_csv(csv_name, iterator=True, chunksize=chunk_size)
    chunk_count = math.ceil(df.shape[0] / chunk_size)
    
    # create table (only header)
    df = next(df_iter)
    df.head(n=0).to_sql(name=table_name1, con=engine, if_exists='replace')
    df.to_sql(name=table_name1, con=engine, if_exists='replace', index=False)
    
    # insert table on postgres
    for _ in range(chunk_count):
        t_start = time()
        
        try:
            df = next(df_iter)
        except StopIteration:
            print('No more data to read, ending ingestion.')
            break

        df.to_sql(name=table_name1, con=engine, if_exists='append', index=False)
        t_end = time()
        print(f'Inserted another chunk! Took {t_end - t_start:.3f} second(s).')

    # download second table - csv data
    file_name = 'output2.csv'
    download_file(url2, file_name)
    df = pd.read_csv(file_name)
    print(f'Dataframe has {df.shape[0]} rows')

    # insert table on postgres
    t_start = time()
    df.to_sql(name=table_name2, con=engine, if_exists='replace', index=False)
    t_end = time()
    print(f'Inserted another table! Took {t_end - t_start:.3f} second(s).')

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
    parser.add_argument('--table_name1')
    parser.add_argument('--url1')
    parser.add_argument('--table_name2')
    parser.add_argument('--url2')

    args = parser.parse_args()

    main(args)
