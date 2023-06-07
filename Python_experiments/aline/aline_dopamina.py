import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os


files = [
    r"C:\Users\uzuna\Documents\GITHUB\My_projects\Lab_Projects_as_IC\aline\A1.xlsx",
    r"C:\Users\uzuna\Documents\GITHUB\My_projects\Lab_Projects_as_IC\aline\A2-2.xlsx",
    r"C:\Users\uzuna\Documents\GITHUB\My_projects\Lab_Projects_as_IC\aline\A3-2.xlsx",
    r"C:\Users\uzuna\Documents\GITHUB\My_projects\Lab_Projects_as_IC\aline\A5-2.xlsx",
    r"C:\Users\uzuna\Documents\GITHUB\My_projects\Lab_Projects_as_IC\aline\A7-2.xlsx",
    r"C:\Users\uzuna\Documents\GITHUB\My_projects\Lab_Projects_as_IC\aline\A8-2.xlsx",
    r"C:\Users\uzuna\Documents\GITHUB\My_projects\Lab_Projects_as_IC\aline\A9-2.xlsx",
]

data = pd.read_excel(files[0])
x_ticks = data["x"]
F0 = sum(data["x"][0:100]) / 100
fig, ax = plt.subplots()

df_f0 = []
for i, file in enumerate(files):
    print(f"Processing file {i + 1} of {len(files)}")
    # filename without extension
    filename = os.path.splitext(os.path.basename(file))[0]
    data = pd.read_excel(file)
    data.columns = pd.MultiIndex.from_frame(data.columns.to_frame().applymap(str.lower))
    for i in range(len(data["y"])):
        df_f0.append(data["y"].iloc[i] - F0 / F0)
    ax.plot(x_ticks, df_f0, label=f"{filename}")
    df_f0 = []


ax.set_title("Intensidade de fluorescência em função do comprimento de onda")
ax.set_xlabel("Comprimento de onda")
ax.set_ylabel("dF-F0")
ax.set_ylim(0, 10000)
ax.legend()
# plt.show()
fig.set_size_inches(19.20, 10.80)
plt.savefig("F-F0.svg", dpi=100, format="svg")

pass
