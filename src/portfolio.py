import datetime
from typing import Union, Dict, Any
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

import src.stock as stock

class Portfolio:

    def __init__(self, tickers = ('AAPL',)):
        temp = [stock.Stock(ticker = key) for key in tickers]
        self.assets = dict(zip(tickers, temp))

    def __str__(self):
        returned_str = "assets :"
        for ticker in self.assets.keys():
            returned_str += f" {ticker}"
        return returned_str

    def __getitem__(self, ticker : str):
        if ticker in self.assets.keys(): ## changer ça en erreur
            return self.assets[ticker]

    def __setitem__(self, ticker : str, value):
        if ticker in self.assets.keys():
            self.assets[ticker] = value

    def get_common_start_date(self, start_date : Union[datetime.datetime,str,None] = None) -> datetime.datetime:
        tickers = list(self.assets.keys())
        tickers = [ticker for ticker in tickers if (ticker in self.assets.keys())]

        if type(start_date) == str:
            start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d')
            common_start_date = start_date
        else:
            common_start_date = self.assets[tickers[0]].data["Date"].iloc[0]

        for ticker in tickers:
            if common_start_date < self.assets[ticker].data["Date"].iloc[0]:
                common_start_date = self.assets[ticker].data["Date"].iloc[0]

        return common_start_date

    def get_common_end_date(self, end_date : Union[datetime.datetime,str,None] = None) -> datetime.datetime:
        tickers = list(self.assets.keys())
        tickers = [ticker for ticker in tickers if (ticker in self.assets.keys())]

        if end_date is not None:
            if type(end_date) == str:
                end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d')
                common_end_date = end_date
        else:
            common_end_date = self.assets[tickers[0]].data["Date"].iloc[-1]

        for ticker in tickers:
            if common_end_date > self.assets[ticker].data["Date"].iloc[-1]:
                common_end_date = self.assets[ticker].data["Date"].iloc[-1]

        return common_end_date

    def get_historical_data(self,start_date : Union[datetime.datetime,str,None] = None, end_date : Union[datetime.datetime,str,None] = None, inplace : bool = False) ->  Union[None,Dict[str, Any]]:
        min_date = start_date
        max_date = end_date
        for ticker in self.assets.keys():
            if self.assets[ticker].data["Date"].iloc[0] <= min_date:
                min_date = self.assets[ticker].data["Date"].iloc[0]
            if self.assets[ticker].data["Date"].iloc[-1] <= max_date:
                max_date = self.assets[ticker].data["Date"].iloc[-1]

        if inplace is True:
            for ticker in self.assets.keys():
                self.assets[ticker] = self.assets[ticker].get_historical_data(start_date = start_date, end_date = end_date)
        else:
            temp = [stock.Stock(ticker = key, start_date = start_date, end_date = end_date) for key in self.assets.keys()]
            return dict(zip(self.assets.keys(), temp))


    def plot_prices(self, tickers : tuple = None, column_name : str = 'Adj Close', normalized_data : bool = True,start_date : Union[datetime.datetime,str,None] = None, end_date : Union[datetime.datetime,str,None] = None):
        if tickers is None:
            tickers = list(self.assets.keys())
        tickers = [ticker for ticker in tickers if (ticker in self.assets.keys())]

        common_start_date = self.get_common_start_date(start_date = start_date)
        common_end_date = self.get_common_end_date(end_date = end_date)

        for ticker in tickers:
            dates = self[ticker]["Date"][(self[ticker]["Date"] >= common_start_date) & (self[ticker]["Date"] <= common_end_date)]
            prices = np.array(self[ticker][column_name][(self[ticker]["Date"] >= common_start_date) & (self[ticker]["Date"] <= common_end_date)])
            normalize_value = prices[0]*(normalized_data is True)  +1*(normalized_data is not True)
            prices = prices/normalize_value

            plt.plot(dates,prices,label = ticker)

        title = "Comparaison de différents stock price | " + "normalized data"*(normalized_data is True) + "non normalized data"*(normalized_data is not True)
        plt.grid() ; plt.legend() ; plt.title(title)
        plt.ylabel(column_name) ; plt.xlabel("Date")
        plt.show()
        
    def add_indicators(self,indicator : str = 'log return 1D', tickers : tuple = None, column_name : str = "Adj Close",start_date : Union[datetime.datetime,str,None] = None, end_date : Union[datetime.datetime,str,None] = None):
        if tickers is None:
            tickers = list(self.assets.keys())
        tickers = [ticker for ticker in tickers if (ticker in self.assets.keys())]

        common_start_date = self.get_common_start_date(start_date= start_date)
        common_end_date = self.get_common_end_date(end_date = end_date)

        for ticker in tickers:
            self[ticker].add_indicators(indicator = indicator, column_name = column_name, start_date = common_start_date, end_date = common_end_date, inplace = True)


    def compute_correlations(self, tickers : list = None, column_name : str = 'Adj Close',start_date : Union[datetime.datetime,str,None] = None, end_date : Union[datetime.datetime,str,None] = None):
        if tickers is None:
            tickers = list(self.assets.keys())
        tickers = [ticker for ticker in tickers if (ticker in self.assets.keys())]


        common_start_date = self.get_common_start_date(start_date = start_date)
        common_end_date = self.get_common_end_date(end_date = end_date)

        ## A COMPLETER
        arr = np.array([self[ticker][column_name][(self[ticker]["Date"] >= common_start_date) & (self[ticker]["Date"] <= common_end_date)] for ticker in tickers])
        return np.corrcoef(arr)

    def plot_heatmap(self, tickers : list = None, column_name : str = 'Adj Close',start_date : Union[datetime.datetime,str,None] = None, end_date : Union[datetime.datetime,str,None] = None) -> None:
        correlation_matrix = self.compute_correlations(tickers = tickers, column_name = column_name,start_date = start_date, end_date = end_date)
        sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0, xticklabels=tickers, yticklabels=tickers)
        plt.title(f'Correlation Heatmap | {start_date} to {end_date}')
        plt.show()

    def plot_histogram(self, tickers : tuple = None, column_name : str = "Adj Close", bins : int = None,start_date : Union[datetime.datetime,str,None] = None, end_date : Union[datetime.datetime,str,None] = None):
        if tickers is None:
            tickers = list(self.assets.keys())
        tickers = [ticker for ticker in tickers if (ticker in self.assets.keys())]

        if column_name not in self.assets[tickers[0]].data.columns: ## transformer ça en erreur plutôt
            column_name = 'Adj Close'

        common_start_date = self.get_common_start_date(start_date=start_date)
        common_end_date = self.get_common_end_date(end_date=end_date)

        if bins is None:
            temp_asset = self.assets[tickers[0]]
            sample_size = temp_asset.data[(temp_asset.data["Date"] >= common_start_date) & (temp_asset.data["Date"] <= common_end_date)].shape[0]
            n = 50
            if sample_size >= 10000 :
                bins = int(sample_size ** (1 / 3))
            else:
                if n >= 2*sample_size:
                    bins = int(sample_size)
                else:
                    bins = n

        for ticker in tickers:
            arr = np.array(self[ticker][column_name][(self[ticker]["Date"] >= common_start_date) & (self[ticker]["Date"] <= common_end_date)])
            plt.hist(arr, bins=bins, density=True, label = f"{ticker}")

        plt.xlabel(column_name) ; plt.grid() ; plt.legend()
        plt.title(f"Histogramme de {column_name} | {common_start_date} to {common_end_date}")
        plt.show()

    






