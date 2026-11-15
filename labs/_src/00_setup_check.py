# %% [markdown]
# # Setup check
#
# Run every cell once before Day 1. It imports the libraries the labs use, reads the four population files of Zulal Water Utility and draws one seeded sample. Nothing here calls or downloads a model.

# %%
import os, sys, subprocess
from pathlib import Path

IN_COLAB = "google.colab" in sys.modules
if IN_COLAB:
    REPO_URL = "https://github.com/SDAIAAcademy/ds-201.git"
    if not Path("/content/ds-201").exists():
        subprocess.run(["git", "clone", "-q", REPO_URL, "/content/ds-201"], check=True)
    os.chdir("/content/ds-201/labs")
    subprocess.run([sys.executable, "-m", "pip", "install", "-q", "-r", "requirements-colab.txt"], check=True)
else:
    while not Path("zulal.py").exists() and Path.cwd() != Path.cwd().parent:
        os.chdir("..")  # solutions/ notebooks run from labs/
sys.path.insert(0, os.getcwd())

import numpy as np
import pandas as pd
import zulal as U
np.set_printoptions(precision=3, suppress=True)
print("mode:", U.MODE)

# %%
import importlib

missing = []
for name in ("numpy", "pandas", "scipy", "statsmodels", "matplotlib"):
    try:
        mod = importlib.import_module(name)
        print(f"✅ {name} {mod.__version__}")
    except ImportError:
        missing.append(name)
        print(f"❌ {name} is missing")

# %%
counts = {"districts": len(U.districts()), "households": len(U.households()), "repairs": len(U.repairs()), "survey": len(U.survey())}
print(counts)
ok = counts == {"districts": 30, "households": 80_000, "repairs": 12_000, "survey": 9_000}
U.check(ok, "the four population files are complete: 30 districts, 80,000 households, 12,000 repairs, 9,000 survey responses")

# %%
x = U.households()["consumption_l_day"].to_numpy(float)
m = float(U.rng(1).choice(x, size=50, replace=False).mean())
print(f"a seeded sample of 50 households has mean consumption {m:.1f} litres a day; your neighbour should read the same number")
plt = U.plt()
plt.hist(x, bins=40)
plt.title("Daily consumption of 80,000 households, litres")
plt.show()

# %%
if missing:
    print("Missing:", ", ".join(missing), "· locally run `uv sync` in labs/; in Colab rerun the first cell.")
else:
    print("Ready for Day 1.")
