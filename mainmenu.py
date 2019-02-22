# -*- coding: utf-8 -*-
"""
Created on Fri Feb 22 02:12:30 2019

@author: abdav
"""
import os
from Portfolio import Portfolio
import pandas as pd
import numpy as np
from func import check_date
import matplotlib.pyplot as plt

def print_menu_name(name):
    print("""
          ################################
                    """ + name + """  
          ################################\n""")

def main_menu():
    while True:
        print_menu_name('Main Menu')
        print('1: Press 1 for Stock Analysis')
        print('2: Press 2 to load an existing portfolio')
        print('3: Press 3 to create a portfolio')
        print('4: Press 4 to delete an existing portfolio')
        print('5: Press 5 to see loaded portfolios')
        print('6: Press 6 to save portfolios')
        print('7: Press 7 to select one portfolio and move forward')
        print('0: Press 0 to quit')
        response = input('enter a key...\n')
        number = False
        try:
            response = int(response)
            number=True
        except:
            print('Incorrect input. Please enter a number')
        if number:
            if response in [1,2,3,4,5,6,7,0]:
                return response
            else:
                print('Enter 1, 2, 3, 4, 5 or 6 please\n\n')
 
def see_loaded_portfolio_menu():
    print_menu_name('See Portfolios')
    print('These are the currently loaded portfolios, please enter the name of the one you want to see:\nType main to go back to the main menu\n')
    i=0
    for name in port_dict.keys():
        print(i, name)
        i+=1
    while True:
        response = input('Enter name...\n').strip()
        if response == 'main':
            return 1
        if response in port_dict.keys():
            break
        else:
            print('Incorrect name\n')
    print('\n\n')
    print(port_dict[response])
    input('Press any key to continue...')
    return 2
    
def save_portfolio_menu():
    print_menu_name('Save Portfolios')
    print('These are the currently loaded portfolios, please enter the name of the one you want to save:\nType main to go back to the main menu\n')
    i=0
    for name in port_dict.keys():
        print(i, name)
        i+=1
    while True:
        response = input('Enter name...\n').strip()
        if response == 'main':
            return 1
        if response in port_dict.keys():
            break
        else:
            print('Incorrect name\n')
    print('\n\n')
    port_dict[response].save_port()
    print('Portfolio', response, 'successfully saved')
    input('Press any key to continue...')
    return 2
    

def load_portfolio_menu():
    while True:
        print_menu_name('Load Portfolio')
        print('1: Press 1 to return to main menu')
        print('2: Enter the name of the portfolio to load')
        response = input()
        try:
            response = int(response)
            if response == 1:
                return 1
            else:
                print('Wrong Input\n\n')
        except:
            a = Portfolio()
            b = a.load_in(response)
            if b:
                port_dict[a.name] = a
                print('Portfolio ' +a.name+ ' was successfully loaded')
                return 1
                
            
def delete_portfolio_menu():
    while True:
        print_menu_name('Delete a Portfolio')
        print('1: Press 1 to return to main menu')
        print('2: Enter the name of the portfolio to delete')
        response = input('Enter answer ...\n')
        try:
            response = int(response)
            if response == 1:
                return 1
            else:
                print('Wrong Input\n\n')
        except:
            try:
                os.remove('Saved/' + response + '.csv')
                if response in port_dict:
                    del port_dict[response]
                print(response + ' was deleted successfully\n\n\n')
            except:
                print('No portfolio called ' + response + ' found')
        return 1
                
def create_portfolio_menu():
    while True:
        print_menu_name('Create a Portfolio')
        print('1: Press 1 to return to main menu')
        print('2: Press 2 if you want to make a portfolio with stocks/indices')
        print('3: Press 3 if you want to make a portfolio with filters')
        response = input()
        number = False
        try:
            response = int(response)
            number = True
        except:
            print('Incorrect input. Please enter a number\n\n')
        if number:
            if response == 1:
                return 1
            elif response == 2:
                return 2
            elif response == 3:
                return 3
            else:
                print('Wrong Input\n\n')
       
def filter_portfolio():
    name = input('Enter name for your portfolio\nEnter name...')
    d = {'Forward P/E': [0,0],
               'Market Cap (intraday)':[0,0],
               'Diluted EPS':[0,0],
               'Forward Annual Dividend Yield':[0,0],
               'Operating Margin':[0,0],
               'Profit Margin':[0,0],
               'Beta (3Y Monthly)':[0,0],
               'Avg Vol (3 month)':[0,0],
               'Quarterly Revenue Growth':[0,0]}
    
    while True:
        print("""\n\n1 - Forward P/E
2 - Market Cap (intraday)
3 - Diluted EPS
4 - Forward Annual Dividend Yield
5 - Operating Margin
6 - Profit Margin
7 - Beta (3Y Monthly)
8 - Avg Vol (3 month)
9 - Quarterly Revenue Growth
              
0 : Press 0 to go back to main menu
              
These are the available filters. PLease select the ones you want to use by typing their key separated by a coma
entrer a key...""")
        response = input().strip()
        if response == '0':
            return 0
        response = response.split(',')
        fmt=True
        for i in range(len(response)):
            try:
                response[i] = int(response[i].strip())
            except:
                print(response[i], ' is not a correct choice')
                fmt=False
                break
        if fmt:
            break
        
    for i in range(len(response)):
        while True:
            print('\nPlease enter the minimum value and the maximum value for', list(d.keys())[response[i]-1], 
                  '\nInput a zero for min if you do not want a minimum or a zero for max if you do not want a maximum'
                  '\ntype main to return the main menu')
            print('enter values ... ')
            r = input().strip()
            if r =='main':
                return 0
            fmt=True
            r = r.split(',')
            try:
                m = float(r[0].strip())
                M = float(r[1].strip())
            except:
                print('Wrong input format')
                fmt = False
            if fmt:
                d[list(d.keys())[response[i]-1]][0]=m
                d[list(d.keys())[response[i]-1]][1]=M
                break
    
    while True:
        print('\nPlease enter the maximum number of sctocks you want in your portfolio (cannot be 0)')
        n = input('enter n ... ')
        try:
            n = int(n.strip())
            fmt=True
        except:
            print(n, ' is not an int\n')
            fmt=False
        if fmt:
            if n==0:
                print('0 is not allowed')
            else:
                break
        
    a = Portfolio()
    print('create portfolio...')
    a.create_filter_port(d, n)
    a.set_name(name)
    if a.isempty():
        while True:
            print('Your criteria are too restrictive. No stocks found')
            print('Do you want to start over (1) or go back to main menu (0) ?')
            print('0 - main menu')
            print('1 - start over')
            ans = input('enter a key...\n')
            if ans.strip()=='1':
               return 1
            elif ans.strip()=='0':
                return 0
            else:
                print('Answer not recognized\n')
    
    while True:
        print('Do you want to use poke quant most efficient weight for this portfolio (1) or use equally weighted(2)?')
        print('0 - back to main menu')
        print('1 - Poke Quant most efficiet weights')
        print('2 - Equally weighted portfolio')
        ans = input('enter a key ...')
        if ans.strip() == '0':
            return 0 
        if ans.strip() == '1':
            weights = efficient_weight(a._portfolio.index.values)
            if weights == 'Fail': return 0
            a = Portfolio(a._portfolio.index.values, weights, name=name)
            break
        elif ans.strip() == '2':
            break
        else:
            print('Answer not recognized\n')
    
    port_dict[name] = a
    print('\nPortfolio', name, 'successfully created')
    return 0 
        
            
      
 
          
def stock_portfolio():
    print_menu_name('Stock Portfolio')
    print('Press 0 at any time to return to the main menu\n\n\n\n')
    print('1: Please enter a name for the portfolio')
    name = input()
    if name == '0':
        main_menu()
    while True:
        print('Please enter tickers separated by comas in the following format:')
        print("AAPL, MSFT, GOOG")
        tickers = input().strip()
        if tickers == '0':
            return 0
        fmt = True
        tickers = tickers.split(',')
        for i in range(len(tickers)):
            tickers[i] = tickers[i].strip()
            if not tickers[i] in main_tick.index.values:
                fmt = False
                print(tickers[i], ' is not a valid ticker. Spelling may be wrong or may not be available')
                break
        if fmt:
            break
        
    while True:
        print('If you want an equally weighted portfolio, press 1')
        print('If you want the poke quant most efficient weights press 2')
        print('Enter the weights for your portfolio separated by comas if you want personnalized weight in ' +\
              '\n(it should be the same length as the number of stocks) ')
        weights = input().strip()
        fmt = True
        if weights == '0':
            return 0
        if weights != '1' and weights!='2':
            weights = weights.split(',')
            if len(weights) != len(tickers):
                print(len(tickers), ' tickers\n', len(weights), 'weights')
                fmt = False
            else:
                for i in range(len(weights)):
                    try:
                        weights[i] = float(weights[i].strip())
                    except:
                        print(weights[i], ' is not float compatible')
                        fmt=False
                        break
        if weights =='2':
            weights = efficient_weight(tickers)
            if weights == 'Fail':
                return 0
        if fmt:
            break
    if weights == '1':
        a = Portfolio(tickers, name=name)
    else:
        a = Portfolio(tickers, weights, name=name)
    port_dict[name]=a
    print('portfolio', a.name, 'successfully created')
    return 0
        
def efficient_weight(tickers):
    a = Portfolio(tickers, name='temporary')
    df = a.eff_frt(plot=True)
    while True:
        print('This is the efficient frontier for your stocks. Enter the desired sigma, and the appropriate weights will be selected\nEnter main to return to main menu')
        sigma = input()
        if sigma.strip() == 'main':
            return 'Fail'
        try:
            sigma = float(sigma.strip())
            break
        except:
            print('The entered sigma is not float compatible\n')
    df = df.loc[((df.stdev>=(sigma-0.01)) & (df.stdev<=(sigma+0.01))), :]
    if len(df.index>0):
        df.reset_index(drop=True, inplace=True)
        if len(df.index>20):
            df = df.iloc[np.floor(np.random.uniform(size=20)*(len(df.index)-1)), :]
            df.reset_index(drop=True, inplace=True)
            df.sort_values(by='stdev', inplace=True)
            df.reset_index(drop=True, inplace=True)
        print(df)
        while True:
            print('Here are the portfolio matching your sigma. Please enter the index of the one you want\nType main to go back to main menu')
            ind = input().strip()
            if ind == 'main':
                return 'Fail'
            ind = int(ind)
            if ind in df.index.values:
                break
            else:
                print('wrong index, please select an available index\n')
                print(df)
        ind = int(ind)
        weights=df.iloc[ind, :-3].values
        return weights
    else:
        print('No sigma matches your selection, please select one according to the efficient frontier figure\n')
        print('Reloading efficient frontier ... \n')
        return efficient_weight(tickers)

def select_portfolio_menu():
    print_menu_name('Select Portfolio')
    print('These are the currently loaded portfolios, please enter the name of the one you want to work with\nType main to go back to the main menu\n')
    i=0
    for name in port_dict.keys():
        print(i, name)
        i+=1
    while True:
        response = input('Enter name...\n').strip()
        if response == 'main':
            return 0 
        if response in port_dict.keys():
            break
        else:
            print('Incorrect name\n')
    print('\n\n')
    selected_port[0] = port_dict[response]
    while True:
        print('Press 1 if you would like to edit the portfolio')
        print('Press 2 if you would like to perform some portfolio analysis')
        print('Press 0 if you would like to quit')
        response1 = input()
        number = False
        try:
            response1 = int(response1)
            number=True
        except:
            print('Incorrect input. Please enter a number')
        if number:
            if response1 == 1:
                return 1
            elif response1 == 2:
                return 2
            elif response1 == 0:
                return 0
            else:
                print('Enter 1, 2, 3, or 0 please\n\n')

def edit_portfolio_menu():
    while True:
        print_menu_name('Edit Portfolio')
        print('This is your current portfolio:')
        print(selected_port[0])
        print()
        print('1: Press 1 to set weights')
        print('2: Press 2 to add a stock')
        print('3: Press 3 to remove a stock')
        print('5: Press 0 to return to the main menu')
        response = input('Enter key...')
        number = False
        try:
            response = int(response)
            number=True
        except:
            print('Incorrect input. Please enter a number')
        if number:
            if response == 1:
                return 1
            elif response == 2:
                return 2
            elif response == 3:
                return 3
            elif response == 0:
                return 0
            else:
                print('Enter 1, 2, 3, 4, or 0 please\n\n')
 
def set_weights_menu():
    print_menu_name('Set Weights')
    p=selected_port[0]
    while True:
        print('0 - Press 0 to return to the main menu')
        print('1 - Press 1 for equally weighted portfolio')
        print('2 - Press 2 for Poke quant most efficent weights')
        print('3 - Press 3 to return to the Edit menu')
        print('Enter the weights for your portfolio separated by comas if you want personnalized weight in ' +\
              '\n(it should be the same length as the number of stocks) ')
        
        
        fmt = True
        weights = input("enter answer ... ").strip()
        if weights == '0':
            return 0
        if weights=='3':
            return 1
        elif weights == '1':
            p._portfolio.loc[:, 'Weight'] = [1/len(p._portfolio.index)]*len(p._portfolio.index)
            print('Weights successfully updates')
            print()
            print(p)
            input('Enter any key to conitnue ...')
            return 1
        elif weights == '2':
            w = efficient_weight(p._portfolio.index.values)
            if w == 'Fail':
                return 0
            #for ind, stock in enumerate(p._portfolio.index.values):
            p._portfolio.loc[:, 'Weight'] = w
            print('Weights successfully updated')
            print()
            print(p)
            input('Enter any key to conitnue ...')
            return 1
        else:
            weights = weights.split(',')
            if len(weights) == len(p._portfolio.index.values):
                for i in range(len(weights)):
                    try:
                        weights[i] = float(weights[i].strip())
                    except:
                        print(weights[i], ' is not float copatible')
                        fmt=False
                        break
                if fmt:
                     p._portfolio.loc[:, 'Weight'] = weights
                     print('Weights sussessfully uodated')
                     print()
                     print(p)
                     input('Enter any key to conitnue ...')
                     return 1
            else:
                print('Wrong input')
                fmt=False
        if fmt:
            break
    return 1
            
def add_stock_menu():
    print_menu_name('Add Stocks')
    while True:
        print('Press 0 for main menu')
        print('Press 1 for edit menu')
        print('Please enter the ticker and weight you would like to add separated by a comma, in the following format:')
        print('AAPL, 0.25')
        ticker = input('Enter ticker...').strip()
        if ticker == '0':
            return 0
        if ticker == '1':
            return 1
        fmt = True
        ticker = ticker.split(',')
        if not ticker[0].strip() in main_tick.index.values:
            print(ticker, ' is not a valid ticker')
            fmt = False
        try:
            ticker[1] = float(ticker[1].strip())
        except:
            fmt = False
            print(ticker[1], ' is not float compatible')
        if fmt:
            break
    selected_port[0].add_stock(ticker[0].strip(), ticker[1])
    print('Stock successfully added')
    print(selected_port[0])
    input('Enter any key to conitnue ...')
    return 1

def remove_stock_menu():
    print_menu_name('Remove Stocks')
    while True:
        print('Press 0 for main menu')
        prtin('Press 1 for edit menu')
        print('Please enter the ticker you would like to remove:')
        ticker = input('Enter ticker...').strip()
        if ticker == '0':
            return 0
        if ticker == '1':
            return 1
        if not ticker in selected_port[0]._portfolio.index.values:
            print(ticker, ' is not in the portfolio')
        else:
            break

    selected_port[0].remove_stock(ticker)
    print('Stock successfully removed')
    print(selected_port[0])
    input('Enter any key to conitnue ...')
    return 1
            
        
        
def portfolio_analysis_menu():
    while True:
        print_menu_name('Portfolio Analysis')
        print()
        print('1 - Press 1 to see main portfolio metrics')
        print('2 - Press 2 to see the portfolio summary')
        print('3 - Press 3 to access portfolio time series')
        print('4 - Press 4 for portfolio\'s return')
        print('5 - Press 5 to portfolio\'s sigma')
        print('6 - Press 6 for portfolio comparisons (port or indexes)')
        print('7 - Press 7 for stock time series')
        print('0 - Press 0 to return to the main menu')
        response = input('Enter a key ... \n').strip()
        nb = True
        try:
            response = int(response)
        except:
            nb=False
            print('Please input a number\n')
        if nb:
            if response in [1,2,3,4,5,6,7,0]:
                return response
            else:
                print('Wrong input, plus use one of the given choices')
                
def portfolio_metrics():
    print_menu_name('metrics')
    print(selected_port[0].ptf_summary())
    input('Type any key to continue ... ')
    return 0

def portfolio_summary():
    print_menu_name('summary')
    print(selected_port[0].summary())
    input('Type any key to continue ... ')
    return 0
    
def portfolio_tms():
    print_menu_name('time series')
    while True:
        print('Enter start and end date as yyyymmdd, yyyymmdd\n(you can use "today" (spelled today) for the last day')
        print('Press 0 for analysis menu')
        dt = input('Enter date ...\n').strip()
        if dt == '0':
            return 0
        else:
            dt = dt.split(',')
            
            try:
                dt[0] = check_date(dt[0].strip())
                dt[1] = check_date(dt[1].strip())
                fmt = True
            except:
                fmt = False
                print('Wrong date input\n')
            if fmt:
                print(selected_port[0].ptf_tms(dt[0], dt[1]))
                selected_port[0].ptf_tms(dt[0], dt[1]).plot(figsize=(8,8), label='Portfolio', legend=True, title='No rebalancing, weights change as prices change')
                print()
                print(selected_port[0].ptf_tms(dt[0], dt[1], True))
                selected_port[0].ptf_tms(dt[0], dt[1], True).plot(figsize=(8,8), label='Portfolio', legend=True, title='With rebalancing, weights are held constant')

                print('This is the evolution of the portfolio without rebalancing, weights are assumed to be constant')
                input('Enter an key to continue ... ')
                return 0
    return 0

def stock_tms():
    print_menu_name('time series stock')
    while True:
        print('Enter start and end date as yyyymmdd, yyyymmdd\n(you can use "today" (spelled today) for the last day')
        print('Press 0 for analysis menu')
        dt = input('Enter date ...\n').strip()
        if dt == '0':
            return 0
        else:
            dt = dt.split(',')
            
            try:
                dt[0] = check_date(dt[0].strip())
                dt[1] = check_date(dt[1].strip())
                fmt = True
            except:
                fmt = False
                print('Wrong date input\n')
            if fmt:
                print(selected_port[0].get_timeseries(dt[0], dt[1]))
                (100*selected_port[0].get_timeseries(dt[0], dt[1])/selected_port[0].get_timeseries(dt[0], dt[1]).iloc[0,:].values).plot(figsize=(8,8), legend=True)
                plt.show()
                print()
                input('Enter an key to continue ... ')
                return 0
    return 0
    
def portfolio_return():
    print_menu_name('Return')
    while True:
        print('Enter start and end date as yyyymmdd, yyyymmdd\n(you can use "today" (spelled today) for the last day')
        print('Press 0 for analysis menu')
        dt = input('Enter date ...\n').strip()
        if dt == '0':
            return 0
        else:
            dt = dt.split(',')
            
            try:
                dt[0] = check_date(dt[0].strip())
                dt[1] = check_date(dt[1].strip())
                fmt = True
            except:
                fmt = False
                print('Wrong date input\n')
            if fmt:
                print_menu_name('Return')
                print('Annualized return :',selected_port[0].get_return(dt[0], dt[1], annualized=True))
                print('Non annualized return :',selected_port[0].get_return(dt[0], dt[1], annualized=False))
                input('Enter any key to continue ...')
                return 0
            
def portfolio_sigma():
    print_menu_name('Sigma')
    while True:
        print('Enter start and end date as yyyymmdd, yyyymmdd\n(you can use "today" (spelled today) for the last day')
        print('Press 0 for analysis menu')
        dt = input('Enter date ...\n').strip()
        if dt == '0':
            return 0
        else:
            dt = dt.split(',')
            
            try:
                dt[0] = check_date(dt[0].strip())
                dt[1] = check_date(dt[1].strip())
                fmt = True
            except:
                fmt = False
                print('Wrong date input\n')
            if fmt:
                print_menu_name('Return')
                print('Annualized sigma :',selected_port[0].get_sigma(dt[0], dt[1], annualized=True))
                print('Non annualized sigma :',selected_port[0].get_sigma(dt[0], dt[1], annualized=False))
                input('Enter any key to continue ...')
                return 0

                

def main():
    
    current = 'main_menu()'
    while True:
        response = eval(current)
        
        if current == 'main_menu()':
            if response == 1:
                pass
            elif response == 2:
                current = 'load_portfolio_menu()'
            elif response == 3:
                current = 'create_portfolio_menu()'
            elif response == 4:
                current = 'delete_portfolio_menu()'
            elif response == 5:
                current = 'see_loaded_portfolio_menu()'
            elif response == 6:
                current = 'save_portfolio_menu()'
            elif response == 7:
                current = 'select_portfolio_menu()'
            elif response == 0:
                break
        
        elif current == 'load_portfolio_menu()':
            current = 'main_menu()'
        
        elif current == 'delete_portfolio_menu()':
            current = 'main_menu()'
        
        elif current == 'see_loaded_portfolio_menu()':
            if response ==1 : current = 'main_menu()'
            if response ==2 : current = 'see_loaded_portfolio_menu()'
        
        elif current == 'save_portfolio_menu()':
            if response ==1 : current = 'main_menu()'
            elif response == 2 : 'save_portfolio_menu()'

        elif current == 'create_portfolio_menu()':
            if response == 1 : current = 'main_menu()'
            if response == 2 : current = 'stock_portfolio()'
            if response == 3 : current = 'filter_portfolio()'

        elif current == 'filter_portfolio()':
            if response == 0 : current='main_menu()'
            if response == 1 : current='filter_portfolio()'
        
        elif current == 'stock_portfolio()':
            current = 'main_menu()'
            
        elif current == 'select_portfolio_menu()':
            if response == 0 : current = 'main_menu()'
            if response == 1 : current = 'edit_portfolio_menu()'
            if response == 2 : current = 'portfolio_analysis_menu()'
            
        elif current == 'edit_portfolio_menu()':
            if response == 0 : current = 'main_menu()'
            if response == 1: current = 'set_weights_menu()'
            if response == 2 : current = 'add_stock_menu()'
            if response == 3 : current = 'remove_stock_menu'
            
        elif current == 'set_weights_menu()':
            if response == 0 : current = 'main_menu()'
            if response == 1 : current = 'edit_portfolio_menu()'
            
        elif current == 'add_stock_menu()':
            if response == 0 : current = 'main_menu()'
            if response == 1 : current = 'edit_portfolio_menu()'
            
        elif current == 'remove_stock_menu()':
            if response == 0 : current = 'main_menu()'
            if response == 1 : current = 'edit_portfolio_menu()'
        
        elif current == 'portfolio_analysis_menu()':
            if response == 1 : current = 'portfolio_metrics()'
            if response == 2 : current = 'portfolio_summary()'
            if response == 3 : current = 'portfolio_tms()'
            if response == 4 : current = 'portfolio_return()'
            if response == 5 : current = 'portfolio_sigma()'
            if response == 6 : current = 'portfolio_com()'
            if response == 7 : current = 'stock_tms()'
            if response == 0 : current = 'main_menu()'
        
        elif current == ('portfolio_metrics()'):
            if response == 0: current = 'portfolio_analysis_menu()'
            
        elif current == ('portfolio_summary()'):
            if response == 0: current = 'portfolio_analysis_menu()'
            
        elif current == ('portfolio_tms()'):
            if response == 0: current = 'portfolio_analysis_menu()'
        
        elif current == ('stock_tms()'):
            if response == 0: current = 'portfolio_analysis_menu()'
            
        elif current == ('portfolio_return()'):
            if response == 0: current = 'portfolio_analysis_menu()'
            
        elif current == ('portfolio_sigma()'):
            if response == 0: current = 'portfolio_analysis_menu()'
        
        
        
        
           

    
        
if __name__ == '__main__':
    port_dict = dict()
    selected_port = ['']
    main_tick = pd.read_csv('comptick.csv', index_col=0)
    main()
    

    
    
