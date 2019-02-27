## file name : stock_menus.py
## 
## team member:
##      Arjun Alagappan
##      David Abitbol
##      Cody Cao
##      Lily li
##      Shanshan Liu
##      Kurtis Lee
##
## This file contains the menus and control the floes for the stock analysis functionality
## This file imports: Portfolio.py, yahoo.py, stock.py, options_module.py
## This file is imported by: mainmenu.py

from stock import *
from Portfolio import *
from func import *
import os
import time
from options_module import *
from yahoo import *

def check_positive(i):
    if i <= 0:
        raise Exception("Number not positive.")
    
def cs():
    # clears the screen
    os.system('cls')


def stock_explore(ticker_interest = None, options = False):
    cs()
    print("Loading universe of stocks...")
    univ = stock_universe()
    print("Universe loaded...")
    time.sleep(2)
    cs()
    
    empty_port = Portfolio()
    new_tick_list = []
    while True:    
        print("Select a stock:")
        print('''
              1. Enter ticker\n
              2. Select by filters\n
              0. Exit to main menu
              ''')
        good_keys = ['1','2','0']
        key = input("Enter a key: ")
        while key not in good_keys:
            cs()
            print("Invalid key.")
            print("Select a stock:")
            print('''
              1. Enter ticker\n
              2. Select by filters\n
              0. Exit to main menu
              ''')
            key = input("Enter a key: ")
        if key == '1':
            # search by stock list
            print("Selecting by ticker...")
            time.sleep(2)
            cs()
            nticks = input("Enter how many tickers you would like to see: ")
            try:
                nticks = int(nticks)
                check_positive(nticks)
            except:
                nticks = 5
                print("Invalid entry. Default selection for 5 stocks")
            stks = 0
            time.sleep(2)
            cs()
            while stks < nticks:
                new_tick = input("Enter a ticker: ")
                if new_tick in univ.loc[:,'Ticker'].values and new_tick not in new_tick_list:
                    new_tick_list.append(new_tick)
                    stks += 1
                elif new_tick in new_tick_list:
                    print("Ticker already included.")
                    k = input('''Press 1 to choose a new stock. Any other key
                              to continue on''')
                    if k == '1':
                        continue
                    else:
                        stks += 1
                elif new_tick not in univ.loc[:,'Ticker'].values:
                    print("Ticker not found. Choose another ticker.")
                    continue
                cs()
                print("Current selection: ")
                for idx, val in enumerate(new_tick_list):
                    print(str(idx+1) + '. ', val, sep = '\t')
            print("Stocks chosen!")
            time.sleep(2)
            if options:
                return options_menu(new_tick_list)
            return stock_menu(new_tick_list)
                
        elif key == '2':
            # ask for filters
            n = input("Number of stocks from filter: ")
            try:
                n = int(n)
                check_positive(n)
            except:
                print("Invalid entry. Defaulted to 5.")
                n = 5
            filter_d = {'Market Cap (intraday)': [0,0], 'Beta (3Y Monthly)':[0,0],
                          'Quarterly Revenue Growth':[0,0]}
            for key,value in filter_d.items():
                print('\t' + key)
                low = input("Enter minimum (0 for default min): ")
                high = input("Enter maximum (0 for default max): ")
                try:
                    low = float(low)
                    high = float(high)
                except:
                    print("Invalid numbers")
                    low = 0
                    high = 0
                value[0] = low
                value[1] = high
            empty_port.create_filter_port(filter_d, n)
            new_tick_list = list(empty_port._portfolio.index)
            print("Stocks chosen!")
            time.sleep(3)
            if options:
                return options_menu(new_tick_list)
            return stock_menu(new_tick_list)
        elif key == '0':
            return stock_menu()

def stock_statistics(stock_list):
    cs()
    if not stock_list:
        print("No stocks selected...")
        time.sleep(1)
        print("Transferring to stock selector...")
        time.sleep(2)
        return stock_explore()
    n = len(stock_list)
    print("Choose a security to view all the statistics for. Enter the id: ")
    for idx, val in enumerate(stock_list):
        print(str(idx+1) + '. ', val, sep = '\t')
    print(str(n + 1) + '. \tView statistics for all')
    print('0. \tReturn to menu')
    sec = input("Enter a key: ")
    try:
        sec = int(sec)
        if sec == 0:
            raise ValueError
        elif sec == n + 1:
            raise IndexError
        choice = stock_list[sec-1]
    except IndexError:
        choice = 0
    except ValueError:
        choice = 'ret'
    
    if choice == 0:
        for k in stock_list:
            print(k)
            data = get_stats_data(k)
            print(data.transpose())
            input("Enter to continue.")
            print("---------------------------------------\n\n")
    elif choice == 'ret':
        return stock_menu(stock_list)
    else:
        print(choice)
        data = get_stats_data(choice)
        print(data.transpose())
    input("Enter to continue: ")
    cs()
    return stock_statistics(stock_list)
    

def stock_financials(stock_list):
    cs()
    if not stock_list:
        print("No stocks selected...")
        time.sleep(1)
        print("Transferring to stock selector...")
        time.sleep(2)
        return stock_explore()
    n = len(stock_list)
    print("Choose a security for which to view financials. Enter the id: ")
    for idx, val in enumerate(stock_list):
        print(str(idx+1) + '. ', val, sep = '\t')
    print(str(n + 1) + '. \tView financials for all')
    print('0. \tReturn to menu')
    sec = input("Enter a key: ")
    try:
        sec = int(sec)
        if sec == 0:
            raise ValueError
        elif sec == n + 1:
            raise IndexError
        choice = stock_list[sec-1]
    except IndexError:
        choice = 0
    except ValueError:
        choice = 'ret'
    
    if choice == 0:
        for k in stock_list:
            print(k)
            data = get_financial_data(k)
            print(data)
            input("Enter to continue.")
            print("---------------------------------------\n\n")
    elif choice == 'ret':
        return stock_menu(stock_list)
    else:
        print(choice)
        data = get_financial_data(choice)
        print(data)
    input("Enter to continue: ")
    cs()
    return stock_financials(stock_list)


def stock_comparisons(stock_list = None):
    cs()
    if not stock_list or len(stock_list) < 2:
        print("Not enough/no stocks selected...")
        time.sleep(1)
        print("Transferring to stock selector...")
        time.sleep(2)
        return stock_explore()

    print("Choose two stocks to compare: ")
    for idx,val in enumerate(stock_list):
        print(str(idx + 1)+'. ', val, sep ='\t')
    
    while True:
        t1 = input("Enter TICKER of first stock: ")
        t2 = input("Enter TICKER of second stock: ")
        if t1 in stock_list and t2 in stock_list and t1 != t2:
            break
        print("Invalid ticker symbols. ")
    cs()
    print("You've chosen " + t1 + " and " + t2)
    
    p1 = Portfolio(t1, name = t1)
    p2 = Portfolio(t2, name = t2)
    d1 = '2018-01-01'
    d2 = '2019-01-01'
    print('''Default date range:\n
        Start: 2018-01-01
        End:   2019-01-01
        ''')
    k = input("Press 'y' if you'd like to change the dates: ")
    if k == 'y':
        newstart = input("Enter start date in YYYY-MM-DD format: ")
        newend = input("Enter end date in YYYY-MM-DD format: ")
        d1 = newstart
        d2 = newend
    
    print(t1 + " vs. " + t2)
    p1.plot_portfolios_ts(p2, d1, d2)
    print("\n\n\n")
    input("Enter to continue...")
    cs()
    print(t1 + " vs. SP500")
    cor1 = p1.benchmark(d1, d2, index = '^GSPC', plot = True)
    
    print(t2 + " vs. SP500")
    cor2 = p2.benchmark(d1, d2, index = '^GSPC', plot = True)
    print("\n\n\n\n")
    print("Correlation with SP500: ")
    print(t1 + ": " + str(cor1))
    print(t2 + ": " + str(cor2) + '\n')
    
    input("Enter to continue...")
    cs()
    
    print(t1, p1.ptf_summary(d1, d2), sep = '\n')
    print("-----------------------")
    print(t2, p2.ptf_summary(d1, d2), sep = '\n')
    print("-----------------------")
    input("Enter to continue...")
    cs()
    
    print('''
          1. Return to stock menu
          2. Compare two stocks
          ''')
    while True:
        k = input("Enter a key: ")
        if k == '1':
            return stock_menu(stock_list)
        elif k == '2':
            return stock_comparisons(stock_list)
        else:
            print("Invalid key.")
            cs()
    
    
    
def options_menu(stock_list = None):
    cs()
    if not stock_list:
        print("No stocks selected...")
        time.sleep(1)
        print("Transferring to stock selector...")
        time.sleep(2)
        return stock_explore(options = True)
    
    print("Gathering options data for selected stocks...")
    time.sleep(2)
    df, df_atm, df_straddle = get_options_dfs(stock_list)
    
    print("Options data collected successfully!")
    time.sleep(2)
    
    while True:
        cs()
        print("Welcome to PokeQuant Options!")
        print(''' 
              1. View PokeQuant's recommended option buys\n    
              2. Top 3 Bears, Top 3 Bulls\n
              3. Visuals:\n
                  a. Volatility Skew\n
                  b. Mispricing Scatterplot\n
                  c. Mispricing Histogram\n
                  d. Straddle Payoffs\n
              4. Select a new list of stocks\n
              0. Return to stocks menu\n
              ''')
        k = input("Enter a key: ")
        if k == '1':
            get_pq_recommendation(df, 'Bullish')
            get_pq_recommendation(df, 'Bearish')
            print('-----')
            input("Enter to return to options menu: ")
            
        elif k == '2':
            get_top3(df)
            input("Enter to return to options menu: ")
            
        elif k == '3':
            while True:
                cs()
                print("Visuals")
                print('''
                      a. Volatility Skew\n
                      b. Mispricing Scatterplot\n
                      c. Mispricing Histogram\n
                      d. Straddle Payoffs\n
                      0. Return to options menu\n
                      ''')
                key = input("Enter a key: ")
                if key == 'a':
                    print("Viewing volatility skew plots of ATM options...\n")
                    time.sleep(2)
                    options_visualization_vol_skew(df_atm)
                elif key == 'b':
                    print("Viewing mispricing scatterplot...\n")
                    time.sleep(2)
                    options_visualization_mispricing_scat(df)
                elif key == 'c':
                    print("Viewing mispricing histogram...\n")
                    time.sleep(2)
                    options_visualization_mispricing_hist(df)
                elif key == 'd':
                    print("Straddle payoffs: \n")
                    for idx, val in enumerate(stock_list):
                        print(str(idx+1) + '. ', val, sep = '\t')
                    
                    choice = input("Enter a ticker: ")
                    while choice not in stock_list:
                        choice = input("Not in this list. Enter a ticker: ")
                    print("\n\n")
                    date = input("Enter the expiry date (YYYY-MM-DD): ")
                    print("Attempting to plot...")
                    time.sleep(3)
                    try:
                        date = check_date(date)
                        options_visualization_straddle_payoff(df_straddle,choice, date)
                    except:
                        print("Exiting to options menu...")
                        time.sleep(3)
                        break
            
        elif k == '4':
            print("Selecting new stocks...")
            time.sleep(2)
            return stock_explore(options = True)
        elif k == '0':
            print("Returning to main menu")
            time.sleep(2)
            return stock_menu(stock_list)
        else:
            continue
            
    
    
    
        

def stock_menu(stock_list = None):
    cs()
    if stock_list:
        print("Current stock list.")
        for idx, val in enumerate(stock_list):
            print(str(idx + 1) + '.', val, sep = '\t')
        print('---------------------------------')
        print("Press 1 to clear the list")
        print("Any other key to continue.")
        key = input("Enter a key:\n")
        print('---------------------------------')
        if key == '1':
            stock_list = []
            print("Stock list has been cleared!")
            time.sleep(2)
            cs()
    
    print("Stock Menu")
    print('''
          1. Selector\n
          2. Statistics\n
          3. Financials\n
          4. Comparisons\n
          5. Options Menu\n
          0. Exit to main menu.
          ''')
    
    key = input("Enter a key: ")
    good_keys = ['1','2','3','4','5','0']
    while key not in good_keys:
        print('''
          1. Selector\n
          2. Statistics\n
          3. Financials\n
          4. Comparisons\n
          5. Options Menu\n
          0. Exit to main menu.
          ''')
        key = input("Please enter a valid key.")
    
    if key == '1':
        print("Exploring stock universe...")
        time.sleep(3)
        return stock_explore()
    elif key == '2':
        print("Stock statistics...")
        time.sleep(3)
        stock_statistics(stock_list)
    elif key == '3':
        print("Stock financials...")
        time.sleep(3)
        stock_financials(stock_list)
    elif key == '4':
        print("Comparing stocks...")
        time.sleep(3)
        stock_comparisons(stock_list)
    elif key == '5':
        print("Looking at options data")
        time.sleep(3)
        return options_menu(stock_list)
    elif key == '0':
        return 25
    return 1


if __name__ == '__main__':
    stock_menu()   
