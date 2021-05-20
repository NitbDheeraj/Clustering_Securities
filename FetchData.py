# -*- coding: utf-8 -*-
"""
Created on Thu May 20 17:03:53 2021

@author: dheer
"""
import bs4 as bs
import pandas as pd
import os
import pandas_datareader.data as web
import pickle
import requests
#from dateutil.relativedelta import relativedelta, FR
#import numpy as np

#end_date = pd.Timestamp(pd.to_datetime('today').strftime("%m/%d/%Y"))
#start_date = end_date - relativedelta(years=5)

def save_sp500_tickers():
    resp = requests.get('http://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    soup = bs.BeautifulSoup(resp.text, 'lxml')
    table = soup.find('table', {'class': 'wikitable sortable'})
    tickers = []
    for row in table.findAll('tr')[1:]:
        ticker = row.findAll('td')[0].text[:-1]
        tickers.append(ticker)
    with open("sp500tickers.pickle", "wb") as f:
        pickle.dump(tickers, f)
    return tickers

def get_data_from_yahoo(start_date, end_date, reload_sp500=False):
    if reload_sp500:
        tickers = save_sp500_tickers()
    else:
        with open("sp500tickers.pickle", "rb") as f:
            tickers = pickle.load(f)
    if not os.path.exists('stock_dfs'):
        os.makedirs('stock_dfs')

    start = start_date
    end = end_date
    for ticker in tickers:
        # just in case your connection breaks, we'd like to save our progress!
        ticker = ticker.replace('.', '-')
        if not os.path.exists('stock_dfs/{}.csv'.format(ticker)):
            try:
                df = web.DataReader(ticker, 'yahoo', start, end)
                df.reset_index(inplace=True)
                df.set_index("Date", inplace=True)
                df.to_csv('stock_dfs/{}.csv'.format(ticker))
                print('Create {}'.format(ticker))
            except:
                print('Drop {}'.format(ticker))
                pass
        else:
            print('Already have {}'.format(ticker))

def compile_data():
    with open("sp500tickers.pickle", "rb") as f:
        tickers = pickle.load(f)

    main_df = pd.DataFrame()

    for count, ticker in enumerate(tickers):
        try:
            df = pd.read_csv('stock_dfs/{}.csv'.format(ticker))
            df["Name"] = ticker
            df.set_index('Date', inplace=True)
            df.drop(['Adj Close'], axis = 1)

            if main_df.empty:
                main_df = df
            else:
                main_df = main_df.append(df)
        except:
            pass

        if count % 100 == 0:
            print(count)

    print(main_df.head())
    main_df.to_csv('all_stocks_5yr.csv')
    

#get_data_from_yahoo(start_date, end_date, reload_sp500=True)
#compile_data()