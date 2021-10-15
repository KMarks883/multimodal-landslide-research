from bluedot.btcomm import BluetoothServer
import datetime

def data_received(data):
    with open("/home/pi/Desktop/testdata.csv", "a") as log:
        log.write("{0},{1}\n".format(str(datetime.datetime.now()), data))
    print(data)
    
    
s = BluetoothServer(data_received)


#reminder make sure weight is 4 decimal places 

