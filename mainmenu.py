## file name : mainmenu.py
## 
## team member:
##      Arjun Alagappan
##      David Abitbol
##      Cody Cao
##      Lily li
##      Shanshan Liu
##      Kurtis Lee
##
## This is the main file of our application. It is the one is being launched. It controls the flow of the application
## This file imports: stock_menu.py, func.py, Portfolio.py
## This file is imported by nothing

import os
from Portfolio import Portfolio
import pandas as pd
import numpy as np
from func import check_date
import matplotlib.pyplot as plt
import warnings
import time
import stock_menus

port_dict = dict()
selected_port = ['']
main_tick = pd.read_csv('comptick.csv', index_col=0)

def print_menu_name(name):
    d = ''
    for i in range(len(name)+10):
        d += '#'
    print('\n\n' + d)
    print('     ' + name)
    print(d + '\n\n')

def main_menu():
    if type(selected_port[0])!=str:
        port_dict[selected_port[0].name] = selected_port[0]
    while True:
        print_menu_name('Main Menu')
        print('** Press 1 for Stock Analysis')
        print('** Press 2 to load an existing portfolio')
        print('** Press 3 to create a portfolio')
        print('** Press 4 to delete an existing portfolio')
        print('** Press 5 to see loaded portfolios')
        print('** Press 6 to save portfolios')
        print('** Press 7 to select one portfolio and move forward')
        print('** Press 0 to quit')
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
    print('These are the currently loaded portfolios, please enter the name of the one you want to see:\nType 0 to go back to previous menu\n')
    i=0
    for name in port_dict.keys():
        print(i, name)
        i+=1
    while True:
        response = input('Enter name...\n').strip()
        if response == '0':
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
    print('These are the currently loaded portfolios, please enter the name of the one you want to save:\nType 0 to return to the previous menu\n')
    i=0
    for name in port_dict.keys():
        print(i, name)
        i+=1
    while True:
        response = input('Enter name...\n').strip()
        if response == '0':
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
        L = os.listdir(r'Saved')
        L2 = []
        if len(L)>0:
            for el in L:
                if el.split('_')[0] != 'base':
                    L2.append(el)
        if len(L2)>0:
            print('These are the existing portfolios:')
            for el in L2:
                print('\t', el.split('.csv')[0])
            print()
            print('** Press 0 to return to the the previous menu')
            print('** Enter the name of the portfolio you wish to load')
            response = input('Enter name...\n').strip()
            if response == '0':
                return 1
            if (response+'.csv') in L2:
                if response in port_dict.keys():
                    print('Portfolio', response, 'already loaded\n')
                else:
                    a = Portfolio()
                    b = a.load_in(response)
                    if b:
                        port_dict[a.name] = a
                        print('Portfolio ' +a.name+ ' was successfully loaded')
                        pause()
                        return 2
                    else:
                        print('Issue importing portfolio. Please try another one')
                        return 2
            else :
                print('\n', response, ' is an incorrect name. Load failed.')
                input('Press any key to continue...\n')
                return 2
        else:
            print('No currently saved portfolio. \nPress any key to return to previous menu')
            input()
            return 1
            
                    
                
            
def delete_portfolio_menu():
    while True:
        print_menu_name('Delete a Portfolio')
        L = os.listdir(r'Saved')
        L2 = []
        if len(L)>0:
            for el in L:
                if el.split('_')[0] != 'base':
                    L2.append(el.split('_')[0])
        if len(L2)>0:
            print('These are the currently saved portfolio:')
            for el in L2:
                print('\t', el.split('.csv')[0])
            print()            
            
            print('** Press 0 to return to the previous menu')
            print('** Enter the name of the portfolio to delete')
            response = input('Enter answer ...\n')
            try:
                response = int(response).strip()
                if response == 0:
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
                    pause()
            return 1
        else:
            print('There is currently no saved portfolio to delete')
            pause()
            return 1
                
def create_portfolio_menu():
    while True:
        print_menu_name('Create a Portfolio')
        print('** Press  0 to return to the previous menu')
        print('** Press 2 if you want to make a portfolio with stocks/indices')
        print('** Press 3 if you want to make a portfolio with filters')
        response = input()
        number = False
        try:
            response = int(response)
            number = True
        except:
            print('Incorrect input. Please enter a number\n\n')
        if number:
            if response == 0:
                return 1
            elif response == 2:
                return 2
            elif response == 3:
                return 3
            else:
                print('Wrong Input\n\n')
       
def filter_portfolio():
    while True:
        name = input('Enter name for your portfolio ("0" is not a valid name)\nEnter name...').strip()
        if name == '0':
            print('Wrong input')
            pause()
        else:
            break
              
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
              
0 : Press 0 to return to the previous menu
              
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
                  '\nInput 00 for min if you do not want a minimum or a 00 for max if you do not want a maximum'
                  '\ntype 0 to return to the previous menu')
            print('enter values ... ')
            r = input().strip()
            if r =='0':
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
        print('\nPlease enter the maximum number of stocks you want in your portfolio (cannot be 0)')
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
            print('Do you want to start over (1) or go back to the previous menu (0) ?')
            print('** Press 0 to return to the previous menu')
            print('** Press 1 to start over')
            ans = input('enter a key...\n')
            if ans.strip()=='1':
               return 1
            elif ans.strip()=='0':
                return 0
            else:
                print('Answer not recognized\n')
    
    while True:
        print('Do you want to use poke quant most efficient weight for this portfolio (1) or use equally weighted(2)?')
        print('** Press 0  to return to the previous menu')
        print('** Press 1 to use Poke Quant most efficient weights')
        print('** Press 2 for an  equally weighted portfolio')
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
    print('** Press 0 at any time to return to the previous menu\n\n\n\n')
    print('** Otherwise enter a name for the portfolio')
    name = input().strip()
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
        print('** Press 1 for an equally weighted portfolio')
        print('** Press 2 to use Poke Quant most efficient weights')
        print('** Else : enter the weights for your portfolio separated by comas if you want personnalized weight in ' +\
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
        print('This is the efficient frontier for your stocks. Enter the desired sigma, and the appropriate weights will be selected\nEnter 0 to return to the previous menu')
        sigma = input()
        if sigma.strip() == '0':
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
            df['index2'] = df.index.values+1
            df.set_index(df.index2, inplace=True, drop=True)
            df.drop('index2', axis=1, inplace=True)
        print(df)
        while True:
            print('Here are the portfolio matching your sigma. Please enter the index of the one you want\nType 0 to go back to the previous menu')
            ind = input().strip()
            if ind == '0':
                return 'Fail'
            ind = int(ind)
            if ind in df.index.values:
                break
            else:
                print('wrong index, please select an available index\n')
                pause()
                print(df)
        ind = int(ind)
        weights=df.iloc[ind-1, :-3].values
        return weights
    else:
        print('No sigma matches your selection, please select one according to the efficient frontier figure\n')
        print('Reloading efficient frontier ... \n')
        return efficient_weight(tickers)

def select_portfolio_menu():
    print_menu_name('Select Portfolio')
    print('These are the currently loaded portfolios, please enter the name of the one you want to work with\nType 0 to to return to the previous menu\n')
    i=0
    for name in port_dict.keys():
        print(i, name)
        i+=1
    while True:
        response = input('Enter name...\n').strip()
        if response == '0':
            return 0 
        if response in port_dict.keys():
            break
        else:
            print('Incorrect name\n')
    print('\n\n')
    selected_port[0] = port_dict[response]
    while True:
        print('** Press 1 if you would like to edit the portfolio')
        print('** Press 2 if you would like to perform some portfolio analysis')
        print('** Press 0 if you would like to return to the previous menu')
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
        print('** Press 1 to set weights')
        print('** Press 2 to add a stock')
        print('** Press 3 to remove a stock')
        print('** Press 0 to return to the previous menu')
        response = input('Enter key...').strip()
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
        print('** Press 0 to return to the main menu')
        print('** Press 1 for equally weighted portfolio')
        print('** Press 2 for Poke quant most efficent weights')
        print('** Press 3 to return to the Edit menu')
        print('** Else: Enter the weights for your portfolio separated by comas if you want personnalized weight in ' +\
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
            pause()
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
            pause()
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
        print('** Please enter the ticker and weight you would like to add separated by a comma, in the following format:')
        print('AAPL, 0.25')
        print('** Press 0 to return to the previous menu')
       
        ticker = input('Enter ticker...').strip()
        if ticker == '0':
            return 1
        #if ticker == '1':
        #    return 1
        fmt = True
        ticker = ticker.split(',')
        if len(ticker) == 2 :
            if not ticker[0].strip() in main_tick.index.values:
                print(ticker, ' is not a valid ticker')
                fmt = False
            try:
                ticker[1] = float(ticker[1].strip())
            except:
                fmt = False
                print(ticker[1], ' is not float compatible')
                pause()
            if fmt:
                break
        else:
            print('wrong input\n')
            pause()
    selected_port[0].add_stock(ticker[0].strip(), ticker[1])
    print('Stock successfully added')
    print(selected_port[0])
    input('Enter any key to continue ...')
    return 1

def remove_stock_menu():
    print_menu_name('Remove Stocks')
    print('This is your current portfolio:')
    print(selected_port[0])
    pause()
    while True:
        print('Please enter the ticker you would like to remove:')
        print('** Press 0 to return to the previous menu')
       # print('Press 1 to return to the edit menu')
        ticker = input('Enter ticker...').strip()
        if ticker == '0':
            return 1
        #if ticker == '1':
        #    return 1
        if not ticker in selected_port[0]._portfolio.index.values:
            print(ticker, ' is not in the portfolio')
        else:
            break

    selected_port[0].remove_stock(ticker)
    print('Stock successfully removed')
    print(selected_port[0])
    pause()
    return 1
   
def pause():
    input('Enter any key to continue ... ')        
    
def port_comp_menu():
    while True:
        print_menu_name('Portfolio comparison')
        print('** Enter the first and last date of your analysis, separated by a coma, in the following format')
        print('yyyymmdd, yyyymmdd')
        print('or\n,yyyymmdd, today (to go from the first date to today)')
        print('(Enter 0 to return the previous menu)')
        response = input('Enter date ... \n').strip()
        if response == '0' :
            return 0
        dt = response.split(',')
        if len(dt) != 2:
            print(response, ' is not in the correct format')
            pause()
            return 1
        for i in range(2):
            try:    
                dt[i] = check_date(dt[i].strip())
            except:
                print(dt[i], ' is not in the correct format')
                pause()
        print('\n\nEnter the ticker you want to compare your portfolio against . It could the ticker from a stock or an index. (Should be a yahoo finance ticker)')
        print('Enter Rate to compare you portfolio to the 10 years rate')
        print('Press enter to automatically compare your portfolio against the SP500')
        tick = input('Enter ticker ...\n').strip()
        if tick == '':
            selected_port[0].benchmark(dt[0], dt[1], index='^GSPC', plot= True, sigmas=True)
            pause()
            return 0
        elif tick == 'Rate':
            selected_port[0].benchmark(dt[0], dt[1], plot= True, sigmas=True)
            pause()
            return 0
        else:
            try:
                selected_port[0].benchmark(dt[0], dt[1], index = tick, plot= True, sigmas=True)
                pause()
                return 0
            except:
                print('The ticker you entered is not a valid ticker')
                pause()
                return 1
        return 0

def port_comp_metrics():
    while True:
        print_menu_name('Portfolio metrics comparison')
        if len(port_dict) == 1:
            print('No other portfolio load, only ', selected_port[0].name)
            print('To compare your current portfolio to another one, go to main menu and create a new portfolio, or load in ax existing portfolio')
            print('** Press 0 to go to the previous menuu')
            print('** Press 1 to go back to the main menu')
            while True:
                res = input('Enter key ...\n').strip()
                if res == '0':
                    return 0
                elif res == '1':
                    return 2
                else:
                    print('Wrong input\n')
        else:
            print('These are the currently loaded portfolio. Please enter the name of the one you want to compare you portfolio with')
            print('Press 0 to return to the previous menu')
            i = 0
            for el in port_dict.keys():
                if el != selected_port[0].name:
                    print('\t', '** ', el)
                i+=1
            p2 = input('Enter name ... \n').strip()
            if p2 == '0':
                return 0
            try:
                port_dict[p2]
            except :
                print(p2, 'is a wrong input')
                pause()
                return 1
            p2 = port_dict[p2]
            print('Enter the first and last date of your analysis, separated by a coma, in the following format')
            print('yyyymmdd, yyyymmdd')
            print('or\n,yyyymmdd, today (to go from the first date to today)')
            print('(Enter 0 to return the previous menu)')
            response = input('Enter date ... \n').strip()
            if response == '0' :
                return 0
            dt = response.split(',')
            if len(dt) != 2:
                print(response, ' is not in the correct format')
                pause()
                return 1
            for i in range(2):
                try:    
                    dt[i] = check_date(dt[i].strip())
                except:
                    print(dt[i], ' is not in the correct format')
                    pause()
                    return 1
            print(selected_port[0].metrics_comp(p2, dt[0], dt[1]))
            pause()
            return 0
        
def port_comp_port_menu():
    while True:
        print_menu_name('Portfolio comparison to portfolio')
        if len(port_dict) == 1:
            print('No other portfolio load, only ', selected_port[0].name)
            print('To compare your current portfolio to another one, go to main menu and create a new portfolio, or load in ax existing portfolio')
            print('** Press 0 to go to the previous menu')
            print('** Press 1 to go back to the main menu')
            while True:
                res = input('Enter key ...\n').strip()
                if res == '0':
                    return 0
                elif res == '1':
                    return 2
                else:
                    print('Wrong input\n')
            
        else:
            print('These are the currently loaded portfolio. Please enter the name of the one you want to compare you portfolio with')
            print('Press 0 to return to the previous menu')
            i = 0
            for el in port_dict.keys():
                if el != selected_port[0].name:
                    print('\t', '** ', el)
                i+=1
            p2 = input('Enter name ... \n').strip()
            if p2 == '0':
                return 0
            try:
                port_dict[p2]
            except :
                print(p2, 'is a wrong input')
                pause()
                return 1
            p2 = port_dict[p2]
            
            
            print('Enter the first and last date of your analysis, separated by a coma, in the following format')
            print('yyyymmdd, yyyymmdd')
            print('or\n,yyyymmdd, today (to go from the first date to today)')
            print('(Enter 0 to return the previous menu)')
            response = input('Enter date ... \n').strip()
            if response == '0' :
                return 0
            dt = response.split(',')
            if len(dt) != 2:
                print(response, ' is not in the correct format')
                pause()
                return 1
            for i in range(2):
                try:    
                    dt[i] = check_date(dt[i].strip())
                except:
                    print(dt[i], ' is not in the correct format')
                    pause()
                    return 1
            i = 0
            while i<4:
                try:
                    selected_port[0].plot_portfolios_ts(p2, dt[0], dt[1])
                    plt.show()
                    break
                except:
                    i+=1
                    time.sleep(2)
                    if i ==3 :
                        print('Sorry our server is not responding right now. Please try again later')
            pause()
            return 0

            
        
        
def portfolio_analysis_menu():
    while True:
        print_menu_name('Portfolio Analysis')
        print()
        print('** Press 1 to see main portfolio metrics')
        print('** Press 2 to see the portfolio summary')
        print('** Press 3 to access portfolio time series')
        print('** Press 4 for portfolio\'s return')
        print('** Press 5 to portfolio\'s sigma')
        print('** Press 6 to compare your portfolio to a stock or an index')
        print('** Press 7 for stock time series')
        print('** Press 8 to compare you portfolio to another portfolio')
        print('** Press 9 to compare your portfolio\'s metrics to another portfolio\'s')
        print('** Press 0 to return to the previous menu')
        response = input('Enter a key ... \n').strip()
        nb = True
        try:
            response = int(response)
        except:
            nb=False
            print('Please input a number\n')
        if nb:
            if response in [1,2,3,4,5,6,7,8,9,0]:
                return response
            else:
                print('Wrong input, plus use one of the given choices')
                
def portfolio_metrics():
    print_menu_name('metrics')
    while True:
        print('Enter start and end date as yyyymmdd, yyyymmdd\n(you can use "today" (spelled today) for the last day')
        print('Press 0 to return to the previous menu')
        dt = input('Enter date ...\n').strip()
        if dt == '0':
            return 0
        else:
            dt = dt.split(',')
            
            try:
                dt[0] = check_date(dt[0].strip())
                dt[1] = check_date(dt[1].strip())
                break
            except:
                print('Wrong date input\n')
    print(selected_port[0].ptf_summary(dt[0], dt[1]))
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
        print('Press 0 to return to the previous menu')
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
                a = selected_port[0].ptf_tms(dt[0], dt[1], rebalancing = True)
                print(a)
                (a/a.iloc[0]).plot(figsize=(8,8), label='Portfolio', legend=True, title='With rebalancing, weights change are held constant')
                plt.show()
                print('This is the evolution of the portfolio with rebalancing')
                print()
                pause()
                b = selected_port[0].ptf_tms(dt[0], dt[1], rebalancing= False)
                print(b)
                (b/b.iloc[0]).plot(figsize=(8,8), label='Portfolio', legend=True, title='Without rebalancing, weights change with price (most realistic option)')
                plt.show()
                print('This is the evolution of the portfolio without rebalancing')
                input('Enter an key to continue ... ')
                return 0
    return 0

def stock_tms():
    print_menu_name('time series stock')
    while True:
        print('Enter start and end date as yyyymmdd, yyyymmdd\n(you can use "today" (spelled today) for the last day')
        print('Press 0 to return to the previous menu')
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
        print('Press 0 to return to the previous menu')
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
        print('Press 0 to return to the previous menu')
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
                print_menu_name('Sigma')
                print('Annualized sigma :',selected_port[0].get_sigma(dt[0], dt[1], annualized=True))
                print('Non annualized sigma :',selected_port[0].get_sigma(dt[0], dt[1], annualized=False))
                input('Enter any key to continue ...')
                return 0

                

def main():
    
    current = 'main_menu()'
    while True:
        try: 
            response = eval(current)

            if current == 'main_menu()':
                if response == 1:
                    current = 'stock_menus.stock_menu()'
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
            elif current == 'stock_menus.stock_menu()':
                current = 'main_menu()'

            elif current == 'load_portfolio_menu()':
                if response == 1: current = 'main_menu()'
                elif response == 2 : current = 'load_portfolio_menu()'

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
                if response == 3 : current = 'remove_stock_menu()'

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
                if response == 6 : current = 'port_comp_menu()'
                if response == 7 : current = 'stock_tms()'
                if response == 8 : current = 'port_comp_port_menu()'
                if response == 9 : current = 'port_comp_metrics()'
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

            elif current == 'port_comp_menu()':
                if response == 0: current = 'portfolio_analysis_menu()'
                if response ==1 : current = 'port_comp_menu()'

            elif current == 'port_comp_port_menu()':
                if response == 0: current = 'portfolio_analysis_menu()'
                if response == 1 : current = 'port_comp_port_menu()'
                if response == 2 : current = 'main_menu()'

            elif current == 'port_comp_metrics()':
                if response == 0: current = 'portfolio_analysis_menu()'
                if response == 1 : current = 'port_comp_metrics()'
                if response == 2 : current = 'main_menu()'
        except:
            print('An error occured. You are being redirected to the main menu. The last version of your loaded prtfolios should be there')
            current = 'main_menu()'
            pause()
        
    print_menu_name('Exit')
    L = os.listdir(r'Saved')
    L2 = []
    if len(L)>0:
        for el in L:
            if el.split('_')[0] != 'base':
                L2.append(el.split('.csv')[0])
                
                
    for p in list(port_dict.values()):
        if not p.name in L2:
            print('Portfolio :', p.name, 'has not been saved.')
            print('Do you want to save it?')
            print('** press 0 to quit immediately and stop saveing checks')
            print('** Press 1 to save the portfolio :', p.name)
            print('** Press 2 to save all portfolios')
            loop2=True
            stp=False
            while loop2:
                res = input('Enter a key ...').strip()
                if res == '0':
                    stp= True
                    loop2=False
                elif res == '1':
                    p.save_port()
                    stp=False
                    loop2=False
                elif res == '2':
                    for p in port_dict.values():
                        p.save_port()
                    stp=True
                    loop2=False
                else:
                    print('Wrong input\n')
            if stp:
                break     
        else:
            temp = Portfolio()
            temp.load_in(p.name)
            if not p._portfolio.equals(temp._portfolio):
                print('Portfolio :', p.name, 'has been edited but not saved.')
                print('Do you want to save the modifications?')
                print('** press 0 to quit immediately and stop saveing checks')
                print('** Press 1 to save the portfolio :', p.name)
                print('** Press 2 to save all portfolios')
                loop2=True
                stp = False
                while loop2:
                    res = input('Enter a key ...').strip()
                    if res == '0':
                        stp= True
                        loop2=False
                    elif res == '1':
                        p.save_port()
                        stp=False
                        loop2=False
                    elif res == '2':
                        for p in port_dict.values():
                            p.save_port()
                        stp=True
                        loop2=False
                    else:
                        print('Wrong input\n')
                if stp:
                    break    
                

                
    print_menu_name('Program successfully closed')
   
if __name__ == '__main__':

    warnings.filterwarnings("ignore")
    main()
    

    
    
