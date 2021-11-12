from bluedot.btcomm import BluetoothClient
from signal import pause


def data_received(data):
    print(data)
    
    
c = BluetoothClient("B8:27:EB:8F:E8:F8", data_received)

for x in range(10):
    c.send("helloworlddfs\n")
