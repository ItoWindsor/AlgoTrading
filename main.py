import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os


df = pd.read_csv("data/raw/AAPL.csv")

plt.plot(df["Date"][:10],df["Close"][:10])
plt.grid() ; plt.show()


