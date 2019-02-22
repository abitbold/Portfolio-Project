from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np


def get_financial_data(stock):
    """Return a daframe with all of the financials for the company. 
    Includes 4 years worth of Financial"""

    dfL = []
    urls = ['https://finance.yahoo.com/quote/'+stock+'/financials?p='+stock, 
            'https://finance.yahoo.com/quote/'+stock+'/balance-sheet?p='+stock,
            'https://finance.yahoo.com/quote/'+stock+'/cash-flow?p='+stock]
    bs = []
    for url in urls:
        html = urlopen(url)
        bsyc = BeautifulSoup(html.read(), "lxml")
        tables = bsyc.findAll('table')[0]
        T=[]
        row_names = []
        col_names = []

        i=0
        for table in tables:
            for r in table.children:
                temp=[]
                j=0
                for c in r.children:
                    for data in c.children:
                        if data == "-":
                            temp.append(np.nan)
                        else:
                            for data2 in data.children:
                                if i==0 :
                                    col_names.append(data2)
                                else:
                                    if j==0:
                                        rowTemp = data2
                                        j+=1
                                    else:
                                        temp.append(int(data2.replace(',', ''))*1000)
                i+=1
                if len(temp)>1:
                    T.append(temp)
                    row_names.append(rowTemp)
            break
 
        col_names = pd.to_datetime(col_names[1:])
        df = pd.DataFrame(T, index=row_names, columns = col_names )
        #df = df.transpose()
        dfL.append(df)
        bs.append(bsyc.contents)
    df = pd.concat(dfL, axis=0)
    return df


def get_stats_data(stock):
    "Return statistics on the company"""
    html = urlopen('https://finance.yahoo.com/quote/'+stock+'/key-statistics?p='+stock)
    bsyc = BeautifulSoup(html.read(), "lxml")
    tables = bsyc.findAll('table')
    stats = []
    names = []
    for table in tables:
        for r in table.children:
            #temp = []
            #i=0
            for c in r.children:
                j=0
                for data in c.children:
                    for data2 in data.children:
                        if j ==0:
                            try:
                                names.append(data2.contents[0])
                            except:
                                pass
                            break
                        elif j==1:
                            if "N/A" in data2:
                                stats.append(np.nan)
                            else:
                                dt = data2
                                try:
                                    dt = float(dt)
                                    if ("%" or "Rate") in names[-1]:
                                        print(names[-1])
                                        print(dt)
                                        dt = dt/100
                                except:
                                    try:
                                        if "B" in dt:
                                            dt = float(dt.split("B")[0])*1000000000
                                        elif "%" in dt:
                                            dt = float(dt.split("%")[0])/100
                                        elif "/" in dt:
                                            dt = dt.split("/")
                                            dt = float(dt[0])/int(dt[1])
                                        elif "M" in dt and dt[0]!="M":
                                            dt = float(dt.replace("M", ""))*1000000
                                        else:
                                            dt = pd.to_datetime(dt)
                                    except:
                                        pass
                                
                                stats.append(dt)

                    j+=1



    df = pd.DataFrame(stats, index = names, columns=["stats"])
    return df.transpose() #, bsyc.contents
