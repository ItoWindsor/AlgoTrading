import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os


df = pd.read_csv("data/raw/TSLA.csv")

plt.plot(df["Date"],df["Close"])
plt.grid() ; plt.show()