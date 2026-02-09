import matplotlib.pyplot as plt
import numpy as np
from functions import *
from assignment import *
from Grid import Grid
from UserClasses import Rider, Customer, MerchantList, merchantCentre

class Simulation:
    def __init__(self,alpha,beta):
        orderTimes= [*{*pd.read_csv('csv/Customer.csv').get('time')}]
        orderTimes.sort()
        RiderList=createList('csv/Rider.csv',Rider)
        CustomerList=createList('csv/Customer.csv',Customer)
        from main import plot, mode
        time=0
        previousOrderTime=0
        if mode ==0:
            P2={rider:[rider,0] for rider in RiderList}
        elif mode ==1:
            P2= merchantCentre
        # choice, Total=fCostMatrix({rider:[rider,0] for rider in RiderList},min(orderTimes),len(orderTimes))
        while not all([customer.done for customer in CustomerList]):
            log(f'Step {time}')
            currOrders=[order for order in CustomerList if order.appearTime<=time and not order.done]
            if any(currOrders):
                [customer.increase() for customer in currOrders]

            if plot:
                map=Grid()
                map.plot_map(MerchantList,currOrders,RiderList,time)

            if time in orderTimes:
                orderAppear=[order for order in CustomerList if order.appearTime==time]
                orderDone=[order for order in CustomerList if order.appearTime>previousOrderTime and order.done]
                P2=assignment(mode,orderAppear,orderDone,RiderList,P2,alpha,beta,time)
                previousOrderTime=time

            [rider.move() for rider in RiderList]
            time+=1

        ### Analysis
        if plot:
            map=Grid()
            map.plot_map(MerchantList,[],RiderList,time)

        self.assignment={rider.id:[customer.id for customer in rider.history] for rider in RiderList}
        finishing=[customer.done for customer in CustomerList]
        WaitTime=[customer.waitTime for customer in CustomerList]
        PlannedTime=[customer.plannedTime for customer in CustomerList]
        Done=[a for a,b in zip(WaitTime,finishing) if b]
        Delays=[a-b for a,b,c in zip(WaitTime,PlannedTime,finishing) if c]

        self.Delay=sum(Delays)/len(Delays)
        log(f'All Done? : {all(finishing)}')
        log(f'Customer Waiting time: {sum(Done)/len(Done)}')
        log(f'Customer Delayed time: {self.Delay}')
        plt.scatter(np.array(range(len(Delays))),np.array(Delays))
        plt.savefig('Delay Distribution')