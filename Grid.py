from functions import *
import matplotlib.pyplot as plt 

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

from UserClasses import Rider, Customer, MerchantList, merchantCentre
orderTimes= [*{*pd.read_csv('csv/Customer.csv').get('time')}]
orderTimes.sort()
RiderList=createList('csv/Rider.csv',Rider)
CustomerList=createList('csv/Customer.csv',Customer)

map=Grid()
map.plot_map(MerchantList,CustomerList,RiderList,0)
