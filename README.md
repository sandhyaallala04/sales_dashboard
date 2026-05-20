# Interactive Sales Analytics Dashboard

This is a Streamlit-based sales analytics dashboard that allows users to upload a CSV dataset and automatically generate business insights.

## Features

- CSV dataset upload
- Dataset preview
- Total sales, total profit, and total orders
- Monthly sales trend
- Category-wise sales
- Region-wise sales
- Top 10 products by sales
- Interactive Plotly visualizations

## Tech Stack

- Python
- Streamlit
- Pandas
- Plotly

## Required Dataset Columns

- Order ID
- Order Date
- Region
- Category
- Product Name
- Sales
- Profit

## How to Run

```bash
pip install -r requirements.txt
streamlit run app.py