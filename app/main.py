import os
import time


# Disable proxies for local services (MUST BE AT TOP)
os.environ['NO_PROXY'] = 'localhost,127.0.0.1'

from fastapi import FastAPI, Query, HTTPException
from .llm_agent import LLMAgent
from .db_postgres import search_pg
from .db_elastic import ElasticSearchClient
import logging



app = FastAPI(title="Agentic Data Retrieval API")
llm_agent = LLMAgent()
agent = LLMAgent() # Changed llm_agent to agent
es_client = ElasticSearchClient()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def remove_duplicates(pg_res, es_res):
    seen = set()
    merged = []
    dupes = 0
    for item in pg_res + es_res:
        if "error" in item: continue
        key = (item.get("occupation"), item.get("field"), item.get("city"), item.get("country"))
        if key not in seen:
            seen.add(key)
            merged.append(item)
        else:
            dupes += 1
    return merged, dupes

@app.get("/search")
def search(q: str):
    logger.info(f"Received search query: {q}")
    
    # 1. Parse Query via LLM
    start_time = time.time()
    try:
        extracted_params = agent.parse_query(q)
        logger.info(f"Extracted parameters: {extracted_params}")
    except Exception as e:
        logger.exception("Failed to parse query via LLM")
        raise HTTPException(status_code=500, detail="Error parsing query")
    llm_time = time.time() - start_time
    logger.info(f"LLM Parsing took {llm_time:.2f} seconds")

    # The AI now returns "strict_params" and "inferred_params"
    strict = extracted_params.get("strict_params", {})
    inferred = extracted_params.get("inferred_params", {})
    
    # Merge strict and inferred params for a unified "Best Effort" Search Agenda
    # We prioritize strict, but if inferred adds a country/city missing from strict, we use it.
    unified_query = {}
    for key in ["occupation", "field", "city", "country"]:
        s_val = strict.get(key)
        i_val = inferred.get(key)
        
        # Combine lists (synonyms) from both layers
        combined = []
        if isinstance(s_val, list): combined.extend(s_val)
        elif s_val: combined.append(s_val)
        
        if isinstance(i_val, list): combined.extend(i_val)
        elif i_val: combined.append(i_val)
        
        # Remove duplicates from the synonym list
        if combined:
            unified_query[key] = list(dict.fromkeys([str(x) for x in combined if x]))

    # ------------------
    # 2. UNIFIED SEARCH
    # ------------------
    pg_query_raw, es_query_raw = "", ""
    try:
        pg_results, pg_query_raw = search_pg(unified_query)
    except Exception as e:
        logger.exception("PostgreSQL search failed")
        pg_results = []
        
    try:
        es_results, es_query_raw = es_client.search_elastic(unified_query)
    except Exception as e:
        logger.exception("Elasticsearch search failed")
        es_results = []
        
    merged_results, total_dupes = remove_duplicates(pg_results, es_results)

    # ------------------
    # 3. BUILD RESPONSE
    # ------------------
    return {
        "status": "success",
        "query": q,
        "extracted_params": extracted_params,
        "unified_query": unified_query,
        "raw_queries": {
            "postgres": pg_query_raw,
            "elasticsearch": es_query_raw
        },
        "results": {
            "verified": {
                "total_found": len(merged_results),
                "duplicates_removed": total_dupes,
                "data": merged_results,
                "postgres_found": len(pg_results),
                "elastic_found": len(es_results),
                "postgres_data": pg_results,
                "elastic_data": es_results
            },
            "inferred": {
                "total_found": 0,
                "data": [],
                "active": False,
                "note": "Results merged into verified section"
            }
        }
    }

@app.get("/health")
async def health():
    return {"status": "ok"}
