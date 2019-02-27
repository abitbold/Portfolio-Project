## file name : options_module.py
## 
## team member:
##      Arjun Alagappan
##      David Abitbol
##      Cody Cao
##      Lily li
##      Shanshan Liu
##      Kurtis Lee
##
## This file contains all of the code related to the option. Options do not evolve like stock and portfolio, 
## hence they cannot use the same methods, and have their own module
## This file imports: func.py
## This file is imported by: stock_menu.py

from wallstreet import Stock,Call,Put #pip install wallstreet

import datetime
import pandas as pd
import numpy as np
import scipy as sp
import matplotlib
import matplotlib.pyplot as plt
import math
from func import *

# In[2]:


#Control for printing
import sys, os

# Disable
def suppress_stdout():
    with open(os.devnull, "w") as devnull:
        old_stdout = sys.stdout
        sys.stdout = devnull
        try:  
            yield
        finally:
            sys.stdout = old_stdout
            
import re


# # Function Definitions for Monte Carlo Simulation

# In[3]:


def black_scholes(S0,K,r,sigma,T,d,pc):

    d1=(np.log(S0/K)+(r-d+0.5*sigma**2)*T)/(sigma*np.sqrt(T))
    d2=d1-sigma*np.sqrt(T)
    
    if pc=='Call':
        if T == 0:
            return np.maximum(S0-K, 0)
        return S0*np.exp(-1*d*T)*sp.stats.norm.cdf(d1)-K*np.exp(-1*r*T)*sp.stats.norm.cdf(d2)
    elif pc=='Put':
        if T == 0:
            return np.maximum(K-S0, 0)
        return -S0*np.exp(-1*d*T)*sp.stats.norm.cdf(-d1)+K*np.exp(-1*r*T)*sp.stats.norm.cdf(-d2)        
    else:
        print("Error: Please specify Call or Put")
        
#Need to call dividends and rates from other data
def stochastic_vol_bs(S0,K,r,q,V0,T,alpha,psi,pc,N=100,n=52):
    d = T/float(N)
    #V0=np.sqrt(V0)
    
    #Geometric browning motion for vol
    f1 = (alpha-0.5*psi**2)*d
    f2 = psi*np.sqrt(d)
    z1=np.random.randn(n,N+1)
    
    V = np.zeros((n,N+1))
    z1 = f1 + f2*z1
    z1[:,0] = 0
    EE = np.cumsum(z1, axis = 1)
    V = V0*np.exp(EE)
    
    #Black Scholes
    sigma=np.sqrt(np.mean(V,axis=1))
    C = np.zeros(n)
    C = black_scholes(S0,K,r,sigma,T,q,pc)

    price = np.mean(C)
    std_err=np.std(C)/np.sqrt(n)
    
    return price


# # Function Definitions for DataFrame Creation

# In[4]:



#Input: List of stock tickers
#Output: Panda Dataframes for Options, Options At the Money, Option Straddles

def get_options_dfs(tcker_list):
    d=[]
    for tcker in tcker_list:
        #enablePrint()
        try:
            price=Stock(tcker, source='yahoo').price
            c=Call(tcker,strike=price,source='yahoo')
            for exp in c.expirations:
                #blockPrint()
                day=int(exp.split('-')[0])
                month=int(exp.split('-')[1])
                year=int(exp.split('-')[2])

                c=Call(tcker,strike=price,source='yahoo',d=day,m=month,y=year)
                p=Put(tcker,strike=price,source='yahoo',d=day,m=month,y=year)

                d.append({'Expiration':exp,
                                  'Ticker':tcker,
                                  'Call/Put':'Call',
                                  'Underlying Price': price,
                                  'Strike': c.strike,
                                  'Price':c.price,
                                  'Implied Vol': c.implied_volatility(),
                                  'Delta' : c.delta(),
                                  'Gamma':c.gamma()})

                d.append({'Expiration':exp,
                                  'Ticker':tcker,
                                  'Call/Put':'Put',
                                  'Underlying Price': price,
                                  'Strike': p.strike,
                                  'Price':p.price,
                                  'Implied Vol': p.implied_volatility(),
                                  'Delta' : p.delta(),
                                  'Gamma':p.gamma()})

                

        

        
        except:    
            print("Unfortunately we do not have that ticker in our database, please email PokeQuant@gmail.com to request additional data.")

       
        df=pd.DataFrame(d)
        
        #####Clean data for Analysis#####
        df['ATM'] = pd.Series((df['Underlying Price'] > df['Strike']*.99) & (df['Underlying Price']<df['Strike']*1.01), index=df.index)
        df['Expiration'] = pd.to_datetime(df['Expiration'])

        #Calculate time to expiration
        df['Today']=datetime.datetime.now()
        df['Today'] = pd.to_datetime(df['Today'])
        df['Time to Expiration'] = np.busday_count(df['Today'].values.astype('datetime64[D]'),df['Expiration'].values.astype('datetime64[D]'))

        rate = get_rates(datetime.datetime.now() - datetime.timedelta(days = 7), 'today').iloc[-1,:]['10yr']/100
        
        
        
        df['PokeQuant Price'] = df.apply(lambda row: stochastic_vol_bs(row['Underlying Price'], 
                                                                       row['Strike'],
                                                                       rate,
                                                                       get_dividend(row['Ticker']), #Pull dividend data, get_dividend()
                                                                       row['Implied Vol']**2, 
                                                                       row['Time to Expiration']/252,
                                                                       0.01, #calibrate Model
                                                                       0.01, #calibrate Model
                                                                       row['Call/Put']), axis=1)

        df['PokeQuant Mispricing'] = df['Price']-df['PokeQuant Price']
        df['PokeQuant Recommendation'] =  np.where(df['PokeQuant Mispricing']>0, 'Bullish', 'Bearish')
        
        #Take out non-ATM options and old Options
        df_atm=df[(df.ATM==True) & (df['Time to Expiration']>0)].loc[:,df.columns!='Today']

        df_atm=df_atm.sort_values(by='Expiration')
        df_new=df[df['Time to Expiration']>0]
        
        #####Identify Prices#####
        


        #create straddle prices
        aggregation_functions = {'Price': 'sum', 'PokeQuant Price': 'sum','PokeQuant Price': 'sum'}
        df_straddle = df_atm.groupby(['Ticker','Expiration','Strike']).aggregate(aggregation_functions)
        df_straddle['PokeQuant Mispricing'] = (df_straddle['Price']-df_straddle['PokeQuant Price'])/df_straddle['PokeQuant Price']
        df_straddle['PokeQuant Recommendation'] =  np.where(df_straddle['PokeQuant Mispricing']>0, 'Bullish', 'Bearish')

        df_straddle=df_straddle.reset_index()     
        
    return df_new,df_atm,df_straddle
    

    


# # Data Test

# In[5]:





# In[6]:




# # Functions to print information

# In[7]:


#Use: Prints all options where the recommendation is in bullish or bearish direction
#Inputs df, direction == 'Bearish', 'Bullish'
#Output df with only that direction
def get_pq_recommendation(df,direction):
    print("The options PokeQuant are",direction,"on:\n", 
          df.loc[df['PokeQuant Recommendation']==direction])


#Prints best options to go long/short on
def get_top3(df):
    top3_bull=df.sort_values(by='PokeQuant Mispricing', ascending = False).head(3)
    top3_bear=df.sort_values(by='PokeQuant Mispricing').head(3)
    
    print("Top 3 bulls recommended by PokeQuant: \n",top3_bull)
    print("\n\n")
    print("Top 3 bears recommended by PokeQuant: \n",top3_bear)
    


# In[8]:





# # Visualization

# In[9]:


def options_visualization_vol_skew(df_atm):
    if df_atm.empty:
        print("No at the money options available\n")
    
    for stock in df_atm.Ticker.unique():
        plt.plot(df_atm.loc[(df_atm.Ticker==stock) & (df_atm['Call/Put']=='Call')].Expiration,
                    df_atm.loc[(df_atm.Ticker==stock) & (df_atm['Call/Put']=='Call')]['Implied Vol'],label=stock)     

    plt.xticks(rotation=90)
    plt.xlabel('Expiration Date')
    plt.ylabel('Mispricing')
    plt.title('Implied Vol Skew by Stock')
    plt.legend(loc="bottom left")
    plt.show()
    
def options_visualization_mispricing_scat(df):    
    df=df.dropna()    
    for stock in df.Ticker.unique():
        plt.scatter(np.array(df.loc[df.Ticker==stock].Expiration),
                    np.array(df.loc[df.Ticker==stock]['PokeQuant Mispricing']),label=stock)

        
    plt.xticks(rotation=90)
    plt.xlabel('Expiration Date')
    plt.ylabel('Mispricing')
    plt.title('Straddle Mispricing by Stock')
    plt.legend(loc="bottom left")
    plt.show()


# In[10]:


def options_visualization_mispricing_hist(df):
    df=df.dropna()
    for stock in df.Ticker.unique():
        plt.hist(df.loc[df.Ticker==stock]['PokeQuant Mispricing'],alpha=0.5, label=stock)

    plt.xlabel('Mispricing')
    plt.ylabel('Frequency')
    plt.title('Mispricing Histogram by Stock')
    plt.legend(loc="top left")
    plt.show()


# In[11]:


def options_visualization_straddle_payoff(df_straddle,stock,expir):

    try:
        opt = df_straddle.loc[(df_straddle.Ticker==stock) & (df_straddle.Expiration==expir)]
        K=int(opt.Strike)
        price=int(opt['PokeQuant Price'])
    except:
        print("Unfortunately we do not have that option in our database, please email PokeQuant@gmail.com to request additional data.")

    
    x_vals_1=np.arange(K,K+math.floor(.1*K)+1)
    y_vals_1=(x_vals_1-K)-price

    x_vals_2=np.arange(K-math.floor(.1*K),K+1)
    y_vals_2=-1*(x_vals_2-K)-price

    plt.plot(x_vals_1,y_vals_1,color='navy')
    plt.plot(x_vals_2,y_vals_2,color='navy')

    #profit points
    plt.axvline(x=K+price,linestyle='--',color='green',label='Profit Marker')
    plt.axvline(x=K-price,linestyle='--',color='green')
    plt.axhline(y=0,color='black')
    
    plt.xlabel('Stock Price')
    plt.ylabel('Payoff')
    plt.title('Straddle Payoff Diagram of\n {}'.format(stock+", Strike: "+str(K)+", Expiration: "+expir))
    plt.legend(loc="top left")
    plt.show()


# # Test

# In[13]:

if __name__ == '__main__':
    import time

    start = time.time() #Measure time

    my_port=['PANW', 'GS'] #4 minutes runtime
    df,df_atm,df_straddle=get_options_dfs(my_port)
    df

    end = time.time() #Measure time
    print(end - start)
    
    get_pq_recommendation(df,'Bullish')
    
    options_visualization_vol_skew(df_atm)
    options_visualization_mispricing_scat(df)
    options_visualization_mispricing_hist(df)
    options_visualization_straddle_payoff(df_straddle,'GOOG','2019-02-22')

