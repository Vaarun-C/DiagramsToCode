from collections import Counter
from groundTruth import ground_truth_data
from GPTresponses import GPTIconDetections as gpt_data
from detected_icons import a as icon_data
from mapForiconNameType import mapTypesToNames


COUNT = {}
for img_name in ground_truth_data:
    list_a = ground_truth_data[img_name]
    list_b = list(map(lambda x:x[1],icon_data[img_name]))
    list_c = []

    # Map GPT detected icons to image names if it is not supported
    for resource in gpt_data[img_name]:
        mappedName = mapTypesToNames.get(resource, resource)
        list_c.append(mappedName)

    count_a = Counter(list_a)
    count_b = Counter(list_b)
    count_c = Counter(list_c)

    onlyA__b = []
    for item in count_a:
        if item not in count_b:
            onlyA__b.extend([item] * count_a[item])
        elif count_a[item] > count_b[item]:
            onlyA__b.extend([item] * (count_a[item] - count_b[item]))

    onlyA__c = []
    for item in count_a:
        if item not in count_b:
            onlyA__c.extend([item] * count_a[item])
        elif count_a[item] > count_b[item]:
            onlyA__c.extend([item] * (count_a[item] - count_b[item]))

    # Find elements only in B
    onlyB = []
    for item in count_b:
        if item not in count_a:
            onlyB.extend([item] * count_b[item])
        elif count_b[item] > count_a[item]:
            onlyB.extend([item] * (count_b[item] - count_a[item]))
    
    onlyC = []
    for item in count_c:
        if item not in count_a:
            onlyC.extend([item] * count_c[item])
        elif count_c[item] > count_a[item]:
            onlyC.extend([item] * (count_c[item] - count_a[item]))

    # Find elements in both A and B
    bothAB = []
    for item in count_a:
        if item in count_b:
            bothAB.extend([item] * min(count_a[item], count_b[item]))
    
    bothAC = []
    for item in count_a:
        if item in count_c:
            bothAC.extend([item] * min(count_a[item], count_c[item]))

    print("Only in A:", onlyA__b, onlyA__c)
    print("Only in B:", onlyB)
    print("In both A and B:", bothAB)
    print(len(list_a), len(onlyB), len(bothAB))
    # input()
    COUNT[img_name] = len(list_a), len(bothAB), len(onlyB), len(onlyA__b), len(bothAC), len(onlyC), len(onlyA__c)
print(COUNT[img_name])
with open("icon_stats.csv", "w") as f:
    heading = "IMG NAME"
    heading +=",No.of Icon in img"
    heading +=",No.of icons detected correctly by Diagrams2Code"
    heading +=",No.of False Positives by Diagrams2Code"
    heading +=",No.of icons failed to be detected by Diagrams2Code"
    heading +=",No.of icons detected correctly by GPT"
    heading +=",No.of False Positives by GPT"
    heading +=",No.of icons failed to be detected by GPT"
    heading+="\n"
    f.write(heading)
    for k,v in COUNT.items():
        vv=','.join(map(str,v))
        f.write(f"{k},{vv}\n")
