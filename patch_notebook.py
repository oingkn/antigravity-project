import json
import os

notebook_path = r'c:\Users\kyoun\AI Programming\ku-dodatc-aip101\week4_lab.ipynb'

if not os.path.exists(notebook_path):
    print(f"Error: {notebook_path} not found.")
    exit(1)

with open(notebook_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

# The cell to patch is cell index 3 (Library import)
target_cell_index = 3

# Optimized and robust monkeypatch for Gensim 0.10.1 & Scipy 1.7+ & Python 3.10+
patch_code = [
    "import sys\n",
    "import collections\n",
    "import collections.abc\n",
    "import scipy.linalg\n",
    "import scipy.linalg.basic\n",
    "import scipy.linalg.special_matrices\n",
    "import scipy.misc\n",
    "import scipy.special\n",
    "import numpy as np\n",
    "\n",
    "# [Fix] Comprehensive Gensim/Scipy/Python 3.10+ Compatibility Patch\n",
    "\n",
    "# 1. Scipy linalg patch: Inject 'triu' into basic/special_matrices\n",
    "triu = getattr(scipy.linalg, 'triu', getattr(np, 'triu', None))\n",
    "if triu:\n",
    "    scipy.linalg.basic.triu = triu\n",
    "    scipy.linalg.special_matrices.triu = triu\n",
    "\n",
    "# 2. Collections patch: Add Aliases removed in Python 3.10\n",
    "for name in ['Mapping', 'MutableMapping', 'Iterable', 'Sequence', 'Callable']:\n",
    "    if not hasattr(collections, name):\n",
    "        setattr(collections, name, getattr(collections.abc, name))\n",
    "\n",
    "# 3. Scipy misc patch: Add 'logsumexp' moved to scipy.special\n",
    "if not hasattr(scipy.misc, 'logsumexp'):\n",
    "    scipy.misc.logsumexp = scipy.special.logsumexp\n",
    "\n",
    "print(\"✅ Gensim Compatibility Patch Applied\")\n",
    "\n",
    "# "
]

# Reset source if it already contains the patch (to avoid duplicates)
original_source = nb['cells'][target_cell_index]['source']
filtered_source = [line for line in original_source if 'Gensim & Scipy Compatibility' not in line and 'Gensim Compatibility Patch' not in line]

# Also remove everything I previously added if possible, or just start from a known clean line
# The original cell starts with !pip install
start_index = 0
for i, line in enumerate(original_source):
    if line.startswith('!pip install'):
        start_index = i
        break
clean_original_source = original_source[start_index:]

nb['cells'][target_cell_index]['source'] = patch_code + clean_original_source

# Update the complete/finish print statement if needed
for i, line in enumerate(nb['cells'][target_cell_index]['source']):
    if '라이브러리 임포트 완료' in line:
        nb['cells'][target_cell_index]['source'][i] = line.replace('✅ 라이브러리 임포트 완료', '✅ 라이브러리 임포트 완료 (패치 포함)')

with open(notebook_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)

print(f"Successfully applied robust patch to {notebook_path}")
