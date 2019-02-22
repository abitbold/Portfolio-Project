## Porfolio clas

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

    def __init__(self, tickers='', weight='', total = 1000000):
        self._portfolio = pd.DataFrame(columns=['Name', 'Div', 'Mkt', 'Weight', 'Price', 'Last_update',\
                                                'Forward_PE', 'Beta (3Y Monthly)', 'Dividend_yield',\
                                                'Diluted EPS'])
        self.invest=total
                
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

    def save_port(self, name):
        exists=False
        try:
            pd.read_csv('Saved/' + str(name) + '.csv')
            exists = True
        except:
            pass
        if exists:
            a = ''
            while True:
                print('Portfolio ' +  name + ' already exists. Save over ?\n1 = yes\n2 = no')
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
                self._portfolio.to_csv('Saved/' + name + '.csv')
            else:
                return
        else:
            self._portfolio.to_csv('Saved/' + name + '.csv')


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


    def __str__(self):
        return self._portfolio.to_string()


    def __repr__(self):
        return self.__str__()
        
    def isempty(self):
        if len(self._portfolio.index) == 0:
            return True
        else:
            return False

    def get_beta(self,first='last week', last='today', index = '^GSPC'):
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
        print(a)
        
    def create_filter_port(self, d):
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
            if d[k][1] == 0 : col[k][1] = 1000000000000000000
            else: col[k][1]=d[k][1]
            stats = stats.loc[((stats[k]>col[k][0]) & (stats[k]<col[k][1])), :] 
        print(stats.index)
        self.__init__(stats.index.values)
      
      
    
        
        
