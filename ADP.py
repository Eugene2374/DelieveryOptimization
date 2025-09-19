import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from functions import *

from scipy.optimize import linear_sum_assignment

### Classes
class User:
    def __init__(self,init):
        self.id=init['id']
        self.pos=[init['x'],init['y']]

    def dist(self,item):
        return dist(self.pos,item.pos)

class Customer(User):
    def __init__(self,init):
        #Initialize
        super().__init__(init)
        self.merchant=MerchantList[init['merchant']]
        
        #Time
        self.appearTime=init['time']
        self.plannedTime= self.dist(self.merchant)
        self.waitTime=0

        #Switch
        self.done=False
        self.totalDist= sum([self.dist(merchant) for merchant in MerchantList])

    def increase(self):
        if not self.done:
            self.waitTime+=1
    
class Merchant(User):
    def __init__(self, init):
        super().__init__(init)

class Rider(User):
    def __init__(self, init):
        super().__init__(init)
        self.capacity=init['capacity']
        self.destination=self.pos
        self.route=[]

    def move(self):
        curr=self.pos
        self.setDestination()
        if logRiders:
            log(f'Rider {self.id}:{(curr,self.destination)}')
        # Move to Destination
        if curr[0]<self.destination[0]:
            curr[0]+=1
        elif curr[0]>self.destination[0]:
            curr[0]-=1
        elif curr[1]<self.destination[1]:
            curr[1]+=1
        elif curr[1]>self.destination[1]:
            curr[1]-=1

    def setDestination(self):
        if any(self.route) and self.dist(self.route[0])==0:
            if isinstance(self.route[0],Customer):
                self.route[0].done=True
                log(f'Order {self.route[0].pos} is done with waiting time {self.route[0].waitTime}')
            self.route.pop(0)

        # Going through Route
        if any(self.route):
            self.destination=self.route[0].pos
        else:
            self.destination=self.pos

class Grid:
    def __init__(self):
        clearFolder()
        merchantPos=pd.read_csv('csv/Merchant.csv')
        customerPos=pd.read_csv('csv/Customer.csv')
        self.grid=(max(*customerPos['x'],*merchantPos['x'])+1,max(*customerPos['y'],*merchantPos['y'])+1)

    def plot_map(self, MerchantList, CustomerList, RiderList, step):
        '''
        Plot merchants, customers, and riders on a grid.
        Merchants: Red squares, Customers: Blue dots, Riders: Green triangles.
        Saves plot as an image for each step.
        '''
        plt.figure(figsize=(10, 10))
        # Plot grid
        plt.grid(True)
        plt.xlim(-0.5, self.grid[0] - 0.5)
        plt.ylim(-0.5, self.grid[1] - 0.5)
        plt.xticks(range(self.grid[0]))
        plt.yticks(range(self.grid[1]))
        plt.xlabel('X Coordinate')
        plt.ylabel('Y Coordinate')
        plt.title(f'Simulation Step {step}')

        # Plot merchants
        for i, merchant in enumerate(MerchantList):
            plt.scatter(merchant.pos[0], merchant.pos[1], c='red', marker='s', s=100, label='Merchant' if i == 0 else "")
            plt.text(merchant.pos[0] + 0.2, merchant.pos[1], f'M{merchant.id}', fontsize=10, color='red')

        # Plot customers
        for i, customer in enumerate(CustomerList):
            if not customer.done:
                plt.scatter(customer.pos[0], customer.pos[1], c='blue', marker='o', s=50, label='Customer' if i == 0 else "")
                plt.text(customer.pos[0] + 0.2, customer.pos[1], f'C{customer.id} ({customer.waitTime})', fontsize=8, color='blue')

        # Plot riders and their paths
        for i, rider in enumerate(RiderList):
            plt.scatter(rider.pos[0], rider.pos[1], c='green', marker='^', s=100, label='Rider' if i == 0 else "")
            plt.text(rider.pos[0] + 0.2, rider.pos[1], f'R{rider.id}', fontsize=10, color='green')

        plt.legend()
        plt.savefig('figures/%.4f.png'%(step/10000),dpi=100)
        plt.close()

class Simulator:
    def __init__(self):
        ### Initiating
        global logRiders,plot, MerchantList,RiderList,CustomerList,orderTimes, Beta
        from main import logRiders, plot, Beta

        orderTimes= [*{*pd.read_csv('csv/Customer.csv').get('time')}]
        orderTimes.sort()
        MerchantList= createList('csv/Merchant.csv',Merchant)
        RiderList=createList('csv/Rider.csv',Rider)
        CustomerList=createList('csv/Customer.csv',Customer)

        if plot:
            map=Grid()
        
        state={rider:[rider,0] for rider in RiderList}
        time=0
        # choice, Total=fCostMatrix({rider:[rider,0] for rider in RiderList},min(orderTimes),len(orderTimes))
        while not all([customer.done for customer in CustomerList]):
            log(f'Step {time}')
            currOrders=[order for order in CustomerList if order.appearTime<time and not order.done]
            if any(currOrders):
                [customer.increase() for customer in currOrders]

            if time in orderTimes:
                choice=fCostMatrix(state,time)
                for rider,order in choice:
                    state[rider]=[order,max(state[rider][1],time)+order.plannedTime]
                    rider.route.append(order.merchant)
                    rider.route.append(order)

            if plot:
                map.plot_map(MerchantList,currOrders,RiderList,time)
            [rider.move() for rider in RiderList]
            time+=1
        
        ### Analysis
        finishing=[customer.done for customer in CustomerList]
        WaitTime=[customer.waitTime for customer in CustomerList]
        PlannedTime=[customer.plannedTime for customer in CustomerList]
        Done=[a for a,b in zip(WaitTime,finishing) if b]
        Delays=[a-b for a,b,c in zip(WaitTime,PlannedTime,finishing) if c]

        log(f'All Done? : {all(finishing)}')
        log(f'Customer Waiting time: {sum(Done)/len(Done)}')
        log(f'Customer Delayed time: {sum(Delays)/len(Delays)}')
        plt.scatter(np.array(range(len(Delays))),np.array(Delays))
        plt.savefig('Delay Distribution')

def fCostMatrix(state,currTime):
    orderList=[order for order in CustomerList if currTime==order.appearTime]
    CostMatrix=pd.DataFrame({order:[state[rider][0].dist(order.merchant)+order.plannedTime+max(state[rider][1],currTime)+Beta*order.totalDist for rider in RiderList] for order in orderList})
    minCostR,minCostO= linear_sum_assignment(CostMatrix)
    choice = zip([RiderList[rider] for rider in minCostR],[orderList[order] for order in minCostO])
    return choice

    
import main