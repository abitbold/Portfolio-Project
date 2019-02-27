## file name : func.py
## 
## team member:
##      Arjun Alagappan
##      David Abitbol
##      Cody Cao
##      Lily li
##      Shanshan Liu
##      Kurtis Lee
##
## This file contains helper functions for the the portfolio class
## This file imports: yahoo.py
## This file is imported by: mainmenu.py, Portfolio.py, options_module.py

import pandas as pd
from urllib.request import urlopen
from bs4 import BeautifulSoup
import datetime
import numpy as np
import matplotlib.pyplot as plt
from yahoo import *

def get_dividend(ticker):
    df = get_stats_data(ticker)
    div = df['Forward Annual Dividend Yield'].values[0]
    if div is np.nan:
        return 0
    return div

def check_date(dt='today', name='Date', string=True, fmt = '%Y-%m-%d'):
    #Check if date are pandas compatible dates
    #Return string of the date by default, specify string=False to get the pandas date  object
    #Name is used to raise to personalize the error.
    #return current date, if not date specified
    if dt == 'today':
        dt = pd.to_datetime('today')
    elif dt=='last_week':
        dt = pd.to_datetime('today') - datetime.timedelta(days=7)
    else:
        try:
            dt = pd.to_datetime(dt)
        except:
            raise Exception(name + ' was not a correct date format. Input '
                        'it as padas compatible datetime.\n'\
                        'The value was: {}'.format(dt))
    if string : return dt.strftime(fmt)
    else: return dt

def get_rates_yearly(year):
    Year = str(year) # will eventually depend on user request

    s1 = 'https://www.treasury.gov/resource-center/data-chart-center/'
    s2 = 'interest-rates/Pages/TextView.aspx?data=yieldYear&year='
    URL = s1 + s2 + Year
    html = urlopen(URL)

    bsyc = BeautifulSoup(html.read(), "lxml")


    tc_table_list = bsyc.findAll('table', { "class" : "t-chart" })

    tc_table = tc_table_list[0]

    daily_yield_curves = []

    for c in tc_table.children:
        new = []
        for r in c.children:
            content = r.contents[0]
            if content  == '2 mo':
                continue
            
            if r.name == "th":
                new += [content]
            else:
                # get rid of the NA's for the 2-mo rate
                if "N/A" not in content:
                    if "/" not in content:
                        new += [float(content)]
                    else:
                        new += [content]
                    
    # get rid of non-NA 2-mo rate
        if len(new) > 12:
            new = new[0:2] + new[3:]
        
        daily_yield_curves.append(new)
    labels = [x.replace(' ', '') for x in daily_yield_curves[0][1:]]
    inter_df = pd.DataFrame(daily_yield_curves)
    
    dates = pd.to_datetime(inter_df.iloc[1:,0].values)
    
    return pd.DataFrame(inter_df.iloc[1:,1:].values,\
                        index = dates, columns = labels)
    
def validate(date_text):
    try:
        datetime.datetime.strptime(date_text, '%Y-%m-%d')
    except ValueError:
        raise ValueError("Incorrect data format, should be YYYY-MM-DD")


def get_rates(start, end = 'today'):
    # 11:08 pm
    start = check_date(start, string = False)
    end = check_date(end, string = False)
    endyear = end.year
    startyear = start.year
    
    df_final = get_rates_yearly(startyear)
    
    for i in range(startyear+1, endyear + 1):
        df_final = pd.concat([df_final, get_rates_yearly(i)])
    df_final = df_final.sort_index()
    return df_final[(df_final.index >= start) & (df_final.index <= end)]

def compute_returns(ts, log = False):
    # 11:07pm
    idxs = ts.index[1:]
    print("Computing returns.")
    if ts.ndim == 1:
        if log:
            return np.log(np.diff(ts))
        else:
            ret = pd.Series((ts[1:].values/ts[:-1].values - 1), index = idxs)
            ret.name = ts.name
            return ret
    if log:
        return np.log(np.diff(ts, axis = 0))
    else:
        return pd.Series((ts.iloc[1:,0].values/ts.iloc[:-1,0].values) - 1, index = idxs)
    
def benchmark_help(ts1, ts2, plot = False, sigmas = False, 
    normalize = False):
    # only take in series
    # 11:07 PM
    if normalize:
        ts1 = (ts1-ts1.mean())/ts1.std()
        ts2 = (ts2-ts2.mean())/ts2.std()
    xs1 = ts1.index
    xs2 = ts2.index
    idx = xs1.intersection(xs2)
    
    if len(xs1) > len(xs2):
        print("Time series are of different length.\n")
        m_idx = idx.min()
        m_idx_p = ts1.loc[m_idx]
        ts1 = 100*ts1/ts1.iloc[0]
        ts2 = m_idx_p*ts2/ts2.iloc[0]
    elif len(xs1) < len(xs2):
        print("Time series are of different length.\n")
        m_idx = idx.min()
        m_idx_p = ts2.loc[m_idx]
        ts2 = 100*ts2/ts2.iloc[0]
        ts1 = m_idx_p*ts1/ts1.iloc[0] 
    else:
        ts1 = 100*ts1/ts1.iloc[0]
        ts2 = 100*ts2/ts2.iloc[0]
    
    ts1_n = ts1.loc[idx]
    ts2_n = ts2.loc[idx]
    ts1_n = 100*ts1_n/ts1_n.iloc[0]
    ts2_n = 100*ts2_n/ts2_n.iloc[0]
    
    df = pd.DataFrame({ts1.name: ts1_n, ts2.name: ts2_n}, index = idx)
    
    if plot:
        plt.figure(figsize = (8,6))
        plt.title("Time Series")
        plt.xlabel("Date")
        plt.ylabel("Scaled Price")
        plt.plot(xs1, ts1, c = 'b', label = ts1.name)
        plt.plot(xs2, ts2, c = 'r', label = ts2.name)
        plt.legend()
        plt.show()
    
    corr = df.corr().iloc[0,1]

    if sigmas:
        return (corr, ts1.std()*np.sqrt(250),
            ts2.std()*np.sqrt(250))
    return corr
