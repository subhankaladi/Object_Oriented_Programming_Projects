import numpy as np
import pandas as pd
from scipy import stats

class RiskAnalyzer:
    def __init__(self):
        self.confidence_level = 0.95
    
    def analyze_risk(self, stock_data):
        """Analyze risk metrics for the portfolio"""
        risk_metrics = {}
        
        for symbol, data in stock_data.items():
            if data.empty:
                continue
                
            returns = data['Close'].pct_change().dropna()
            
            # Calculate risk metrics
            risk_metrics[symbol] = {
                'volatility': self._calculate_volatility(returns),
                'var_95': self._calculate_var(returns),
                'max_drawdown': self._calculate_max_drawdown(data['Close']),
                'beta': self._calculate_beta(returns),
                'sharpe_ratio': self._calculate_sharpe_ratio(returns),
                'sortino_ratio': self._calculate_sortino_ratio(returns)
            }
        
        # Calculate portfolio-level risk metrics
        portfolio_returns = pd.DataFrame({symbol: data['Close'].pct_change().dropna() 
                                        for symbol, data in stock_data.items() if not data.empty})
        
        if not portfolio_returns.empty:
            risk_metrics['portfolio'] = {
                'correlation_matrix': portfolio_returns.corr(),
                'portfolio_volatility': self._calculate_portfolio_volatility(portfolio_returns),
                'diversification_ratio': self._calculate_diversification_ratio(portfolio_returns)
            }
        
        return risk_metrics
    
    def _calculate_volatility(self, returns):
        """Calculate annualized volatility"""
        return returns.std() * np.sqrt(252)
    
    def _calculate_var(self, returns):
        """Calculate Value at Risk at 95% confidence level"""
        return np.percentile(returns, 5)
    
    def _calculate_max_drawdown(self, prices):
        """Calculate maximum drawdown"""
        peak = prices.expanding(min_periods=1).max()
        drawdown = (prices - peak) / peak
        return drawdown.min()
    
    def _calculate_beta(self, returns):
        """Calculate beta relative to market (using S&P 500 as proxy)"""
        # In a real implementation, you would fetch S&P 500 data
        # For this example, we'll use a simplified approach
        market_returns = returns.rolling(window=20).mean()  # Simplified market proxy
        covariance = returns.cov(market_returns)
        market_variance = market_returns.var()
        return covariance / market_variance if market_variance != 0 else 1.0
    
    def _calculate_sharpe_ratio(self, returns, risk_free_rate=0.02):
        """Calculate Sharpe ratio"""
        excess_returns = returns - risk_free_rate/252
        return np.sqrt(252) * excess_returns.mean() / returns.std()
    
    def _calculate_sortino_ratio(self, returns, risk_free_rate=0.02):
        """Calculate Sortino ratio"""
        excess_returns = returns - risk_free_rate/252
        downside_returns = returns[returns < 0]
        downside_std = np.sqrt(np.mean(downside_returns**2))
        return np.sqrt(252) * excess_returns.mean() / downside_std if downside_std != 0 else 0
    
    def _calculate_portfolio_volatility(self, returns):
        """Calculate portfolio volatility"""
        return returns.mean(axis=1).std() * np.sqrt(252)
    
    def _calculate_diversification_ratio(self, returns):
        """Calculate diversification ratio"""
        # Simplified implementation
        avg_correlation = returns.corr().mean().mean()
        return 1 / (1 + avg_correlation) 