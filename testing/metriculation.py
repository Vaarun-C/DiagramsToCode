import requests
import time
from io import BytesIO
from PIL import ImageDraw
import random
import os

SERVER_URL = 'http://127.0.0.1:8002/generateawstemplate'

base_path='/Users/varunchandrashekar/Downloads/BenchmarkingData/'
img_paths = [file for file in os.listdir(base_path) if file[-4:] != '.txt']
img_paths = [file for file in os.listdir(base_path) if file[0] != '.']

OUT_dict = {}

def run_itall(img_path):
    strt_time = time.time_ns()
    with open(base_path + img_path, 'rb') as img_bytes:
        uuid = img_path+f'__{i}__'#str(random.random()).replace('.','')
        files = {'ArchitectureDiagram': (img_path, img_bytes, 'image/png')}
        data = {"UUID":uuid}
        try:
            response = requests.post(SERVER_URL, files=files, data = data, timeout=5)
        
            if response.status_code == 200:
                print('Response from server:', response.text)
            else:
                print('not Successful', response.status_code, response.reason)
        except Exception as e:
            print(e)
        OUT_dict[uuid] = strt_time



for i, img_path in enumerate(img_paths):
    run_itall(img_path)


    # break



with open('./start_res.txt', 'w') as f:
    f.write('a={\n')
    for k,v in OUT_dict.items():
        f.write(f"\"{k}\":{v},\n")
    f.write('}')