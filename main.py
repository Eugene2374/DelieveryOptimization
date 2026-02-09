from functions import log
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

startTime=datetime.now()
logRiders=False
plot=False
setup=False
focus=True
RiderNo=0
step=0.1
mode=1 ## mode: 0 if old, 1 if new

if __name__=='__main__':
    if setup:
        from setup import *

    stepList=[np.round(i*step,len(str(step).split('.')[1])) for i in range(int(1/step))]
    DelayData=pd.DataFrame(index=stepList,columns=stepList)
    Assignment=[]

    from Simulation import Simulation

    for alpha in stepList:
        for beta in stepList:
            Data=Simulation(alpha,beta)
            DelayData.loc[alpha,beta]=Data.Delay
            if Assignment==[] or Data.Delay< Assignment[0]:
                Assignment=[Data.Delay,pd.DataFrame([Data.assignment])]


    ColorMapping= DelayData.astype(float)
    log(f'Delay Time: {Assignment[0]}\n{'-'*30}')
    log(Assignment[1])
    
    plt.figure(figsize=(10, 10))
    plt.xlabel('Alpha')
    plt.ylabel('Beta')
    plt.title('Optimal assignment')
    sns.heatmap(ColorMapping, annot=True, cmap='RdYlGn_r', fmt=".2f", linewidths=.5)
    plt.savefig('Optimal Chart')
    
    if plot:
        print()
        log('Converting into video:')
        import convert

    print()
    log(f'Program runtime:{datetime.now()-startTime}')