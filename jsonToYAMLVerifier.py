import json
from colorama import Back
json.load
with open("./test_for_PROD.json", 'r') as file:
    data = json.load(file)

replacables = {
    "$$0": f"{Back.RED}$$0{Back.RESET}",
    "$$1": f"{Back.GREEN}$$1{Back.RESET}",
    "$$2": f"{Back.BLUE}$$2{Back.RESET}",
    "$$3": f"{Back.YELLOW}$$3{Back.RESET}",
    "$$4": f"{Back.CYAN}$$4{Back.RESET}",
    "$$5": f"{Back.MAGENTA}$$5{Back.RESET}",
    "$$6": f"{Back.LIGHTBLUE_EX}$$6{Back.RESET}",
    
}

def dispFor(KEY, rsc):
    txt = rsc[KEY].replace('  ','[]')
    for k,v in replacables.items():
        txt=txt.replace(k,v)
    print(KEY,'='*100, txt)

for rsc in data:
    dispFor('Parameters', rsc)
    dispFor('Resources', rsc)
    dispFor('Outputs', rsc)
    dispFor('Conditions', rsc)
    print("Dependencies", rsc['Dependencies'])
    input()
