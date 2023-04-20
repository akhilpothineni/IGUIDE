import os
import json

directory = '2019_HurricaneHarvey/US_2019Hurricane_raw_data_FL/hurricane'
storage = 'DataExtracted'

for count, file in enumerate(os.listdir(directory)):

    f = os.path.join(directory, file)
    wf = os.path.join(storage, str(count)+'.json')
    print('file:', file)
    if os.path.isfile(f):
        if file.lower().endswith('.json'):
            temp = open(f, 'r')
            info = json.load(temp)

            if 'data' in info.keys():    
                data = []
                for val in info['data']:
                    shard = {}
                    inner_key = val.keys()
                    if 'text' in inner_key:
                        shard['text'] = val['text']
                    if 'geo' in inner_key:
                        shard['geo'] = val['geo']
                    if 'created_at' in inner_key:
                        shard['created_at'] = val['created_at']
                    data.append(shard)
                
                with open(wf, 'w', encoding='utf-8') as cleaned:
                    json.dump(data, cleaned)
            temp.close()
    print('end file')
