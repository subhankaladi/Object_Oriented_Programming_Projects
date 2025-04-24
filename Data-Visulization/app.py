import streamlit as st
import pandas as pd
# import numpy as np
import plotly.express as px
from abc import ABC, abstractmethod

# Abstract Base Class (Abstraction)
class DataVisualizer(ABC):
    @abstractmethod
    def visualize(self, data):
        pass

# Concrete Classes (Inheritance)
class BarChartVisualizer(DataVisualizer):
    def visualize(self, data):
        fig = px.bar(data, x='Category', y='Value', title='Bar Chart Visualization')
        st.plotly_chart(fig)

class PieChartVisualizer(DataVisualizer):
    def visualize(self, data):
        fig = px.pie(data, values='Value', names='Category', title='Pie Chart Visualization')
        st.plotly_chart(fig)

# Encapsulation Example
class DataManager:
    def __init__(self):
        self._data = None  # Private attribute
    
    def load_data(self):
        # Sample data
        self._data = pd.DataFrame({
            'Category': ['A', 'B', 'C', 'D'],
            'Value': [10, 20, 30, 40]
        })
    
    def get_data(self):
        return self._data

# Polymorphism Example
class Dashboard:
    def __init__(self):
        self.data_manager = DataManager()
        self.visualizers = {
            'Bar Chart': BarChartVisualizer(),
            'Pie Chart': PieChartVisualizer()
        }
    
    def run(self):
        st.title("Interactive Data Dashboard")
        
        # Sidebar for user input
        st.sidebar.header("Dashboard Controls")
        chart_type = st.sidebar.selectbox(
            "Select Chart Type",
            list(self.visualizers.keys())
        )
        
        # Load data
        self.data_manager.load_data()
        data = self.data_manager.get_data()
        
        # Display data
        st.subheader("Data Preview")
        st.dataframe(data)
        
        # Visualize data based on user selection
        st.subheader("Data Visualization")
        self.visualizers[chart_type].visualize(data)
        
        # Additional interactive features
        st.subheader("Data Analysis")
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("Total Value", data['Value'].sum())
        
        with col2:
            st.metric("Average Value", data['Value'].mean())

# Main function
def main():
    dashboard = Dashboard()
    dashboard.run()

if __name__ == "__main__":
    main() 