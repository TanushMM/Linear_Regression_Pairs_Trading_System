import streamlit as st
import urllib.parse
import requests
import pandas as pd
import json
import csv
from statsmodels.tsa.stattools import adfuller
import statistics
import matplotlib.pyplot as plt
import statsmodels.api as sm
import os

st.markdown(
"""
<style>
.label-size-1 {
    font-size: 22px !important;
}
.label-size-2 {
    font-size: 18px !important;
}
.label-size-3 {
    font-size: 14px !important;
}
</style>
""",
unsafe_allow_html=True
)

fresh_start = True
cwd = os.getcwd()

st.title("Linear Regression Pairs Trading System - Developed by Tanush M M")
st.title("Data Accepted only from 01-01-2019 and thereafter")
st.write("")
st.write("")

st.header("Enter Upstox API Credentials")

with st.form(key='api_form'):
    st.markdown('<div class="label-size-1">API Key:</div>', unsafe_allow_html=True)
    apiKey = st.text_input("Enter your API Key", key="apiKey", label_visibility='collapsed')
    st.markdown('<div class="label-size-1">Secret Key:</div>', unsafe_allow_html=True)
    secretKey = st.text_input("Enter your Secret Key", key="secretKey", label_visibility='collapsed')
    submit_api = st.form_submit_button("Submit API Keys")


rurl = urllib.parse.quote('https://127.0.0.1', safe='')
url = f'https://api.upstox.com/v2/login/authorization/dialog?response_type=code&client_id={apiKey}&redirect_uri={rurl}'
st.markdown('<div class="label-size-2">Copy the following, enter it in URL search and press enter</div>', unsafe_allow_html=True)
st.write(url)

st.header("Enter the Authentication Credentials")
form =  st.form(key='auth_form')
form.markdown('<div class="label-size-2">Enter the Authentication Key: </div>', unsafe_allow_html=True)
authKey = form.text_input("Enter your Authentication Key", key="authKey", label_visibility='collapsed')
form.form_submit_button("Submit Authentication Key")

st.header("Enter the Dates")
form =  st.form(key='date_form')
form.markdown('<div class="label-size-2">From Date: </div>', unsafe_allow_html=True)
fromDate = form.text_input("Enter From Date: ", key='fromDate',label_visibility='collapsed')
form.markdown('<div class="label-size-2">To Date: </div>', unsafe_allow_html=True)
toDate = form.text_input("Enter To Date: ", key='toDate',label_visibility='collapsed')
form.form_submit_button("Submit Dates")

st.header("Select the Indices")
form =  st.form(key='index_form', clear_on_submit=True)
n_50 = form.checkbox("Nifty 50")
n_auto = form.checkbox("Nifty Auto")
n_bank = form.checkbox("Nifty Bank")
n_it = form.checkbox("Nifty IT")
form.form_submit_button("Submit")

st.write("")
st.write("")


nifty_50 = pd.read_csv(f"{cwd}/index_data/ind_nifty50list.csv")
nifty_auto = pd.read_csv(f"{cwd}/index_data/ind_niftyautolist.csv")
nifty_bank = pd.read_csv(f"{cwd}/index_data/ind_niftybanklist.csv")
nifty_it = pd.read_csv(f"{cwd}/index_data/ind_niftyitlist.csv")

def print_generator(i):
    def return_file(i):
        if i == 0:
            return nifty_50
        elif i == 1:
            return nifty_auto
        elif i == 2:
            return nifty_bank
        elif i == 3:
            return nifty_it
    data = return_file(i)
    for j in range(data.shape[0]):
        name = data["Symbol"][j]
        isin = "NSE_EQ|" + data["ISIN Code"][j]
        get_data(name, isin, toDate, fromDate)
        
def get_data(file_name, symbol, to_date, from_date):
    def json_to_csv(json_data, csv_filename):
        candles_data = json_data["data"]["candles"]

        with open(csv_filename, mode='w', newline='') as csv_file:
            writer = csv.writer(csv_file)
            
            # Writing header
            writer.writerow(['data__candles__001','data__candles__002','data__candles__003','data__candles__004','data__candles__005','data__candles__006','data__candles__007'])

            # Writing data
            for candle in candles_data:
                writer.writerow(candle)
    
    url = 'https://api.upstox.com/v2/login/authorization/token'
    headers = {
        'accept': 'application/json' ,
        'Api-Version': '2.0' ,
        'Content-Type': 'application/x-www-form-urlencoded' 
    }
    data ={
        'code':authKey,
        'client_id':apiKey,
        'client_secret':secretKey,
        'redirect_uri':'https://127.0.0.1',
        'grant_type':'authorization_code'
    }
    requests.post(url, headers= headers, data=data)

    #Getting Data
    data_url = f"https://api.upstox.com/v2/historical-candle/{symbol}/day/{to_date}/{from_date}"
    payload={}
    headers = {
    'Accept': 'application/json'
    }
    response = requests.request("GET", data_url, headers=headers, data=payload)
    data = response.json()

    #saving into CSV
    data = json.dumps(data)
    data = json.loads(data)
    json_to_csv(data, file_name+".csv")

if n_50:
    print_generator(0)
if n_auto:
    print_generator(1)
if n_bank:
    print_generator(2)
if n_it:
    print_generator(3)
    
    
def get_file_data(directory):
    count = 0
    csv_path = []
    file_names = []
    path = f'{directory}'
    list_of_files = os.listdir(path)
    for file in list_of_files:
        if '.csv' in file:
            file_names.append(file)
            csv_path.append(f'{directory}/{file}')
            count+=1
    return count,file_names,csv_path


def data_collection(file_data):
    count = file_data[0]
    name = file_data[1]
    path = file_data[2]
    compiled_data = {}
    
    for i in range(0,count):
        if i == 0:
            temp_data = pd.read_csv(f'{path[i]}')
            compiled_data["Date"] = list(temp_data['data__candles__001'].values)
            compiled_data[f'{name[i]}'] = list(temp_data['data__candles__005'].values)
        else:
            temp_data = pd.read_csv(f'{path[i]}')
            compiled_data[f'{name[i]}'] = list(temp_data['data__candles__005'].values)
    data = pd.DataFrame(compiled_data)
    return data


def create_pairs(file_data,compiled_data):
    column_count = compiled_data.shape[1]
    pairs = []
    
    for i in range(1,column_count):
        for j in range(i+1,column_count):
            temp_list = []
            temp_list.append(file_data[1][i-1])
            temp_list.append(file_data[1][j-1])
            pairs.append(temp_list)
    length = len(pairs)
    return length,pairs


def lr_and_error_scores(y,x,compiled_data):
    Y = compiled_data[f'{y}']
    X = compiled_data[f'{x}']
    X = sm.add_constant(X)
    model = sm.OLS(Y,X).fit()
    std_error = statistics.stdev(model.resid) # this is the standard deviation of the residuals
    std_error_intercept_and_slope = model.bse # standard error of intercept and slope
    error_ratio = std_error_intercept_and_slope['const'] / std_error
    return error_ratio


def best_error_pairs_data(file_data,compiled_data,pairs_data):
    no_of_pairs = pairs_data[0]
    best_error_pairs = []
    
    for i in range(0, no_of_pairs):
        temp_pair = []
        stock_a = pairs_data[1][i][0]
        stock_b = pairs_data[1][i][1]
        a_b = lr_and_error_scores(stock_a, stock_b, compiled_data)
        b_a = lr_and_error_scores(stock_b, stock_a, compiled_data)
        
        if a_b < b_a:
            temp_pair.append(pairs_data[1][i][0])
            temp_pair.append(pairs_data[1][i][1])
            best_error_pairs.append(temp_pair)
            
        else:
            temp_pair.append(pairs_data[1][i][1])
            temp_pair.append(pairs_data[1][i][0])
            best_error_pairs.append(temp_pair)
    return best_error_pairs


def lr_adf_data(y,x,compiled_data):
    def adf_test(data):
        model = adfuller(data)
        return model[1]
    
    def standard_error_data(model):
        std_err = statistics.stdev(model.resid)
        return std_err
    
    def std_err_intercept(model):
        return model.bse['const']
    
    Y = compiled_data[y]
    X = compiled_data[x]
    X = sm.add_constant(X)
    model = sm.OLS(Y,X).fit()
    slope = model.params[x]
    intercept = model.params['const']
    adf_p_value = adf_test(model.resid)
    standard_error = standard_error_data(model)
    z_score = model.resid[0]/statistics.stdev(model.resid)
    # z_score = today's residual / std dev of residuals 
    standard_error_of_intercept = std_err_intercept(model)
    current_day_residual = model.resid[0]
    return y,x,slope,intercept,standard_error_of_intercept,adf_p_value,z_score,current_day_residual,standard_error

def compute_lr_values_and_adf_values(best_error_pairs,compiled_data):
    length = len(best_error_pairs)
    big_data = []
    
    for i in range(0,length):
        stock_a = best_error_pairs[i][0]
        stock_b = best_error_pairs[i][1]
        lr_adf_data_values = lr_adf_data(stock_a,stock_b, compiled_data)
        big_data.append(lr_adf_data_values)
    return big_data

   
def check_shape(file_data, path): # this is for explicit checking [this program does not use this function]
    for i in range(file_data[0]):
        data = pd.read_csv(f'{path}\\{file_data[1][i]}')
        print(f"{file_data[1][i]} has a shape of {data.shape}") 
     
def lr_pairs_trading_system(path):
    file_data = get_file_data(path)
    compiled_data = data_collection(file_data)
    pairs_data = create_pairs(file_data,compiled_data)
    best_error_pairs = best_error_pairs_data(file_data,compiled_data,pairs_data)
    big_data = compute_lr_values_and_adf_values(best_error_pairs, compiled_data)
    big_data_data_frame = pd.DataFrame(big_data,columns=['Stock_Y','Stock_X','Slope/Beta','Intercept','Standard Error of Intercept','adf_p_value','z_score (Today\'s Residual / standard_error )','Current Day Residual','standard_error (STD DEV of residuals)'])
    return big_data_data_frame


    
raw_data = lr_pairs_trading_system(f"{cwd}")
data = raw_data
form = st.sidebar.form(" ", clear_on_submit=True)
form.markdown('<div class="label-size-1">Filter & Sort</div>', unsafe_allow_html=True)
sort_ascending = form.checkbox("Ascending")
sort_descending = form.checkbox("Descending")
form.form_submit_button("Sumbit")
sort_column = form.selectbox("Select column to sort by:", data.columns)
reset_button = st.sidebar.button("Reset")
st.sidebar.text_area("Temporary Notes", height=300)

if sort_ascending and not sort_descending:
    data = data.sort_values(by=sort_column, ascending=True)
elif sort_descending and not sort_ascending:
    data = data.sort_values(by=sort_column, ascending=False)

if reset_button:
    df = st.dataframe(raw_data)
if not reset_button:
    df = st.dataframe(data) # this will show the first dataframe

