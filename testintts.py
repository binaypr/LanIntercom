import time

try:
    read = open("reachable.txt", "r")
except:
    write = open("reachable.txt", "w")
    write.write(str(time.time()))
    print("File is old")
    
line = read.readline()
if time.time() - float(line) > 120:
    write = open("reachable.txt", "w")
    write.write(str(time.time()))
    print("File is old")
    