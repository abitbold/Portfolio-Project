from Portfolio import Portfolio
import pandas as pd

def stock_universe():
        stats = pd.read_csv('comptick.csv')
        return (stats)

def stock_timeseries(ticker, first = 'last_week', last = 'today'):
    p = Portfolio(ticker)
    return (p.get_timeseries(first, last))

def stock_return(ticker, first = 'last_week', last = 'today', annualized = False):
    p = Portfolio(ticker)
    return (p.get_return(first, last, annualized = annualized))

def stock_sigma(ticker, first = 'last_week', last = 'today', annualized = True):
    p = Portfolio(ticker)
    return (p.get_sigma(first, last, annualized = annualized))
