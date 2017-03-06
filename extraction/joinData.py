import os
import json

full_data = []
for i in range(100):
    print(i)
    filename = os.path.join("shard", "shard-" + str(i), "wiki-shard.json")
    with open(filename, "r") as f:
        data = json.load(f)
        full_data.extend(data)

with open("wiki-data-pretty.json", "w") as f:
    json.dump(full_data, f, sort_keys=True, indent=4)
with open("wiki-data.json", "w") as f:
    json.dump(full_data, f)
