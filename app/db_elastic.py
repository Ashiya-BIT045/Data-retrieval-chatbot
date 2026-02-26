import requests
import json
from .config import ELASTICSEARCH_URL, ELASTIC_INDEX
import logging

logger = logging.getLogger(__name__)

class ElasticSearchClient:
    def __init__(self):
        self.url = ELASTICSEARCH_URL.rstrip('/')
        try:
            response = requests.get(self.url, timeout=5)
            if response.status_code == 200:
                self.use_fallback = False
                logger.info("Connected to Elasticsearch successfully via requests.")
            else:
                raise Exception(f"Status code {response.status_code}")
        except Exception as e:
            logger.warning(f"Elasticsearch unreachable ({e}). Using Local JSON Fallback.")
            self.use_fallback = True
            self.local_json_path = "local_elastic_data.json"
            self._load_local_repo()

    def _load_local_repo(self):
        import os
        if os.path.exists(self.local_json_path):
            with open(self.local_json_path, "r") as f:
                self.local_repo = json.load(f)
        else:
            self.local_repo = []

    def _save_local_repo(self):
        with open(self.local_json_path, "w") as f:
            json.dump(self.local_repo, f)

    def create_index(self):
        if not self.use_fallback:
            resp = requests.get(f"{self.url}/{ELASTIC_INDEX}", timeout=5)
            if resp.status_code == 404:
                requests.put(f"{self.url}/{ELASTIC_INDEX}", timeout=5)
                logger.info(f"Created Elasticsearch index: {ELASTIC_INDEX}")

    def index_data(self, data: list):
        if not self.use_fallback:
            for item in data:
                requests.post(f"{self.url}/{ELASTIC_INDEX}/_doc", json=item, timeout=5)
            logger.info(f"Indexed {len(data)} documents into Elasticsearch")
        else:
            self.local_repo = data
            self._save_local_repo()
            logger.info(f"Saved {len(data)} documents into Local JSON Fallback")

    def bulk_index_data(self, data: list):
        if not self.use_fallback:
            chunk_size = 1000
            for i in range(0, len(data), chunk_size):
                chunk = data[i:i + chunk_size]
                bulk_data = ""
                for item in chunk:
                    bulk_data += json.dumps({"index": {"_index": ELASTIC_INDEX}}) + "\n"
                    bulk_data += json.dumps(item) + "\n"
                
                headers = {"Content-Type": "application/x-ndjson"}
                resp = requests.post(f"{self.url}/_bulk", data=bulk_data, headers=headers, timeout=60)
                if resp.status_code == 200:
                    logger.info(f"Bulk indexed chunk {i//chunk_size + 1} into Elasticsearch")
                else:
                    logger.error(f"Bulk index failed for chunk {i//chunk_size + 1}: {resp.status_code} - {resp.text}")
        else:
            self.local_repo = data
            self._save_local_repo()
            logger.info(f"Saved {len(data)} documents into Local JSON Fallback")


    def search_elastic(self, params: dict):
        searchable_keys = ["country", "city", "occupation", "field"]
        search_params = {k: params.get(k) for k in searchable_keys if params.get(k)}
        
        if not search_params:
            return []

        if self.use_fallback:
            self._load_local_repo()
            results = []
            for item in self.local_repo:
                match = False
                for key, value in search_params.items():
                    if isinstance(value, list):
                        # Match if any synonym matches the item field
                        if any(str(syn).lower() in str(item.get(key, "")).lower() for syn in value):
                            match = True
                            break
                    else:
                        if str(value).lower() in str(item.get(key, "")).lower():
                            match = True
                            break
                if match:
                    results.append(item)
            return results[:20]

        must_filters = []
        for key, value in search_params.items():
            if isinstance(value, list) and len(value) > 0:
                # Use a nested SHOULD for synonyms within this specific category (AND category1 AND (syn1 OR syn2))
                synonym_shoulds = []
                for syn in value:
                    synonym_shoulds.append({
                        "match": {
                            key: {
                                "query": syn,
                                "operator": "and"
                            }
                        }
                    })
                must_filters.append({
                    "bool": {
                        "should": synonym_shoulds,
                        "minimum_should_match": 1
                    }
                })
            else:
                must_filters.append({
                    "match": {
                        key: {
                            "query": value,
                            "operator": "and"
                        }
                    }
                })
        
        query = {
            "query": {
                "bool": {
                    "must": must_filters
                }
            },
            "size": 20
        }

        try:
            response = requests.post(f"{self.url}/{ELASTIC_INDEX}/_search", json=query, timeout=10)
            if response.status_code == 200:
                hits = response.json()["hits"]["hits"]
                return [hit["_source"] for hit in hits]
            else:
                logger.error(f"Elasticsearch search failed: {response.status_code} - {response.text}")
                return []
        except Exception as e:
            logger.error(f"Elasticsearch search error: {e}")
            return []

