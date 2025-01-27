import json

with open("redis_db_mapping.json", "r", encoding="utf-8") as file:
    data = json.load(file)
    
print(data)
print(data["redis_db"]["superset"])