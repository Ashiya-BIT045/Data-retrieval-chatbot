import pandas as pd
from app.db_postgres import SessionLocal, Job, init_db, engine
from app.db_elastic import ElasticSearchClient
from app.config import ELASTIC_INDEX
import os
import requests
import time
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def wait_for_services(max_retries=10, delay=5):
    """Wait for PostgreSQL and Elasticsearch to be ready."""
    print("Waiting for databases to be ready...")
    
    # Wait for Postgres
    for i in range(max_retries):
        try:
            engine.connect()
            print("PostgreSQL is ready!")
            break
        except Exception:
            print(f"PostgreSQL not ready, retrying in {delay}s... ({i+1}/{max_retries})")
            time.sleep(delay)
    
    # Wait for Elastic
    for i in range(max_retries):
        es_client = ElasticSearchClient()
        if not es_client.use_fallback:
            print("Elasticsearch is ready!")
            return es_client
        else:
            print(f"Elasticsearch not ready, retrying in {delay}s... ({i+1}/{max_retries})")
            time.sleep(delay)
    
    return ElasticSearchClient()

def load_data():
    # 1. Wait for services
    es_client = wait_for_services()

    # 2. Initialize PostgreSQL and load data
    print("Initializing PostgreSQL...")
    init_db()
    db = SessionLocal()
    
    # Clear existing data for idempotency
    try:
        db.query(Job).delete()
        db.commit()
    except Exception as e:
        logger.error(f"Error clearing PSQL data: {e}")
    
    psql_df = pd.read_excel("data/psql_file.xlsx")
    records = psql_df.to_dict(orient="records")
    db.bulk_insert_mappings(Job, records)
    db.commit()
    db.close()
    print(f"Loaded {len(records)} records into PostgreSQL")

    # 3. Initialize Elasticsearch and load data
    print("Initializing Elasticsearch...")
    if not es_client.use_fallback:
        # Delete and recreate index for idempotency
        requests.delete(f"{es_client.url}/{ELASTIC_INDEX}")
        es_client.create_index()

    elastic_df = pd.read_excel("data/elastic_search_data.xlsx")
    records = elastic_df.to_dict(orient="records")
    es_client.bulk_index_data(records)
    print(f"Loaded {len(records)} records into Elasticsearch")


if __name__ == "__main__":
    load_data()

