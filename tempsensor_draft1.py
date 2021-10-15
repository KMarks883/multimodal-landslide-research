from bluedot.btcomm import BluetoothServer
import datetime
import time
import datetime
import os
import glob
import csv
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
from w1thermsensor import W1ThermSensor

sensor = W1ThermSensor()
temperature_in_celsius = sensor.get_temperature()
temperature_in_fahrenheit = sensor.get_temperature(W1ThermSensor.DEGREES_F)
temperature_in_all_units = sensor.get_temperatures([W1ThermSensor.DEGREES_C, W1ThermSensor.DEGREES_F, W1ThermSensor.KELVIN])

from w1thermsensor import W1ThermSensor

# Create the I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

# Create the ADC object using the I2C bus
ads = ADS.ADS1115(i2c)

# Create single-ended input on channel 0
chan0 = AnalogIn(ads, ADS.P0)
chan1 = AnalogIn(ads, ADS.P1)
chan2 = AnalogIn(ads, ADS.P2)
chan3 = AnalogIn(ads, ADS.P3)

# Create differential input between channel 0 and 1
#chan = AnalogIn(ads, ADS.P0, ADS.P1)

#print("{:>5}\t{:>5}".format('raw', 'v'))


#Does not record the second sensor temperature

#receives weight data from client and dispays it
    #with open("/home/pi/Desktop/testdata.csv", "a") as log:
        #log.write("{0},{1}\n".format(str(datetime.datetime.now()), data))


#if the file stream is writing data, this is set to true to prevent program shutdowns from
dont_end_yet = False


def write_to_csv(weight_data):
    # the a is for append, if w for write is used then it overwrites the file
    dont_end_yet = True
    print('Client Sensor Data: ' + weight_data)
    ts = datetime.datetime.now()
    print("{}\t{:>5.5f}\t{:>5.5f}\t{:>5.5f}".format(ts, chan0.voltage, chan1.voltage, chan2.voltage))#, chan3.voltage))
    for sensor in W1ThermSensor.get_available_sensors():
        print("Sensor %s has temperature %.2f" % (sensor.id, sensor.get_temperature()))    
    write_to_csv(weight_data)
    dont_end_yet = True
    time.sleep(0)
    with open('/home/pi/readings.csv', mode='a') as readings:
        sensor_write = csv.writer(readings, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        write_to_log = sensor_write.writerow([ts, chan0.voltage, chan1.voltage, chan2.voltage, sensor.get_temperature()]) # chan3.voltage,
        return(write_to_log)
    

#outputs data gathered from client/server sensors and sends to file write function.
#dataCollection is only called when the server received client data (line 64)
def mergeData(weight_data):
    dont_end_yet = True
    print('Client Sensor Data: ' + weight_data)
    ts = datetime.datetime.now()
    print("{}\t{:>5.5f}\t{:>5.5f}\t{:>5.5f}".format(ts, chan0.voltage, chan1.voltage, chan2.voltage))#, chan3.voltage))
    for sensor in W1ThermSensor.get_available_sensors():
        print("Sensor %s has temperature %.2f" % (sensor.id, sensor.get_temperature()))    
    write_to_csv(weight_data)
    dont_end_yet = True
    time.sleep(0)

def dataCollection_Hault:
    print('Client has disconnected. Haulting data gathering to prevent formatting issues.')

#initilize server 's' and designate callback function when server received data from client 
s = BluetoothServer(mergeData)
#designates function to be called (dataCollection) when client connects to server
s.when_client_disconnects(dataCollection_Hault)

        



