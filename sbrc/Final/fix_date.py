import pandas as pd
import re

def is_nan(x):
    return (x != x)

def fix_date(date):
    if(not is_nan(date)):
        try:
            date = removeTime(date)
            date = handleZeros(date)
        except:
            pass
    return date

def removeTime(string_date):                                                                                          
    # removes the `at 18:00 am` part of the date                                                                            
    response = re.sub(r"([0-1]?[0-9]|2[0-3]):[0-5][0-9]", '', str(string_date))                                                          
    response = response.replace('at ', '')                                                                                  
    response = response.replace('am ', '')                                                                                  
    response = response.replace('pm ', '')                                                                                                                                                                                                          
    response = response.replace('at', '')                                                                                   
    response = response.replace('am', '')                                                                                   
    response = response.replace('pm', '')                                                                                   
    return response

def handleZeros(date):
    date_arr = date.split('/')
    day = date_arr[1]
    month = date_arr[0]
    year = date_arr[2]
    
    def hzero(n):
        n = int(n)
        if n < 10:
            return '0'+str(n)
        else:
            return n

    return str(hzero(day))+"/"+str(hzero(month))+"/"+str(year)

df = pd.read_csv('./Facebook/facebook.csv')
df['facebok_date_parsed'] = df['facebok_date_parsed'].apply(lambda x: fix_date(x))
df['date'] = df['date'].apply(lambda x: fix_date(x))

df.to_csv('facebook_fixed_date.csv')
