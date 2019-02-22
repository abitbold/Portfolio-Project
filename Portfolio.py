## Porfolio class

import pandas as pd
import numpy as np
import datetime
import pandas_datareader as web
import matplotlib.pyplot as plt
from func import *
from yahoo import get_stats_data, get_financial_data
import os

class Portfolio :
    
    comptick = pd.read_csv('comptick.csv', index_col=0)
    base_stats = pd.DataFrame(columns=['Market Cap (intraday)', 'Enterprise Value', 'Trailing P/E', 'Forward P/E',
       'PEG Ratio (5 yr expected)', 'Price/Sales', 'Price/Book',
       'Enterprise Value/Revenue', 'Enterprise Value/EBITDA', 'Fiscal Year Ends',
       'Most Recent Quarter', 'Profit Margin', 'Operating Margin', 'Return on Assets',
       'Return on Equity', 'Revenue', 'Revenue Per Share', 'Quarterly Revenue Growth',
       'Gross Profit', 'EBITDA', 'Net Income Avi to Common', 'Diluted EPS',
       'Quarterly Earnings Growth', 'Total Cash', 'Total Cash Per Share', 'Total Debt',
       'Total Debt/Equity', 'Current Ratio', 'Book Value Per Share',
       'Operating Cash Flow', 'Levered Free Cash Flow', 'Beta (3Y Monthly)',
       '52-Week Change', 'S&P500 52-Week Change', '52 Week High', '52 Week Low',
       '50-Day Moving Average', '200-Day Moving Average', 'Avg Vol (3 month)',
       'Avg Vol (10 day)', 'Shares Outstanding', 'Float', '% Held by Insider]',
       '% Held by Institutions', 'Shares Short (Jan 31, 2019)',
       'Short Ratio (Jan 31, 2019)', 'Short % of Float (Jan 31, 2019)',
       'Short % of Shares Outstanding (Jan 31, 2019)',
       'Shares Short (prior month Dec 31, 2018)', 'Forward Annual Dividend Rate',
       'Forward Annual Dividend Yield', 'Trailing Annual Dividend Rate',
       'Trailing Annual Dividend Yield', '5 Year Average Dividend Yield',
       'Payout Ratio', 'Dividend Date', 'Ex-Dividend Date',
       'Last Split Factor (new per old)', 'Last Split Date'])
    
    base_financial = pd.DataFrame(columns=['Total Revenue', 'Cost of Revenue', 'Gross Profit', 'Research Development',
       'Selling General and Administrative', 'Non Recurring', 'Others',
       'Total Operating Expenses', 'Operating Income or Loss',
       'Total Other Income/Expenses Net', 'Earnings Before Interest and Taxes',
       'Interest Expense', 'Income Before Tax', 'Income Tax Expense',
       'Minority Interest', 'Net Income From Continuing Ops',
       'Discontinued Operations', 'Extraordinary Items',
       'Effect Of Accounting Changes', 'Other Items', 'Net Income',
       'Preferred Stock And Other Adjustments',
       'Net Income Applicable To Common Shares', 'Cash And Cash Equivalents',
       'Short Term Investments', 'Net Receivables', 'Inventory',
       'Other Current Assets', 'Total Current Assets', 'Long Term Investments',
       'Property Plant and Equipment', 'Goodwill', 'Intangible Assets',
       'Accumulated Amortization', 'Other Assets',
       'Deferred Long Term Asset Charges', 'Total Assets', 'Accounts Payable',
       'Short/Current Long Term Debt', 'Other Current Liabilities',
       'Total Current Liabilities', 'Long Term Debt', 'Other Liabilities',
       'Deferred Long Term Liability Charges', 'Minority Interest',
       'Negative Goodwill', 'Total Liabilities', 'Misc. Stocks Options Warrants',
       'Redeemable Preferred Stock', 'Preferred Stock', 'Common Stock',
       'Retained Earnings', 'Treasury Stock', 'Capital Surplus',
       'Other Stockholder Equity', 'Total Stockholder Equity', 'Net Tangible Assets',
       'Net Income', 'Depreciation', 'Adjustments To Net Income',
       'Changes In Accounts Receivables', 'Changes In Liabilities',
       'Changes In Inventories', 'Changes In Other Operating Activities',
       'Total Cash Flow From Operating Activities', 'Capital Expenditures',
       'Investments', 'Other Cash flows from Investing Activities',
       'Total Cash Flows From Investing Activities', 'Dividends Paid',
       'Sale Purchase of Stock', 'Net Borrowings',
       'Other Cash Flows from Financing Activities',
       'Total Cash Flows From Financing Activities',
       'Effect Of Exchange Rate Changes', 'Change In Cash and Cash Equivalents'])

    ids = 1
    def __init__(self, tickers='', weight='', total = 1, name = 'default'):
        self._portfolio = pd.DataFrame(columns=['Name', 'Div', 'Mkt', 'Weight', 'Price', 'Last_update',\
                                                'Forward_PE', 'Beta', 'Dividend_yield',\
                                                'Diluted_EPS'])
        self.invest=total
        self.__id__ = Portfolio.ids
        Portfolio.ids += 1
        self.set_name(name)
        if len(tickers)>0:
            if type(tickers) is str:
                self.add_stock(tickers, 1)
            else:
                if ((weight=='') or (np.sum(weight)<=10)):
                    for ind, tick in enumerate(tickers):
                        if weight != '':
                            self.add_stock(tick, weight[ind])
                        else:
                            self.add_stock(tick, 1/len(tickers))
                else:
                    raise Exception ('Please learn 1st grade math, weights should sum to 1')
          
                
    def delete_port(self):        
        try:
            os.remove('Saved/' + self.name + '.csv')
        except:
            pass
        
    def set_name(self, name):
        if type(name)==str:
            self.name=name
        else:
            raise Exception ('Input name as string!')
            
    def add_stock(self, ticker, weight):
        if not ticker in Portfolio.comptick.index.values:
            raise Exception(str(ticker) + ' is not an available ticker')
        if not ticker in Portfolio.base_stats.index:
            Portfolio.base_stats.loc[ticker, :]= get_stats_data(ticker).loc['stats',:]
            if pd.isna(Portfolio.base_stats.loc[ticker,'Forward Annual Dividend Yield']): Portfolio.base_stats.loc[ticker,'Forward Annual Dividend Yield'] = 0 
        self._portfolio.loc[ticker, ['Div', 'Mkt']] = Portfolio.base_stats.loc[ticker, ['Forward Annual Dividend Yield',\
                                                                           'Market Cap (intraday)']].values
        
        self._portfolio.loc[ticker, 'Price'] = web.get_data_yahoo(ticker, start=check_date('last_week'), end=check_date())['Adj Close'][-1] 
        self._portfolio.loc[ticker, 'Last_update'] = check_date(fmt='%Y-%m-%d %H:%M')
        self._portfolio.loc[ticker, 'Weight'] = weight
        self._portfolio.loc[ticker, 'Name'] = Portfolio.comptick.loc[ticker, 'Company_name']
        self._portfolio.loc[ticker,'Beta'] = Portfolio.base_stats.loc[ticker, 'Beta (3Y Monthly)']
        self._portfolio.loc[ticker,'Dividend_yield'] = Portfolio.base_stats.loc[ticker,'Forward Annual Dividend Yield']
        self._portfolio.loc[ticker,'Diluted_EPS'] = Portfolio.base_stats.loc[ticker,'Diluted EPS']
        self._portfolio.loc[ticker,'Forward_PE'] = Portfolio.base_stats.loc[ticker,'Forward P/E']
        
        
    def remove_stock(self, ticker):
        if ticker in self._portfolio.index:
            self._portfolio.drop(ticker, inplace=True)
        
    def set_weight(self, ticker, weight):
        try:
            weight = float(weight)
        except:
            raise Exception ('weight must be a number (float compatible)')
        if ticker in self._portfolio.index:
            self._portfolio.loc[ticker, 'Weight'] = weight
        else:
            raise Exception(str(ticker) + ' is not in the portfolio')
            
    
    def get_return(self, first='last_week', last='today', rebalancing = False, annualized=True):
        if len(self._portfolio.index)>0:
            tms = self.ptf_tms(first, last, rebalancing)
            first = check_date(first, string=False)
            last = check_date(last, string=False)
            if annualized:
                return (tms[-1]/tms[0])**(250/(last-first).days)-1
            else:
                return (tms[-1]/tms[0]-1)
        else:
            return None
            
    
    def get_sigma(self, first='last_week', last='today', rebalancing = False, annualized=True):
        if len(self._portfolio.index)>0:
            tms = self.ptf_tms(first, last, rebalancing)
            if annualized:
                return(tms.std()*np.sqrt(250))#/(check_date(last, string=False)-check_date(first, string=False))))
            return tms.std()
        else:
            return None
    
    def summary(self):
        return Portfolio.base_stats.loc[self._portfolio.index,:].transpose()
    
    def ptf_tms(self, first = 'today', last = 'today', rebalancing = True):
        if rebalancing:
            initial_weights = self._portfolio.loc[:, 'Weight']
            prices = self.get_timeseries(first, last)
            prices = prices/prices.iloc[0,:]
            prices.iloc[1:,:] = (prices.iloc[1:,:].values / prices.iloc[0:-1,:].values)*initial_weights.values
            prices.iloc[0,:] = initial_weights
            return prices.sum(axis=1)
        else:
            prices = self.get_timeseries(first, last)
            p = prices.copy()
            prices = prices/prices.iloc[0,:]
            weights = np.zeros((len(prices.iloc[:,0]), len(self._portfolio.index)))
            initial_weights = self._portfolio.loc[:, 'Weight']
            weights[0,:] = self._portfolio.Weight.values
            weights[1:, :] = (prices.iloc[1:,:].values*initial_weights.values)/np.array([(prices.iloc[1:, :].values*initial_weights.values).sum(axis=1).tolist()]).transpose()
            p.iloc[1:,:] = (p.iloc[1:,:].values / p.iloc[0:-1,:].values)*weights[0:-1, :]
            p.iloc[0,:] = initial_weights
            return p.sum(axis=1)
          
    def get_timeseries(self, first='today', last='today', spec='Adj Close', tick=True, extra_tick=''):
        ## Dates have to be given as pandas compatible dates
        ## extra_tick has to be a list of string
        ## if tick is false, return only time series for the extra tick
        ## if tick is true return timeseries for all of the stocks in the portfolio plus the extra tick given
        ## first and last are the date, input the same date to get one day, do not specify any date
        ## to get the most current price
        first = check_date(first, 'first')
        last= check_date(last, 'last')
        if extra_tick=='':
            return web.get_data_yahoo(self._portfolio.index, start=first, end=last)[spec]
        else:
            if not type(extra_tick) == list:
                raise Exception('The extra tickers ust be given in a list of string')
            if tick:
                return web.get_data_yahoo(self._portfolio.index.values.tolist()+extra_tick, start=first, end=last)[spec]
            else:
                return web.get_data_yahoo(extra_tick, start=first, end=last)[spec] 
                
    
    def empty_port(self):
        for stock in self._portfolio.index:
            self._portfolio.drop(stock, inplace=True)

    def save_port(self):
        exists=False
        try:
            pd.read_csv('Saved/' + self.name + '.csv')
            exists = True
        except:
            pass
        if exists:
            a = ''
            while True:
                print('Portfolio ' +  self.name + ' already exists. Save over ?\n1 = yes\n2 = no')
                a=input()
                try: 
                    a = int(a)
                except: 
                    pass
                if ((a == 1) or (a== 2)):
                    break
                else:
                    print('Incorrect')
            if a==1:
                self._portfolio.to_csv('Saved/' + self.name + '.csv')
            else:
                return
        else:
            self._portfolio.to_csv('Saved/' + self.name + '.csv')


    def load_in(self, name):
        try:
            pd.read_csv('Saved/' + str(name) + '.csv')
            exists = True
        except:
            pass
        if exists:
            self._portfolio = pd.read_csv('Saved/' + str(name) + '.csv', index_col = 0)
        else:
            print('No portfolio named : ', name)

    
    def metrics_comp(self, b):
        temp = pd.concat([a.ptf_summary(), b.ptf_summary()], axis=1).copy()
        temp.columns = [self.name, b.name]
        return temp


    def __str__(self):
        return self._portfolio.to_string()


    def __repr__(self):
        return self.__str__()
        
    def isempty(self):
        if len(self._portfolio.index) == 0:
            return True
        else:
            return False

    def get_beta(self,first='last_week', last='today', index = '^GSPC'):
        corr_port, sigma_port, sigma_index = self.compute_corr(index, first, last, sigmas = True)
        beta_port = corr_port*sigma_port/sigma_index
        return (beta_port)
     
    def ptf_summary(self, first='last_week', last='today'):
        a = pd.DataFrame()#np.zeros(7,1), index = ['Portfolio Value', 'Forward P/E', 'Portfolio Beta',\
                         #'Dividend Yield', 'Diluted EPS', 'Portfolio Sigma', 'Portfolio Return'], columns = ['Portfolio Metrics'])
        a.loc['Portfolio Value','Portfolio Metrics'] = (1+self.get_return(first, last))*self.invest
        a.loc['Forward P/E','Portfolio Metrics'] = (self._portfolio.Weight.values * self._portfolio.Forward_PE).sum()
        a.loc['Portfolio Beta','Portfolio Metrics'] = self.get_beta(first,last)
        a.loc['Dividend Yield','Portfolio Metrics'] = (self._portfolio.Weight * self._portfolio.Dividend_yield).sum()
        a.loc['Diluted EPS','Portfolio Metrics'] = (self._portfolio.Weight * self._portfolio.Diluted_EPS).sum()
        a.loc['Portfolio Sigma','Portfolio Metrics'] = self.get_sigma(first,last, annualized=True)
        a.loc['Portfolio Return','Portfolio Metrics'] = self.get_return(first,last, annualized=True)
        return a
        
    def create_filter_port(self, d, n):
        stats = pd.read_csv('Allticks/Allticks2_Stats.csv', index_col=0)
        #stats.replace('NA', np.nan, inplace=True)
        col = {'Forward P/E': [0,0],
               'Market Cap (intraday)':[0,0],
               'Diluted EPS':[0,0],
               'Forward Annual Dividend Yield':[0,0],
               'Operating Margin':[0,0],
               'Profit Margin':[0,0],
               'Beta (3Y Monthly)':[0,0],
               'Avg Vol (3 month)':[0,0],
               'Quarterly Revenue Growth':[0,0]}
        if not type(d) is dict:
            raise Exception('filter should be entered as a dict')
        for k in d:
            if not k in col:
                raise Exception (str(k) + ' is not a filter')
            try: 
                d[k][0] = float(d[k][0])
                d[k][1] = float(d[k][1])
            except: 
                raise Exception(str(k) + ' should be a float for both end of the interval. Current value is : ',+ str(k))
            if d[k][0]>d[k][1] :
                raise Exception(str(k) + ' end is smaller than begining')
            col[k][0]=d[k][0]
            if d[k][1] == 0 : col[k][1] = 10000000000000000000
            else: col[k][1]=d[k][1]
            stats = stats.loc[((stats[k]>col[k][0]) & (stats[k]<col[k][1])), :] 
        if len(stats.index)>0:
            if len(stats.index)>n:
                stats = stats.iloc[np.floor(np.random.uniform(size=n)*n).astype('int'), :]   
            self.__init__(stats.index.values.tolist())
      
    def eff_frt(self, start = '2018-01-01', end = 'today', sims = 20000,
            plot = False):
        # plots the efficient frontier from the given portfolio of stocks
        # returns all of the max SR weights, returns, vols in a dataframe
        nstocks = len(self._portfolio.index)
        start_s = check_date(start, 'Start', False)
        end_s = check_date(end, 'End', False)
        try:
            rf = get_rates(start_s, end_s).loc[start_s,'10yr']
        except KeyError:
            try:
                start_s = start_s + datetime.timedelta(days = 1)
                rf = get_rates(start_s, end_s).loc[start_s, '10yr']
            except KeyError:
                start_s = start_s + datetime.timedelta(days = 1)
                rf = get_rates(start_s, end_s).loc[start_s, '10yr']
        rf /= 100.0
        ts = self.get_timeseries(start, end, 'Adj Close', True)
        ts = ts/ts.shift(1)
        ann_returns = (np.prod(ts, axis = 0)**(250/ts.shape[0])) - 1
        ts = ts.dropna(axis = 0)
        stdev_ind = ts.std()*np.sqrt(250)
        cov = (ts.cov()).values
        ret_std = np.zeros((sims,2))
        ws = []
        for i in range(sims):
            weights = np.random.random(nstocks)
            weights /= sum(weights)
            ws.append(weights)
            ret_std[i,0] = weights.dot(ann_returns)
            ret_std[i,1] = np.sqrt(weights.dot(cov.dot(weights)))*np.sqrt(250)
        ws = np.array(ws)
        min_std_index = list(np.where(ret_std[:,1] == ret_std[:,1].min())[0])[0]
        min_ret = ret_std[min_std_index,0]
        shrp_rats = (ret_std[:,0] - rf)/ret_std[:,1]
        ival = (min_ret, min_ret + .001)
        pfolio_idx = list(np.where(np.greater_equal(ret_std[:,0], ival[0]) & np.less(ret_std[:,0], ival[1]))[0])
        max_SR_list = []
        idxs = []
        while pfolio_idx:
            max_SR = np.amax(shrp_rats[pfolio_idx])
            max_SR_idx = list(np.where(shrp_rats == max_SR)[0])[0]
            max_SR_list.append((max_SR, max_SR_idx))
            idxs.append(max_SR_idx)
            ival = (ival[0] + .001, ival[1] + .001)
            pfolio_idx = list(np.where(np.greater_equal(ret_std[:,0], ival[0]) & np.less(ret_std[:,0], ival[1]))[0])
        if plot:
            plt.figure(num = None, figsize = (8,6), dpi = 80, facecolor = 'w', edgecolor = 'k')
            plt.scatter(stdev_ind, ann_returns, c = 'g', s = 15, label = list(self._portfolio.index))
            plt.scatter(ret_std[:,1], ret_std[:,0], c = 'b', s = 1, label = 'Hypothetical Portfolios')
            plt.scatter(ret_std[idxs,1], ret_std[idxs,0], c = 'r', s = 5, label = 'Maximum Sharpe Ratios')
            plt.ylabel("Absolute Returns")
            plt.xlabel("Standard Deviation")
            plt.legend()
            plt.show()

        opt_ws = ws[idxs]
        opt_rets = ret_std[idxs,0]
        opt_std = ret_std[idxs,1]
        opt_SR = shrp_rats[idxs]
        col_names = list(self._portfolio.index) + ['returns'] + ['stdev'] + ['Sharpe']
        df = pd.DataFrame(columns = col_names)
        for idx, val in enumerate(opt_ws):
            row = list(val) + [opt_rets[idx]] + [opt_std[idx]] + [opt_SR[idx]]
            row_d = dict(zip(col_names,row))
            df_temp = pd.DataFrame(row_d, index = [0])
            df = pd.concat([df, df_temp], ignore_index = True)
        return df

    def benchmark(self,start, end, index = None, plot = False, sigmas = False,
                  normalize = False, rate = '10yr', log = False, returns = False):
        # returns correlation between portfolio and index if specified
        # else returns correlation between
        # 11:06 PM
        port_vals = self.ptf_tms(start,end)
        toplot = 100*port_vals/port_vals.iloc[0]
        if returns:
            toplot = compute_returns(port_vals, log)
            
        if index:
            try:
                print("Trying to get time series for index.")
                i_ts = self.get_timeseries(start,end,'Adj Close', False, [index]).loc[:,index]
            except:
                print("Failed to get time series for index.")
                raise Exception("Not a valid index/ticker")
            print("Computing returns for the index")
            indextoplot = 100*i_ts/i_ts.iloc[0]
            if returns:
                indextoplot = compute_returns(i_ts,log)
            return benchmark_help(toplot, indextoplot, plot, sigmas,normalize)
        else:
            try:
                print("Getting rates from the Fed")
                rates = get_rates(start,end).loc[:,rate]
            except:
                print("Failed to get rates from the Fed")
                raise Exception ("Not a valid interest rate")
            port_rets = compute_returns(port_vals)
            return benchmark_help(port_rets, rates, plot, sigmas, normalize, True)
    
    def sharpe_ratio_ptf(self, first='today', last='today', rebalancing = True):
        from scipy.stats.mstats import gmean
        first = check_date(first,'first')
        last = check_date(last,'last')
        ptf = self.ptf_tms(first,last, rebalancing)
        rp = gmean(np.compute_returns(ptf)+1)-1
        rf = get_rates(first,last).loc[first,'10yr']
        sig = ptf.std()*np.sqrt(250)
        return (rp - rf)/sig

    def sharpe_ratio_stk(self, first='today', last='today'):
        from scipy.stats.mstats import gmean
        first = check_date(first,'first')
        last = check_date(last,'last')

        stk = self.get_timeseries(first,last)
        rp = gmean(np.compute_returns(stk)+1)-1
        rf = get_rates(first,last).loc[first,'10yr']
        sig = stk.std()*np.sqrt(250)

        return (rp - rf)/sig
    
    def compute_corr(self, x, start = '2018-01-01', end = 'today',
                     sigmas = False, plot = False):
        # returns correlation between portfolio and index/time series
        # optionally returns annualized volatility
        # optionally plots the two time series of returns
        
        if type(x) is str: # x is a ticker for a stock/index
            return self.benchmark(start, end, x, plot, sigmas)
        else: # x is a time series
            ts1 = self.pft_tms(start, end)
            rt1 = compute_returns(ts1)
            rt2 = compute_returns(x)
            
        sigmax = np.std(rt2)*np.sqrt(250)
        sigmay = np.std(rt1)*np.sqrt(250)
        
        if sigmas:
            return (np.corrcoef(rt1,rt2)[0,1], sigmay, sigmax)
        return np.corrcoef(rt1,rt2)[0,1]
        
    def plot_portfolios_ts(self, other_port, start = '2018-01-01', end = 'today'):
        # compares current portfolio ts with another portfolio's ts
        ts1 = self.pft_tms(start, end)
        ts2 = other_port.pft_tms(start, end)
        xs = list(ts1.index)
        ts1 = ts1*100/ts1[0]
        ts2 = ts2*100/ts2[0]
        plt.plot(xs, ts1, c = 'b', label = ts1.name)
        plt.plot(xs, ts2, c = 'r', label = ts2.name)
        plt.legend()
        plt.show()
        return np.corrcoef(ts1, ts2)[0,1]
    

    
if __name__ == '__main__':
    a = Portfolio(['AAPL', 'MSFT', 'GE'])
    print(a)
