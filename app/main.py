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
    
    def remove_duplicates(pg_res, es_res):
        seen = set()
        merged = []
        dupes = 0
        for item in pg_res + es_res:
            if "error" in item: continue
            key = (item["occupation"], item["field"], item["city"], item["country"])
            if key not in seen:
                seen.add(key)
                merged.append(item)
            else:
                dupes += 1
        return merged, dupes

    # ------------------
    # 2. STRICT QUERIES (VERIFIED RESULTS)
    # ------------------
    try:
        pg_strict = search_pg(strict)
    except Exception as e:
        logger.exception("PostgreSQL strict search failed")
        pg_strict = [{"error": str(e)}]
        
    try:
        es_strict = es_client.search_elastic(strict)
    except Exception as e:
        logger.exception("Elasticsearch strict search failed")
        es_strict = [{"error": str(e)}]
        
    merged_strict, strict_dupes = remove_duplicates(pg_strict, es_strict)

    # ------------------
    # 3. INFERRED QUERIES (AI CONTEXTUAL RESULTS)
    # ------------------
    # Only execute inferred search if the LLM provided inferred rules
    merged_inferred, inferred_dupes = [], 0
    pg_inferred_res, es_inferred_res = [], []
    
    # Check if there are actual non-null values in the inferred dict
    has_inferences = any(v is not None for v in inferred.values())
    
    if has_inferences:
        try:
            pg_inferred_res = search_pg(inferred)
        except Exception:
            pass
            
        try:
            es_inferred_res = es_client.search_elastic(inferred)
        except Exception:
            pass
            
        raw_merged_inferred, inferred_dupes = remove_duplicates(pg_inferred_res, es_inferred_res)
        
        # PREVENT DUPLICATES ACROSS SECTIONS:
        # We do not want to show an item in "Inferred Results" if it already showed up in "Verified Results"
        verified_keys = {(i.get("occupation"), i.get("field"), i.get("city"), i.get("country")) for i in merged_strict}
        
        for item in raw_merged_inferred:
            key = (item.get("occupation"), item.get("field"), item.get("city"), item.get("country"))
            if key not in verified_keys:
                merged_inferred.append(item)
    
    # ------------------
    # 4. BUILD RESPONSE
    # ------------------
    return {
        "status": "success",
        "query": q,
        "extracted_params": extracted_params,
        "results": {
            "verified": {
                "total_found": len(merged_strict),
                "duplicates_removed": strict_dupes,
                "data": merged_strict,
                "postgres_found": len([x for x in pg_strict if "error" not in x]),
                "elastic_found": len([x for x in es_strict if "error" not in x]),
                "postgres_data": [x for x in pg_strict if "error" not in x],
                "elastic_data": [x for x in es_strict if "error" not in x]
            },
            "inferred": {
                "total_found": len(merged_inferred),
                "data": merged_inferred,
                "active": has_inferences
            }
        }
    }

@app.get("/health")
async def health():
    return {"status": "ok"}
