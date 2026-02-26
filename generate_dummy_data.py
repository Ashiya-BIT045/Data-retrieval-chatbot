import pandas as pd
import os

data = [
    {"country": "UAE", "city": "Dubai", "occupation": "Software Engineer", "field": "Technology"},
    {"country": "USA", "city": "New York", "occupation": "Data Scientist", "field": "Technology"},
    {"country": "UK", "city": "London", "occupation": "Product Manager", "field": "Business"},
    {"country": "Germany", "city": "Berlin", "occupation": "DevOps Engineer", "field": "Technology"},
    {"country": "Canada", "city": "Toronto", "occupation": "UX Designer", "field": "Design"},
]

df = pd.DataFrame(data)

os.makedirs("data", exist_ok=True)
df.to_excel("data/psql_file.xlsx", index=False)
df.to_excel("data/elastic_search_data.xlsx", index=False)

print("Dummy data files created in data/")
