import numpy as np
import pandas as pd

class PortfolioAnalyzer:
    def __init__(self):
        self.risk_free_rate = 0.02  # Assuming 2% risk-free rate
    
    def analyze_portfolio(self, stock_data, investment_amount):
        """Analyze portfolio performance and return statistics"""
        portfolio_stats = {}
        
        # Calculate equal weight allocation
        num_stocks = len(stock_data)
        weight = 1.0 / num_stocks
        
        # Calculate returns for each stock
        returns = {}
        for symbol, data in stock_data.items():
            if not data.empty:
                returns[symbol] = data['Close'].pct_change().dropna()
        
        # Calculate portfolio metrics
        portfolio_returns = pd.DataFrame(returns).mean(axis=1)
        portfolio_stats['total_return'] = (portfolio_returns + 1).prod() - 1
        portfolio_stats['annualized_return'] = (1 + portfolio_stats['total_return']) ** (252/len(portfolio_returns)) - 1
        portfolio_stats['volatility'] = portfolio_returns.std() * np.sqrt(252)
        portfolio_stats['sharpe_ratio'] = (portfolio_stats['annualized_return'] - self.risk_free_rate) / portfolio_stats['volatility']
        
        # Calculate individual stock metrics
        stock_metrics = {}
        for symbol, data in stock_data.items():
            if not data.empty:
                stock_metrics[symbol] = {
                    'return': (data['Close'][-1] / data['Close'][0]) - 1,
                    'volatility': data['Close'].pct_change().std() * np.sqrt(252),
                    'allocation': investment_amount * weight
                }
        
        portfolio_stats['stock_metrics'] = stock_metrics
        return portfolio_stats 