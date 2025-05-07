# Smart Financial Portfolio Analyzer

A comprehensive financial portfolio analysis and investment advisory tool built with Python and Streamlit. This application helps investors make informed decisions by providing detailed portfolio analysis, risk assessment, and investment recommendations.

## Features

- **Portfolio Analysis**
  - Performance metrics calculation
  - Portfolio allocation visualization
  - Stock performance comparison
  - Historical returns analysis

- **Investment Recommendations**
  - Technical analysis indicators
  - Trend analysis
  - RSI signals
  - Moving average signals
  - Overall sentiment analysis

- **Risk Analysis**
  - Volatility calculation
  - Value at Risk (VaR)
  - Maximum drawdown
  - Beta calculation
  - Sharpe and Sortino ratios
  - Portfolio diversification metrics

- **Market Trends**
  - Sector distribution
  - Market cap analysis
  - P/E ratio comparison
  - Dividend yield analysis

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/smart-portfolio-analyzer.git
cd smart-portfolio-analyzer
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Run the Streamlit application:
```bash
streamlit run app.py
```

2. Open your web browser and navigate to the URL shown in the terminal (typically http://localhost:8501)

3. Select stocks from the sidebar and set your investment amount

4. Explore different analysis tabs:
   - Portfolio Analysis
   - Investment Advice
   - Risk Analysis
   - Market Trends

## Project Structure

```
smart-portfolio-analyzer/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Project dependencies
├── README.md             # Project documentation
└── src/
    ├── data_fetcher.py   # Stock data fetching module
    ├── portfolio_analyzer.py  # Portfolio analysis module
    ├── investment_advisor.py  # Investment recommendations module
    ├── risk_analyzer.py  # Risk analysis module
    └── visualization.py  # Data visualization module
```

## Dependencies

- streamlit==1.32.0
- pandas==2.2.0
- numpy==1.26.4
- yfinance==0.2.36
- plotly==5.18.0
- scikit-learn==1.4.0
- python-dotenv==1.0.1
- requests==2.31.0

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Disclaimer

This tool is for educational and informational purposes only. It should not be considered as financial advice. Always do your own research and consult with a financial advisor before making investment decisions.
