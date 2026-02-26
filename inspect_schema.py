import pandas as pd
import json

def inspect_excel(filename):
    try:
        df = pd.read_excel(filename)
        return {
            "columns": df.columns.tolist(),
            "first_row": df.iloc[0].to_dict() if not df.empty else None,
            "row_count": len(df)
        }
    except Exception as e:
        return {"error": str(e)}

result = {
    "psql": inspect_excel("data/psql_file.xlsx"),
    "elastic": inspect_excel("data/elastic_search_data.xlsx")
}

with open("schema_inspection.json", "w") as f:
    json.dump(result, f, indent=2)

print("Inspection complete. Result saved to schema_inspection.json")
