import os, subprocess

template_folder = "./generatedTemplates/"
results_path = 'cfn_results.txt'

files = os.listdir(template_folder)
OUTPUT = {}
for i, file in enumerate(files):
    try:
        result = subprocess.run(['cfn-lint', template_folder+file], capture_output=True, text=True, check=True)
        print(f"\r {i}/{len(files)} ", end='        ')
        OUTPUT[file] = "SUCCESS"
    except subprocess.CalledProcessError as e:
        OUTPUT[file] = e.stdout
    except FileNotFoundError:
        print("Error: File Not found.")

with open(results_path, 'w') as f:
    f.write('a={\n')
    for k,v in OUTPUT.items():
        f.write(f"\"{k}\":\"\"\"\n{v}\n\"\"\",\n")
    f.write('}')