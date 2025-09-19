from functions import log
from extract import extract

logRiders=False
plot=False
setup=False
focus=True
Beta=0.2

RiderNo=0

from ADP import *
# from linearProgram import * 
# from UnplannedLP import * 
# from oldLinearProgram import * 
# from basic import *

if __name__=='main':
    if setup:
        from setup import *

    Simulator()

    if plot:
        log('\nConverting into video:')
        import convert
    
    if focus and logRiders:
        extract(RiderNo)