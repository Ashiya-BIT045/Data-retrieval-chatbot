import requests
import json

def test_search(query):
    print(f"\n--- Testing Query: '{query}' ---")
    url = f"http://localhost:8000/search?q={query}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        print("Status: Success\n")
        
        extracted = data.get("extracted_params", {})
        print("STRICT PARAMS:", extracted.get("strict_params"))
        print("INFERRED PARAMS:", extracted.get("inferred_params"))
        print("\nREASONING:", extracted.get("reasoning"))
        print("-" * 40)
        
        verified = data["results"]["verified"]
        print(f"VERIFIED RESULTS: Found {verified['total_found']} (Omitted {verified['duplicates_removed']} dupes)")
        
        inferred = data["results"]["inferred"]
        if inferred["active"]:
            print(f"INFERRED RESULTS (ACTIVE): Found {inferred['total_found']}")
        else:
            print("INFERRED RESULTS (INACTIVE): No inferences made by AI.")
            
    else:
        print(f"Failed with status code: {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    test_search("Software Engineer in NYC")
    test_search("hr who speaks hindi")
