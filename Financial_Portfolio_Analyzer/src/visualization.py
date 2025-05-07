import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np

class DataVisualizer:
    def __init__(self):
        self.color_palette = px.colors.qualitative.Set3
    
    def plot_portfolio_performance(self, portfolio_stats):
        """Create portfolio performance visualization"""
        # Create performance metrics cards
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Return", f"{portfolio_stats['total_return']:.2%}")
        with col2:
            st.metric("Annualized Return", f"{portfolio_stats['annualized_return']:.2%}")
        with col3:
            st.metric("Volatility", f"{portfolio_stats['volatility']:.2%}")
        with col4:
            st.metric("Sharpe Ratio", f"{portfolio_stats['sharpe_ratio']:.2f}")
        
        # Create stock allocation pie chart
        stock_metrics = portfolio_stats['stock_metrics']
        allocation_data = pd.DataFrame([
            {'Stock': symbol, 'Allocation': metrics['allocation']}
            for symbol, metrics in stock_metrics.items()
        ])
        
        fig = px.pie(allocation_data, values='Allocation', names='Stock',
                     title='Portfolio Allocation',
                     color_discrete_sequence=self.color_palette)
        st.plotly_chart(fig)
        
        # Create performance comparison bar chart
        performance_data = pd.DataFrame([
            {'Stock': symbol, 'Return': metrics['return']}
            for symbol, metrics in stock_metrics.items()
        ])
        
        fig = px.bar(performance_data, x='Stock', y='Return',
                     title='Stock Performance Comparison',
                     color='Return',
                     color_continuous_scale='RdYlGn')
        st.plotly_chart(fig)
    
    def display_recommendations(self, recommendations):
        """Display investment recommendations"""
        for symbol, rec in recommendations.items():
            with st.expander(f"{symbol} - {rec['overall_sentiment']}"):
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Current Price", f"${rec['current_price']:.2f}",
                             f"{rec['price_change_pct']:.2f}%")
                with col2:
                    st.metric("Trend", rec['trend'])
                with col3:
                    st.metric("RSI Signal", rec['rsi_signal'])
                
                st.write("Technical Analysis:")
                st.write(f"- Moving Average Signal: {rec['moving_average_signal']}")
                st.write(f"- Overall Sentiment: {rec['overall_sentiment']}")
    
    def plot_risk_metrics(self, risk_metrics):
        """Create risk analysis visualizations"""
        # Create risk metrics for individual stocks
        stock_risks = {symbol: metrics for symbol, metrics in risk_metrics.items() 
                      if symbol != 'portfolio'}
        
        # Create risk comparison bar chart
        risk_data = pd.DataFrame([
            {'Stock': symbol, 'Volatility': metrics['volatility']}
            for symbol, metrics in stock_risks.items()
        ])
        
        fig = px.bar(risk_data, x='Stock', y='Volatility',
                     title='Stock Volatility Comparison',
                     color='Volatility',
                     color_continuous_scale='RdYlGn_r')
        st.plotly_chart(fig)
        
        # Display portfolio-level risk metrics
        if 'portfolio' in risk_metrics:
            st.subheader("Portfolio Risk Analysis")
            
            # Correlation matrix heatmap
            corr_matrix = risk_metrics['portfolio']['correlation_matrix']
            fig = px.imshow(corr_matrix,
                           title='Stock Correlation Matrix',
                           color_continuous_scale='RdYlBu')
            st.plotly_chart(fig)
            
            # Display portfolio metrics
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Portfolio Volatility",
                         f"{risk_metrics['portfolio']['portfolio_volatility']:.2%}")
            with col2:
                st.metric("Diversification Ratio",
                         f"{risk_metrics['portfolio']['diversification_ratio']:.2f}")
    
    def plot_market_trends(self, market_trends):
        """Create market trends visualization"""
        # Create sector distribution
        sector_data = pd.DataFrame([
            {'Stock': symbol, 'Sector': data['sector']}
            for symbol, data in market_trends.items()
        ])
        
        fig = px.pie(sector_data, names='Sector',
                     title='Portfolio Sector Distribution',
                     color_discrete_sequence=self.color_palette)
        st.plotly_chart(fig)
        
        # Create market metrics comparison
        metrics_data = pd.DataFrame([
            {
                'Stock': symbol,
                'Market Cap': data['market_cap'],
                'P/E Ratio': data['pe_ratio'],
                'Dividend Yield': data['dividend_yield']
            }
            for symbol, data in market_trends.items()
        ])
        
        # Display metrics in a table
        st.dataframe(metrics_data.style.format({
            'Market Cap': '${:,.0f}',
            'P/E Ratio': '{:.2f}',
            'Dividend Yield': '{:.2%}'
        })) 