import json
filtered = []

with open('./dataset/data_feed.json') as json_file:
    data = json.load(json_file)
    print(len(data["dataFeedElement"]))
    