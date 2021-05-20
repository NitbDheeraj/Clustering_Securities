# -*- coding: utf-8 -*-
"""
Created on Thu May 20 18:10:20 2021

@author: dheer
"""
import numpy as np
import pandas as pd
from dateutil.relativedelta import relativedelta
import FetchData
#import getinputvectors
import AutoEncoder
import PlotData
from sklearn.cluster import KMeans

class Main():
    
    def GetData():
        end_date = pd.Timestamp(pd.to_datetime('today').strftime("%m/%d/%Y"))
        start_date = end_date - relativedelta(years=5)
        FetchData.get_data_from_yahoo(start_date, end_date, reload_sp500=True)
        FetchData.compile_data()
        
    def KMeansClustering():
        #load and prepare data for K-means
        encodedData = np.array(pd.read_csv('encoded_with_labels.txt', sep = ',', header=None))
        encoded_values = encodedData[:,2:4]
        
        ns = [2, 5, 20]
        
        for n in ns:

            #apply kmeans clustering and plot
            kmeans = KMeans(n_clusters=n)
            kmeans.fit(encoded_values)
            y_kmeans = kmeans.predict(encoded_values)
            #centers = kmeans.cluster_centers_   
            PlotData.PlotKmeans(encoded_values,y_kmeans, n )
            
    def GMMClustering():
        data = pd.read_csv('encoded_with_labels.txt')

        data.columns= ['company', 'year', 'x', 'y']

        company = data['company'].tolist()
        year = data['year'].tolist()

        l = [company[i] + ', ' + str(year[i]) for i in range(len(company))]
        x = data['x'].tolist()
        y = data['y'].tolist()

        bigtech_companies = ['AMZN', 'GOOGL', 'AAPL', 'ORCL', 'MSFT', 'FB', 'IBM']
        data_justtech = data.loc[data['company'].isin(bigtech_companies)]

        company_bigtech = data_justtech['company'].tolist()
        year_bigtech = data_justtech['year'].tolist()

        l_bt = [company_bigtech[i] + ', ' + str(year_bigtech[i]) for i in range(len(company_bigtech))]
        x_bt = data_justtech['x'].tolist()
        y_bt = data_justtech['y'].tolist()
        
        PlotData.plot_gmm(x,y,l,'allstocks')
        PlotData.plot_gmm(x_bt,y_bt,l_bt,'bigtech')


    def inputvec(data, company, year):
        
        '''
        takes the relevant info from data (company is a string, year is an int)
        generates a 4D vector Q_{i} for the ith quarter
        
        Q_{i} elements:
            v_{i}: standard deviation of opening price
            s_{i}: mean(high price - low price)
            n_{y,i}: mean(traded shares)
            h_{y,i}: mean(high price)
        
        output is concatenation of company, year, Q_{1}, Q_{2}, Q_{3}, and Q_{4}
        '''
    
        #filters out by the company and relevant year
        filter1 = data.loc[data['Name'] == company]
        filter2 = filter1.loc[filter1['Date'].str.contains(str(year))]
        
        def Q(i):
            
            if i == 1:
                
                month_strs = ['-01-', '-02-', '-03-']
                
            if i == 2:
                
                month_strs = ['-04-', '-05-', '-06-']
                
            if i == 3:
                
                month_strs = ['-07-', '-08-', '-09-']
                
            if i == 4:
                
                month_strs = ['-10-', '-11-', '-12-']
            
            filterquarter = filter2
            months = [filterquarter.loc[filterquarter['Date'].str.contains(month_str)] for month_str in month_strs]
        
            opens = [month['Open'].tolist() for month in months] 
            opens = [j for i in opens for j in i] #concatenates months
            
            highs = [month['High'].tolist() for month in months]
            highs = [j for i in highs for j in i]
            
            lows = [month['Low'].tolist() for month in months]
            lows = [j for i in lows for j in i]
            
            volumes = [month['Volume'].tolist() for month in months]
            volumes = [j for i in volumes for j in i]
            
            spreads = [highs[i] - lows[i] for i in range(len(highs))]
            
            #ignores NaNs
            
            if len(opens) != 0: #checking if there's actually any data
                mo, mh, ml, mv, ms = max(opens), max(highs), max(lows), max(volumes), max(spreads)
                try:
                    opens = [opening/mo for opening in opens]
                    highs = [high/mh for high in highs]
                    lows = [low/ml for low in lows]
                    volumes = [volume/mv for volume in volumes]
                    spreads = [spread/ms for spread in spreads]
    
                except:
                    pass
                v, s = np.nanstd(opens), np.nanmean(spreads)
                n, h = np.nanmean(volumes), np.nanmean(highs)
        
            else:
                v, s, n, h = 'nan', 'nan', 'nan', 'nan'
        
            return [v, s, n, h]
    
        return [company, year] + Q(1) + Q(2) + Q(3) + Q(4)    
    

    if __name__ == '__main__':
        #GetData()
        
        raw = pd.read_csv('all_stocks_10yr.csv')
        data = raw.loc[:, ('Date','Open','High','Low','Close','Volume','Name')]
        
        companies = data.Name.unique()
        years = ['2016', '2017','2018', '2019', '2020', '2021']

        #list comprehension to get input vectors for each company in each year
        inputvecs = [inputvec(data, company, year) for company in companies for year in years]

        with open('inputvector_table.txt', 'w+') as f:
            for item in inputvecs:
                if 'nan' not in tuple(item): #doesn't write in vectors with insufficient data
                    f.write('%s %s %.02f %.02f %.02f %.02f %.02f %.02f %.02f %.02f %.02f %.02f %.02f %.02f %.02f %.02f %.02f %.02f\n'%(tuple(item)))
                    
        AutoEncoder.PerformOperation()
        
        KMeansClustering()
        GMMClustering()

        
