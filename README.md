# Linear Regression Pairs Trading System

## Overview

This project is a **Linear Regression Pairs Trading System** designed using **Streamlit**. It facilitates traders in identifying trading pairs based on linear regression analysis and performs statistical tests to evaluate the pairs' potential profitability. The system uses **Upstox API** to fetch historical stock data and processes it to generate trading signals.

## Features

1. **API Integration**: Connect to Upstox API to retrieve historical stock data.
2. **Data Selection**: Choose indices such as Nifty 50, Nifty Auto, Nifty Bank, and Nifty IT.
3. **Data Processing**: Convert JSON data to CSV and compile the data.
4. **Linear Regression Analysis**: Perform linear regression and error score calculation.
5. **ADF Test**: Conduct Augmented Dickey-Fuller (ADF) test for stationarity.
6. **Interactive Dashboard**: Filter and sort results using Streamlit’s interactive widgets.

## Setup and Usage

### Step-by-Step Guide

1. **API Credentials**:

   - Enter your **API Key** and **Secret Key**.
   - Use the provided URL to authenticate and obtain an **Authentication Key**.

2. **Date Input**:

   - Enter the **From Date** and **To Date** for the data you wish to analyze.

3. **Index Selection**:

   - Select the indices you are interested in from Nifty 50, Nifty Auto, Nifty Bank, and Nifty IT.

4. **Data Retrieval**:

   - The system fetches the data for the selected indices, converts it from JSON to CSV, and saves it locally.

5. **Data Compilation**:

   - The collected data is compiled into a dataframe, containing the closing prices of all selected stocks.

6. **Pair Generation**:

   - Generate all possible pairs of stocks from the compiled data.

7. **Linear Regression Analysis**:

   - Perform linear regression on each pair and calculate the error ratios.

8. **Best Error Pairs Selection**:

   - Select pairs with the lowest error ratios for further analysis.

9. **ADF Test and Statistical Analysis**:

   - Conduct the ADF test to check for stationarity.
   - Compute the slope, intercept, standard error, and z-scores for the selected pairs.

10. **Interactive Dashboard**:
    - Use Streamlit’s sidebar to filter and sort the results based on various criteria.
    - View the results in a dynamic dataframe.

## Key Functions

### 1. `get_data(file_name, symbol, to_date, from_date)`

Fetches historical data from Upstox API and converts JSON response to CSV format.

### 2. `data_collection(file_data)`

Compiles data from multiple CSV files into a single dataframe.

### 3. `create_pairs(file_data, compiled_data)`

Generates all possible pairs of stocks from the compiled data.

### 4. `lr_and_error_scores(y, x, compiled_data)`

Performs linear regression on each pair and calculates the error ratio.

### 5. `best_error_pairs_data(file_data, compiled_data, pairs_data)`

Selects pairs with the lowest error ratios for further analysis.

### 6. `lr_adf_data(y, x, compiled_data)`

Conducts the ADF test and computes relevant statistical metrics for each pair.

### 7. `compute_lr_values_and_adf_values(best_error_pairs, compiled_data)`

Aggregates the results of linear regression and ADF test into a comprehensive dataframe.

### 8. `lr_pairs_trading_system(path)`

Main function that orchestrates the entire process and returns the final dataframe for display.
