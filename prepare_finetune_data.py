import os
import json
import sys
sys.path.insert(0, r'C:\Users\djordje\PythonGPT3Tutorial')
import my_functions

# cita promptove i odgovore i smesta ih u JSON za fine-tuning

src_dir = 'completions/'
prompt_dir = 'prompts/'


if __name__ == '__main__':
    files = os.listdir(src_dir)
    data = list()
    for file in files:
        completion = my_functions.open_file(src_dir + file)
        prompt = my_functions.open_file(prompt_dir + file)
        info = {'prompt': prompt, 'completion': completion}
        data.append(info)
    with open('plots.jsonl', 'w', encoding='utf-8') as outfile:
        for i in data:
            json.dump(i, outfile)
            outfile.write('\n')