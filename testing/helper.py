def write_dict(filename,d):
    with open(filename, 'w') as f:
        f.write('a={\n')
        for k,v in d.items():
            formated_v = ',\n'.join(map(str,v))
            f.write(f"\"{k}\":[\n{formated_v}\n],\n")
        f.write('}')