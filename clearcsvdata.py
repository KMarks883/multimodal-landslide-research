import os

f = open('/home/pi/testdata.csv', "a")
f.truncate()
f.close()


if os.stat('/home/pi/testdata.csv').st_size == 0:
    print('File is empty')
else:
    print('Somehow the file is not empty')
    
