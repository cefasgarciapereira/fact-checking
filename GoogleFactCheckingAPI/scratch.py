
import json

data = []

for i in range(0, 10000):
    data.append({
        "index": i
    })
    if (i % 5) == 0:
        print(i)
        with open('./dataset/scratch_chunk.json', 'w') as outfile:
            json.dump(data, outfile)
        outfile.close()
