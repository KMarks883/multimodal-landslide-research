import piplates.DAQCplate as DAQC
import time

for i in range(0,7):
    time.sleep(0.5)
    DAQC.setDOUTbit(0,i)

for i in range(0,7):
    time.sleep(0.5)
    DAQC.clrDOUTbit(0,6-i)