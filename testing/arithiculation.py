import requests
import time
from io import BytesIO
from PIL import ImageDraw
import random
import os

SERVER_URL = 'http://127.0.0.1:8002/result/'

base_path='/Users/varunchandrashekar/Downloads/BenchmarkingData/'
img_paths = [file for file in os.listdir(base_path) if file[-4:] != '.txt']
img_paths = [file for file in os.listdir(base_path) if file[0] != '.']
uuids = set(f"{pth}__{i}__" for i, pth in enumerate(img_paths))
# tot_count = sum(uuids.values())

OUT_dict = {}

while len(uuids)>0:
    for i, uuid in enumerate([*uuids]):
        try:
            response = requests.get(SERVER_URL, params={"uuid": uuid}, timeout=5)
            # print(response)
            if response.status_code == 200:
                data = response.json()
                # print(data, response)
                print(data, i, len(uuids), uuid)
                if data["status"] == "Completed":
                    OUT_dict[uuid] = time.time_ns()
                    print(uuid)
                    # print(response._content)
                    uuids-={uuid}
        except Exception as e:
            # print(e)
            pass

with open('./end_res.txt', 'w') as f:
    f.write('a={\n')
    for k,v in OUT_dict.items():
        f.write(f"\"{k}\":{v},\n")
    f.write('}')