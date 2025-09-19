size=(10,10)
totalMerchants=10
totalRiders=20
totalCustomers=100
loadTime=50
capacity=2


import random as rd
import pandas as pd

Board={
    'x':size[0],
    'y':size[1],
}

merchants = {
    'x': [rd.randint(0,Board['x']) for i in range(totalMerchants)],
    'y': [rd.randint(0,Board['y']) for i in range(totalMerchants)],
}

riders = {
    'x':[rd.randint(0,Board['x']) for i in range(totalRiders)],
    'y':[rd.randint(0,Board['y']) for i in range(totalRiders)],
    'capacity': capacity,
}

customers = {
    'x': [],
    'y': [],
    'time':[],
    'merchant':[]
}

for i in range(totalCustomers):
    customers['x'].append(rd.randint(0,Board['x']))
    customers['y'].append(rd.randint(0,Board['y']))
    customers['time'].append(rd.randint(0,loadTime))
    customers['merchant'].append(rd.randint(0,len(merchants['x'])-1))
    while any(customers['x'][-1]==x and customers['y'][-1]==y for x,y in zip(*merchants.values())):
        customers['x'][-1]=rd.randint(0,Board['x'])
        customers['y'][-1]=rd.randint(0,Board['y'])

customers['time'].sort()

df_merch = pd.DataFrame(merchants)
df_rider = pd.DataFrame(riders)
df_cust = pd.DataFrame(customers)

df_merch.index.name='id'
df_rider.index.name='id'
df_cust.index.name='id'

df_cust.to_csv('csv/Customer.csv')
df_merch.to_csv('csv/Merchant.csv')
df_rider.to_csv('csv/Rider.csv')

