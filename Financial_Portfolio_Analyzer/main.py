import streamlit as st
from src.data_fetcher import StockDataFetcher
from src.portfolio_analyzer import PortfolioAnalyzer
from src.investment_advisor import InvestmentAdvisor
from src.risk_analyzer import RiskAnalyzer
from src.visualization import DataVisualizer

def main():
    st.set_page_config(page_title="Smart Financial Portfolio Analyzer", layout="wide")
    
    st.title("📈 Smart Financial Portfolio Analyzer")
    st.write("Your intelligent investment companion")
    
    # Initialize components
    data_fetcher = StockDataFetcher()
    portfolio_analyzer = PortfolioAnalyzer()
    investment_advisor = InvestmentAdvisor()
    risk_analyzer = RiskAnalyzer()
    visualizer = DataVisualizer()
    
    # Sidebar for user input
    st.sidebar.header("Portfolio Settings")
    selected_stocks = st.sidebar.multiselect(
        "Select Stocks",
        ["AAPL", "GOOGL", "MSFT", "AMZN", "META", "TSLA"],
        default=["AAPL", "GOOGL"]
    )
    
    investment_amount = st.sidebar.number_input(
        "Investment Amount ($)",
        min_value=1000,
        max_value=1000000,
        value=10000,
        step=1000
    )
    
    # Main content
    if selected_stocks:
        # Fetch and display stock data
        stock_data = data_fetcher.fetch_stock_data(selected_stocks)
        
        # Create tabs for different analyses
        tab1, tab2, tab3, tab4 = st.tabs(["Portfolio Analysis", "Investment Advice", "Risk Analysis", "Market Trends"])
        
        with tab1:
            st.header("Portfolio Analysis")
            portfolio_stats = portfolio_analyzer.analyze_portfolio(stock_data, investment_amount)
            visualizer.plot_portfolio_performance(portfolio_stats)
            
        with tab2:
            st.header("Investment Recommendations")
            recommendations = investment_advisor.get_recommendations(stock_data)
            visualizer.display_recommendations(recommendations)
            
        with tab3:
            st.header("Risk Analysis")
            risk_metrics = risk_analyzer.analyze_risk(stock_data)
            visualizer.plot_risk_metrics(risk_metrics)
            
        with tab4:
            st.header("Market Trends")
            market_trends = data_fetcher.fetch_market_trends(selected_stocks)
            visualizer.plot_market_trends(market_trends)

if __name__ == "__main__":
    main() 