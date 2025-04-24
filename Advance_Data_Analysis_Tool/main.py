import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime, timedelta
from abc import ABC, abstractmethod
from typing import List, Dict, Optional


# Abstraction
class DataSource(ABC):
    @abstractmethod
    def load_data(self) -> pd.DataFrame:
        pass

# Inheritance
class CSVDataSource(DataSource):
    def __init__(self, file_path: str):
        self.file_path = file_path
    
    def load_data(self) -> pd.DataFrame:
        return pd.read_csv(self.file_path)

# Inheritance
class APIDataSource(DataSource):
    def __init__(self, api_url: str):
        self.api_url = api_url
    
    def load_data(self) -> pd.DataFrame:
        # Simulating API call
        dates = pd.date_range(end=datetime.today(), periods=100).to_pydatetime().tolist()
        data = {
            'date': dates,
            'value': np.random.randn(100).cumsum(),
            'category': np.random.choice(['A', 'B', 'C'], 100)
        }
        return pd.DataFrame(data)

# Encapsulation
class DataAnalyzer:
    def __init__(self, data_source: DataSource):
        self.data = data_source.load_data()
        self._clean_data()  # private method for encapsulation
    
    def _clean_data(self):
        if 'date' in self.data.columns:
            self.data['date'] = pd.to_datetime(self.data['date'])
            self.data = self.data.sort_values('date')
    
    def get_summary_stats(self) -> Dict:
        numeric_cols = self.data.select_dtypes(include=np.number).columns
        return {
            col: {
                'mean': self.data[col].mean(),
                'median': self.data[col].median(),
                'min': self.data[col].min(),
                'max': self.data[col].max()
            }
            for col in numeric_cols
        }
    
    def filter_by_date(self, start_date: datetime, end_date: datetime) -> pd.DataFrame:
        if 'date' not in self.data.columns:
            return self.data
        start_date = pd.to_datetime(start_date)
        end_date = pd.to_datetime(end_date)
        return self.data[(self.data['date'] >= start_date) & (self.data['date'] <= end_date)]
    
    def plot_time_series(self, y_column: str, category_column: Optional[str] = None):
        if 'date' not in self.data.columns:
            st.warning("No date column found for time series plot")
            return
        
        fig = px.line(
            self.data, 
            x='date', 
            y=y_column,
            color=category_column,
            title=f"Time Series of {y_column}"
        )
        st.plotly_chart(fig)
    
    def plot_distribution(self, column: str):
        fig = px.histogram(
            self.data,
            x=column,
            title=f"Distribution of {column}"
        )
        st.plotly_chart(fig)

# Encapsulation
class Dashboard:
    def __init__(self, analyzer: DataAnalyzer):
        self.analyzer = analyzer
    
    def render(self):
        st.title("Advanced Data Analysis Dashboard")
        
        # Sidebar controls
        st.sidebar.header("Controls")
        show_summary = st.sidebar.checkbox("Show Summary Statistics", True)
        
        if 'date' in self.analyzer.data.columns:
            min_date = self.analyzer.data['date'].min().to_pydatetime()
            max_date = self.analyzer.data['date'].max().to_pydatetime()
            date_range = st.sidebar.date_input(
                "Date Range",
                value=(min_date, max_date),
                min_value=min_date,
                max_value=max_date
            )
            
            if len(date_range) == 2:
                filtered_data = self.analyzer.filter_by_date(date_range[0], date_range[1])
            else:
                filtered_data = self.analyzer.data
        else:
            filtered_data = self.analyzer.data
        
        # Main content
        if show_summary:
            st.header("Summary Statistics")
            stats = self.analyzer.get_summary_stats()
            for col, values in stats.items():
                st.subheader(col)
                cols = st.columns(4)
                cols[0].metric("Mean", f"{values['mean']:.2f}")
                cols[1].metric("Median", f"{values['median']:.2f}")
                cols[2].metric("Min", f"{values['min']:.2f}")
                cols[3].metric("Max", f"{values['max']:.2f}")
        
        st.header("Data Visualization")
        
        numeric_cols = filtered_data.select_dtypes(include=np.number).columns
        if len(numeric_cols) > 0:
            selected_column = st.selectbox("Select column for visualization", numeric_cols)
            
            if 'date' in filtered_data.columns:
                category_cols = [None] + list(filtered_data.select_dtypes(exclude=np.number).columns)
                selected_category = st.selectbox("Select category (optional)", category_cols)
                
                tab1, tab2 = st.tabs(["Time Series", "Distribution"])
                
                with tab1:
                    self.analyzer.plot_time_series(selected_column, selected_category)
                
                with tab2:
                    self.analyzer.plot_distribution(selected_column)
            else:
                self.analyzer.plot_distribution(selected_column)
        
        st.header("Raw Data")
        st.dataframe(filtered_data)

# Polymorphism
# Different data sources (CSVDataSource, APIDataSource) use same `load_data()` method differently
if __name__ == "__main__":
    data_source = APIDataSource("https://api.example.com/data")
    analyzer = DataAnalyzer(data_source)
    dashboard = Dashboard(analyzer)
    dashboard.render()
