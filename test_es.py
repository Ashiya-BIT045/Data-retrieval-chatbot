import requests

url = "http://127.0.0.1:9200"
print(f"Testing connection to {url}")
try:
    response = requests.get(url)
    print(f"Response status: {response.status_code}")
    print(f"Response body: {response.json()}")
    
    if response.status_code == 200:
        print("Success: Reachable via requests!")
        # Try to create an index
        create_resp = requests.put(f"{url}/test_index_req")
        print(f"Create index response: {create_resp.status_code} - {create_resp.text}")
    else:
        print("Error: Status code not 200.")
except Exception as e:
    print(f"Error: Exception occurred: {e}")
    traceback.print_exc()


