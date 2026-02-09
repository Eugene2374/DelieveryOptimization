from functions import *

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
        self.history=[]

    def move(self):
        curr=self.pos
        self.setDestination()
        from main import logRiders
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

MerchantList= createList('csv/Merchant.csv',Merchant)
merchantCentre=centre(MerchantList)