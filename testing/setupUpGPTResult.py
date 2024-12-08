import os
import json

data = {}

for image in os.listdir("/Users/varunchandrashekar/Downloads/BenchmarkingData"):
    with open(f"./gptTemplates/{image[:-4]}.yaml", "w") as file:
        pass