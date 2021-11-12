###########################################################################################################################################################################      
##                                                                                                                                                                        ##
##          This is a low-functionality script for simply testing the load cells. This does not contain the additional functionality or code of the production script.    ##
##          To reduce the amount of complexity and increase the readability of the code.
##
##                                                                                                                                                                        ##
###########################################################################################################################################################################




from time import sleep, strftime, time
import sys
import datetime 
import asyncio
import matplotlib.pyplot as plt
import keyboard
import glob

from bluedot.btcomm import BluetoothClient
from signal import pause
#Set up HX711 Driver
EMULATE_HX711=False
if not EMULATE_HX711:
    import RPi.GPIO as GPIO
    from hx711 import HX711
else:
    from emulated_hx711 import HX711

#Exit Function
def cleanAndExit():
    print("Cleaning.")
    if not EMULATE_HX711:
        GPIO.cleanup()
    print("Bye.")
    sys.exit()

hx = HX711(20, 21)
hx2 = HX711(17, 27)
hx3 = HX711(20, 21)

hx.set_reading_format("MSB", "MSB")

def TareItUp ():
   hx.tare()
   hx2.tare()
   hx3.tare()
       
keyboard.add_hotkey('0', TareItUp)
#Load cells return a value based on variation within voltage, the reference unit is a coefficient of that reading.
#Therefore, the reference unit must be emperically found and set to the desired value for your desired unit.

# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# 
# Calculate referenceUnit: set it to 1, then place a known weight on the scale, then the (reference unit = reported weight / actual weight)
#
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


referenceUnit1 = 100
referenceUnit2 = 100
referenceUnit3 = 100

hx.set_reference_unit(referenceUnit1)
hx.reset()
hx.tare()

hx2.set_reference_unit(referenceUnit2)
hx2.reset()
hx2.tare()

hx3.set_reference_unit(referenceUnit3)
hx3.reset()
hx3.tare()

#displays connection errors from server (dont want this to happen)
def data_received(D):
    print(D)

#initiate client connection 
c = BluetoothClient("B8:27:EB:8F:E8:F8", data_received)


arr = []
arr2 = []
arr3 = []

def getAverage(): #returns the average of all data points in the list. 
    return (sum(arr2[len(arr2) - 5:len(arr2) - 1])/5) + 2

movingaverage = 1 #This is holds the moving average that will be used to determine recording frequency

plt.axis([0,30,-100,100])
plt.ion()
plt.show()
vmin = 1000000000
vmax = vmin * -1



go = True 
slowmode = False #determines if slow mode is currently on
subset = 0 #tracks the amount of subsets processed 

while (go):
    try:
        #IMPORTANT: Dont forget about this coniditonal
        #if(len(arr2) == 50):
            #arr = arr[1:50]
            #arr2 = arr2[1:50]
            #arr3 = arr3[1:50]
            
        #val = (hx.get_weight(5)) / 4.4477
        #arr.append(val)
        #print("Scale 1 Weight: " + str(val))
        
        
            
        '''
        A value of 1 in .get_weight() results in about 11.36 points/s.
            Time it takes for each point is about 0.0878 s.
        '''
            
        val = (hx2.get_weight(1)) / 2.1745#Fast mode
        valtime = datetime.datetime.now() #timestamp
        arr2.append(val)
        #print("Scale 2 Weight: " + str(val))
                        
                
        if(val < movingaverage):
            sleep(0.4122) #slow mode, time.sleep makes rate two points/second
            if(slowmode == False): #lets user know when slow mode is activated
                slowmode = True
                print("Slow Mode ON")
        else:
            if(slowmode == True):
                slowmode = False
                print("Slow Mode is OFF")
                
        if(len(arr2) % 5 == 0): #once we have a new subset of 5, calculate average
            subset = subset + 1 
            movingaverage = getAverage() #function calculates average
            print("Current Moving Average:" + str(getAverage()))
            print("Subset:" + str(subset)) #current subset
            print("Array Length:" + str(len(arr2))) #shows subsets are being calculated correctly
            # Do moving average calculations
            # Get a value for the average

            
            
            
        #val = hx3.get_weight(5)/4.3771
        #arr3.append(val)
        #print("Scale 3 Weight: " + str(val))
        
        #min1 = min(arr)
        #max1 = max(arr)
        min2 = min(arr2) 
        max2 = max(arr2) 
        #min3 = min(arr3)
        #max3 = max(arr3)
        
        #vmin = min( [min1, min2, min3] )
        #vmax = max( [max1, max2, max3] )
        
        vmin = min2 - 5 
        vmax = max2 + 5 
            
        #hx.power_down()
        #hx.power_up()
        plt.clf()
        #plt.plot(arr)
        plt.plot(arr2)
        plt.plot(movingaverage)
        #plt.plot(arr3)
        plt.axis([0,60, vmin, vmax])
        plt.draw()
        plt.pause(0.001)
        #time.sleep(0)
        #print("New Cycle:  ")

        
        
    
        ##with open("/home/pi/Strain_Data.csv", "a") as log:
         ##   Data = val
            #print(str(datetime.datetime.now()))
            #log.write("{0},{1}\n".format(strftime("%Y-%m-%d %H:%M:%S"),str(Data)))
          ##  log.write("{0},{1}\n".format(str(datetime.datetime.now()),str(Data)))
            
    
        
        #sends recorded data/timestamp to server, where it will stored 
        c.send(str(val) + "," + str(valtime) + "\n")
        
        
        
        
        
        
        if keyboard.is_pressed('alt'):
            go = False
            #plotFigure()
    except (KeyboardInterrupt, SystemExit):
            cleanAndExit()
            
            
    '''      
    def plotFigure():
        #hx.power_down()
        #hx.power_up()
        plt.clf()
        #plt.plot(arr)
        plt.plot(arr2)
        #plt.plot(arr3)
        plt.axis([0,60, vmin, vmax])
        plt.draw()
        plt.pause(0.001)
        #time.sleep(0)
        #print("New Cycle:  ")
   '''


