# Functions used with the portfolio class

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
    
