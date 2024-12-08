from groundTruth import GROUND_TRUTH
import os

images = os.listdir('/Users/varunchandrashekar/Downloads/BenchmarkingData')
print(set(images) - set(GROUND_TRUTH.keys()))