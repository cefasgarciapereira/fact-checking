import json

INPUT_NAME = './poynter_social_false.json'

with open(INPUT_NAME) as json_file:
    data = json.load(json_file)

for item in data[:5]:
    for fb_id in item['facebook_ids']:
        print(fb_id.replace('_',''))
        print(item)