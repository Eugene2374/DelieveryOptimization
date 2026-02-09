import pandas as pd
from functions import *
from scipy.optimize import linear_sum_assignment
from UserClasses import merchantCentre 


def assignment(Mode, OrderIn, OrderOut, RiderList:pd.Series,P2i,alpha,beta,currTime):
    if Mode==0:
        CostMatrix=pd.DataFrame({order:[P2i[rider][0].dist(order.merchant)+order.plannedTime+max(P2i[rider][1],currTime)+alpha*order.totalDist for rider in RiderList] for order in OrderIn})
        minCostR,minCostO= linear_sum_assignment(CostMatrix)
        choice=zip([RiderList[rider] for rider in minCostR],[OrderIn[order] for order in minCostO])
        for rider,order in choice:
            P2i[rider]=[order,max(P2i[rider][1],currTime)+order.plannedTime]
            rider.route.extend([order.merchant,order])
            rider.history.append(order)
        return P2i
    
    elif Mode==1:
        P2=listFDiv(1,listSum(listMult(beta,P2i),listMult((1-beta),listSum(centre(OrderIn),listMult(-1,centre(OrderOut))))))
        for order in OrderIn:
            orderMap={}
            riderEnd=[rider.route[-1] if len(rider.route)>0 else rider for rider in RiderList]
            for index in range(len(riderEnd)):
                dummy=riderEnd.copy()
                dummy[index]=order
                orderMap[RiderList[index]]=[dist(listSum(listMult(alpha,centre(dummy)),listMult(1-alpha,P2)),merchantCentre)]
            index,value=linear_sum_assignment(pd.DataFrame(orderMap))
            [RiderList[i].route.extend([order.merchant,order]) for i in value]
            [RiderList[i].history.append(order) for i in value]
        return P2