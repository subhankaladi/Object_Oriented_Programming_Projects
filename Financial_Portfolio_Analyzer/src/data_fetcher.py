import yfinance as yf
# import pandas as pd
from datetime import datetime, timedelta

class StockDataFetcher:
    def __init__(self):
        self.cache = {}
    
    def fetch_stock_data(self, symbols):
        """Fetch historical stock data for given symbols"""
        end_date = datetime.now()
        start_date = end_date - timedelta(days=365)
        
        data = {}
        for symbol in symbols:
            if symbol not in self.cache:
                try:
                    stock = yf.Ticker(symbol)
                    hist = stock.history(start=start_date, end=end_date)
                    self.cache[symbol] = hist
                except Exception as e:
                    print(f"Error fetching data for {symbol}: {str(e)}")
                    continue
            
            data[symbol] = self.cache[symbol]
        
        return data
    
    def fetch_market_trends(self, symbols):
        """Fetch market trends and indicators"""
        trends = {}
        for symbol in symbols:
            try:
                stock = yf.Ticker(symbol)
                info = stock.info
                trends[symbol] = {
                    'sector': info.get('sector', 'N/A'),
                    'industry': info.get('industry', 'N/A'),
                    'market_cap': info.get('marketCap', 0),
                    'pe_ratio': info.get('trailingPE', 0),
                    'dividend_yield': info.get('dividendYield', 0)
                }
            except Exception as e:
                print(f"Error fetching trends for {symbol}: {str(e)}")
                continue
        
        return trends 