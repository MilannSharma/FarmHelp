import json
import os

if os.path.exists('agriculture_knowledge_base.json'):
    with open('agriculture_knowledge_base.json', encoding='utf-8') as f:
        data = json.load(f)
    print('Articles:', len(data))
    if data:
        print('Sample article keys:', list(data[0].keys()) if isinstance(data[0], dict) else 'Not a dict')
else:
    print('File does not exist')
