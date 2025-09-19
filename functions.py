from datetime import datetime as dt
import pandas as pd
import os

### Start the log file
with open("system.log",'w') as f:
    f.write(f'{dt.now()}\tSystem Start\n')

### Functions
def dist(plot1:list[int],plot2:list[int]):
    '''
    Calculate distance between 2 points
    '''
    return sum([abs(customer-merchant) for customer,merchant in zip(plot1,plot2)])

def log(message:str):
    with open("system.log",'a') as f:
        print(message)
        f.write(f'{dt.now()}\t{message}\n')

def clearFolder():
    for filename in os.listdir('./figures'):
        filepath=os.path.join('./figures',filename)
        if os.path.isfile(filepath):
            os.remove(filepath)

def createList(csv,createdClass):
    itemCSV=pd.read_csv(csv).to_dict(orient='records')
    return [createdClass(item) for item in itemCSV]