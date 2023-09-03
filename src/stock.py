from typing import Union
import matplotlib.pyplot as plt
import datetime
import pandas as pd
import numpy as np

import src.enumerate_classes as enumcls


class Stock:
    def __init__(self, ticker: str = "AAPL",
                 start_date : Union[datetime.datetime,str] = None,
                 end_date : Union[datetime.datetime,str] = None):

        self.ticker = ticker
        self.data = pd.read_csv(filepath_or_buffer = f"../data/raw/{ticker}.csv")
        if type(self.data["Date"][0]) != datetime.datetime:
            self.data["Date"] = pd.to_datetime(self.data["Date"], format='%Y-%m-%d')
        if start_date is not None:
            if type(start_date) == str:
                start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d')
            self.data = self.data[self.data["Date"] >= start_date]
        if end_date is not None:
            if type(end_date) == str:
                end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d')
            self.data = self.data[self.data["Date"] <= end_date]

    def __getitem__(self, column : str):
        if column in self.data.columns: ## changer ça en erreur
            return self.data[column]

    def __setitem__(self, column : str, value):
        if column in self.data.columns:
            self.data[column] = value


    def get_historical_data(self,
                            start_date : datetime.datetime = None,
                            end_date : datetime.datetime = None,
                            inplace = False) -> Union[None,pd.DataFrame]:
        if start_date is not None:
            data_temp = self.data[self.data["Date"] >= start_date]
        if end_date is not None:
            data_temp = self.data[self.data["Date"] <= end_date]
        if inplace is True:
            self.data = data_temp
        else:
            return data_temp

    def plot_histogram(self,
                       column_name : str = 'Adj Close',
                       bins : int = None,
                       start_date : Union[datetime.datetime,str] = None,
                       end_date : Union[datetime.datetime,str] = None) -> None:

        if column_name not in self.data.columns: ## transformer ça en erreur plutôt
            column_name = 'Adj Close'

        if start_date is None:
            start_date = self["Date"].iloc[self[column_name].first_valid_index()]
        if end_date is None:
            end_date = self["Date"].iloc[self[column_name].last_valid_index()]

        if bins is None:
            sample_size = self.data[(self["Date"] >= start_date) & (self["Date"] <= end_date)].shape[0]
            n = 50
            if sample_size >= 10000 :
                bins = int(sample_size ** (1 / 3))
            else:
                if n >= 2*sample_size:
                    bins = int(sample_size)
                else:
                    bins = n


        arr = np.array(self.data[column_name][(self["Date"] >= start_date) & (self["Date"] <= end_date)])
        plt.hist(arr, bins = bins, density = True)
        plt.xlabel(column_name) ; plt.grid()
        plt.title(f"{self.ticker} | Histogramme de {column_name} | {start_date} to {end_date}")
        plt.show()

    def add_indicators(self,indicator : str = 'log return 1d', column_name : str = "Adj Close",start_date : Union[datetime.datetime,str,None] = None, end_date : Union[datetime.datetime,str,None] = None, inplace = True):
        if start_date is None:
            start_date = self["Date"].iloc[0]
        if end_date is None:
            end_date = self["Date"].iloc[-1]

        arr = np.array(self[column_name][(self['Date'] >= start_date) & (self["Date"] <= end_date)])
        temp = [1]
        indicator = enumcls.return_element(indicator, enumcls.indicators)
        match indicator:
            case enumcls.indicators.log_return_1d:
                for i in range(1, len(arr)): ## TODO : VECTORIZE IT PLS
                    temp.append(arr[i] / (arr[i - 1]))
                temp = np.log(np.array(temp))
        if inplace is True:
            self.data[indicator.value] = np.zeros(self.data.shape[0])
            self.data[indicator.value] = np.nan
            self.data[indicator.value][(self.data["Date"] >= start_date) & (self.data["Date"] <= end_date)] = temp
        else:
            return temp




