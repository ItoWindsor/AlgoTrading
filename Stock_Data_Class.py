import pandas as pd
import os
from datetime import datetime
import seaborn as sns
import matplotlib.pyplot as plt

class StockData:
    def __init__(self, folder_path : str):
        data_frames = []
        for filename in os.listdir(folder_path):
            if filename.endswith('.csv'):
                ticker = filename[:-4]
                file_path = os.path.join(folder_path, filename)
                stock_data = pd.read_csv(file_path)
                stock_data['Ticker'] = ticker
                data_frames.append(stock_data)
        
        self.data = pd.concat(data_frames, ignore_index=True)
        self.data['Date'] =  pd.to_datetime(self.data['Date'])
        self.data['Return'] = self.data.groupby('Ticker')['Adj Close'].pct_change()

    def infos(self) -> None :
        "Display Available Tickers"
        print(f"Current Tickers in dataframe :  {self.data['Ticker'].unique()}")

    def get_historical_data(self, ticker, from_date: str = None, to_date: str = None) -> pd.DataFrame : 
        "return historical data from a specified stock given ticker and optional datetimes"

        filtered_data = self.data[self.data['Ticker'] == ticker]

        if from_date:
            from_date = datetime.strptime(from_date, '%Y-%m-%d')
            filtered_data = filtered_data[filtered_data['Date'] >= from_date]

        if to_date:
            to_date = datetime.strptime(to_date, '%Y-%m-%d')
            filtered_data = filtered_data[filtered_data['Date'] <= to_date]
        return filtered_data
    
    def plot_stocks(self, tickers : str , normalize : bool = False)  -> None :
        sns.set_style('whitegrid') 

        common_start_date = None
        for ticker in tickers:
            stock_data = self.get_historical_data(ticker)
            start_date = stock_data['Date'].iloc[0]
            if common_start_date is None or start_date > common_start_date:
                common_start_date = start_date
                print(common_start_date)

        plt.figure(figsize=(10, 6)) 
        for ticker in tickers:
            stock_data = self.get_historical_data(ticker)
            stock_data = stock_data[stock_data['Date'] >= common_start_date]
            if normalize:
                stock_data['Adj Close'] = stock_data['Adj Close'] / stock_data['Adj Close'].iloc[0]
            sns.lineplot(x='Date', y='Adj Close', data=stock_data, label=ticker)
        plt.title('Historical Stock Prices')
        plt.xlabel('Date')
        plt.ylabel('Adj Close Price')
        plt.legend()
        plt.show()



def sequential_split_by_ticker(data, train_fraction=0.8):
    # Assuming 'Ticker' is the column that contains the ticker names
    tickers = data['Ticker'].unique()

    train_dfs = []
    test_dfs = []

    for ticker in tickers:
        ticker_data = data[data['Ticker'] == ticker]
        train_size = int(len(ticker_data) * train_fraction)
        train, test = ticker_data.iloc[:train_size], ticker_data.iloc[train_size:]
        train_dfs.append(train)
        test_dfs.append(test)

    train_combined = pd.concat(train_dfs)
    test_combined = pd.concat(test_dfs)

    return train_combined, test_combined
