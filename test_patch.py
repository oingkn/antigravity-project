import sys
import scipy.linalg

# [Fix] Gensim & Scipy Compatibility Monkeypatch
import scipy.linalg.basic
import scipy.linalg.special_matrices
import numpy as np

# Select triu from scipy.linalg or fallback to numpy
triu = getattr(scipy.linalg, 'triu', np.triu)

# Inject triu into the submodules where old gensim versions look for it
scipy.linalg.basic.triu = triu
scipy.linalg.special_matrices.triu = triu

# [Fix] Python 3.10+ Compatibility (collections.Mapping move)
import collections
if not hasattr(collections, 'Mapping'):
    import collections.abc
    collections.Mapping = collections.abc.Mapping
    collections.MutableMapping = collections.abc.MutableMapping
    collections.Iterable = collections.abc.Iterable
    collections.Sequence = collections.abc.Sequence
    collections.Callable = collections.abc.Callable


print("Monkeypatch applied.")

# Now try the import that failed
try:
    from gensim.models import Word2Vec
    print("Successfully imported Word2Vec from gensim!")
except ImportError as e:
    print(f"Failed to import Word2Vec: {e}")
except Exception as e:
    print(f"An error occurred: {e}")
