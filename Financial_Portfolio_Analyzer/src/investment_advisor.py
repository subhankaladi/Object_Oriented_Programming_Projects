# import numpy as np
# import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

class InvestmentAdvisor:
    def __init__(self):
        self.scaler = StandardScaler()
        self.kmeans = KMeans(n_clusters=3, random_state=42)
    
    def get_recommendations(self, stock_data):
        """Generate investment recommendations based on stock data"""
        recommendations = {}
        
        for symbol, data in stock_data.items():
            if data.empty:
                continue
                
            # Calculate technical indicators
            data['SMA_20'] = data['Close'].rolling(window=20).mean()
            data['SMA_50'] = data['Close'].rolling(window=50).mean()
            data['RSI'] = self._calculate_rsi(data['Close'])
            
            # Get latest values
            latest = data.iloc[-1]
            prev = data.iloc[-2]
            
            # Generate recommendation
            recommendation = {
                'symbol': symbol,
                'current_price': latest['Close'],
                'price_change': latest['Close'] - prev['Close'],
                'price_change_pct': (latest['Close'] - prev['Close']) / prev['Close'] * 100,
                'trend': self._analyze_trend(latest, prev),
                'rsi_signal': self._analyze_rsi(latest['RSI']),
                'moving_average_signal': self._analyze_moving_averages(latest),
                'overall_sentiment': self._calculate_sentiment(latest, prev)
            }
            
            recommendations[symbol] = recommendation
        
        return recommendations
    
    def _calculate_rsi(self, prices, period=14):
        """Calculate Relative Strength Index"""
        delta = prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        return 100 - (100 / (1 + rs))
    
    def _analyze_trend(self, latest, prev):
        """Analyze price trend"""
        if latest['Close'] > latest['SMA_20'] and latest['SMA_20'] > latest['SMA_50']:
            return "Strong Uptrend"
        elif latest['Close'] < latest['SMA_20'] and latest['SMA_20'] < latest['SMA_50']:
            return "Strong Downtrend"
        elif latest['Close'] > latest['SMA_20']:
            return "Moderate Uptrend"
        elif latest['Close'] < latest['SMA_20']:
            return "Moderate Downtrend"
        else:
            return "Sideways"
    
    def _analyze_rsi(self, rsi):
        """Analyze RSI signal"""
        if rsi > 70:
            return "Overbought"
        elif rsi < 30:
            return "Oversold"
        else:
            return "Neutral"
    
    def _analyze_moving_averages(self, latest):
        """Analyze moving average signals"""
        if latest['Close'] > latest['SMA_20'] and latest['SMA_20'] > latest['SMA_50']:
            return "Bullish"
        elif latest['Close'] < latest['SMA_20'] and latest['SMA_20'] < latest['SMA_50']:
            return "Bearish"
        else:
            return "Neutral"
    
    def _calculate_sentiment(self, latest, prev):
        """Calculate overall sentiment score"""
        sentiment_score = 0
        
        # Price momentum
        if latest['Close'] > prev['Close']:
            sentiment_score += 1
        else:
            sentiment_score -= 1
            
        # RSI sentiment
        if latest['RSI'] > 70:
            sentiment_score -= 1
        elif latest['RSI'] < 30:
            sentiment_score += 1
            
        # Moving average sentiment
        if latest['Close'] > latest['SMA_20']:
            sentiment_score += 1
        if latest['Close'] > latest['SMA_50']:
            sentiment_score += 1
            
        # Convert score to sentiment
        if sentiment_score >= 2:
            return "Strong Buy"
        elif sentiment_score == 1:
            return "Buy"
        elif sentiment_score == 0:
            return "Hold"
        elif sentiment_score == -1:
            return "Sell"
        else:
            return "Strong Sell" 