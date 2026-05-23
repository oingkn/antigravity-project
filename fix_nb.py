import json
import glob
import os

def fix_notebook(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        nb = json.load(f)

    changed = False
    for cell in nb['cells']:
        if cell['cell_type'] == 'code':
            source = "".join(cell['source'])
            if 'import matplotlib' in source and 'platform.system' in source:
                # Let's replace the whole font logic cell with proper rcParams setup
                new_source = []
                for line in cell['source']:
                    if "matplotlib.rc('font', family='Malgun Gothic')" in line:
                        new_source.append(line.replace("matplotlib.rc('font', family='Malgun Gothic')", "matplotlib.rcParams['font.family'] = 'Malgun Gothic'"))
                        changed = True
                    elif "matplotlib.rc('font', family='AppleGothic')" in line:
                        new_source.append(line.replace("matplotlib.rc('font', family='AppleGothic')", "matplotlib.rcParams['font.family'] = 'AppleGothic'"))
                        changed = True
                    elif "matplotlib.rc('font', family='NanumGothic')" in line:
                        # For Linux, also clear font cache before setting it!
                        # But to keep it simple, just substitute rcParams
                        new_source.append(line.replace("matplotlib.rc('font', family='NanumGothic')", "matplotlib.rcParams['font.family'] = 'NanumGothic'"))
                        changed = True
                    else:
                        new_source.append(line)
                
                # Check for nanum font manager flush if linux is detected
                # To be completely safe and avoid NanumGothic error on colab:
                fixed_source = []
                for idx, line in enumerate(new_source):
                    if "matplotlib.rcParams['font.family'] = 'NanumGothic'" in line:
                        fixed_source.append("    import matplotlib.font_manager as fm\n")
                        fixed_source.append("    fm._load_fontmanager(try_read_cache=False)\n")
                        fixed_source.append(line)
                    else:
                        fixed_source.append(line)
                
                cell['source'] = fixed_source

    if changed:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(nb, f, ensure_ascii=False, indent=1)
        print(f"Fixed {file_path}")

for ipynb in glob.glob("*.ipynb"):
    fix_notebook(ipynb)
