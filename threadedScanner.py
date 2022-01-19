import concurrent.futures
import threading
import subprocess
import time

FILE_DECAY = 60 * 60
SOCKET_SCAN = 254

reachableList = []

def checkFile():
    #Basic check to see if a good reachable file has been created
    #Valid is dependent on the file being created in the last 60 minutes (or as defined)
    
    needsRefreshing = False
    try:
        read = open("reachable.txt", "r")
    except:
        #If no file exists, create one
        write = open("reachable.txt", "w")
        write.write(str(time.time()) + "\n")
        print("File is old")
        write.close()
        needsRefreshing = True
    else:
        #Read the first line of the file (contains a timestamp)
        line = read.readline()
        if time.time() - float(line) > FILE_DECAY:
            read.close()
            write = open("reachable.txt", "w")
            print("Needs Refreshing")
            write.write(str(time.time()) + "\n")
            needsRefreshing = True
    
    return needsRefreshing


def checkIP(ip):
    #Checks if a given IP is reachable
    result = subprocess.run('ping -n 1 -l 4 ' + ip, stdout=subprocess.PIPE, shell=True)
    string = result.stdout
    split = string.splitlines()
    if("Destination host unreachable" in split[2].decode("utf-8")):
        return "Unreachable: " + ip
    else:
        file.write(ip + "\n")
        return "Reachable: " + ip

def getHostName(ip):
    #Checks the given IP for a hostname
    ip = ip.replace("\n", "")
    result = subprocess.run('ping -a -n 1 -l 4 ' + ip, stdout=subprocess.PIPE, shell=True)
    string = result.stdout
    split = string.splitlines()[1].decode("utf-8")
    hostname = split.split(" ")[1]
    
    if(hostname != ip):
        hostFile.write(hostname + ";;;" + ip + "\n")
        print(hostname + "|" + ip)
    
    return


def findReachable():
    list = []
    for i in range(1,SOCKET_SCAN):
        list.append("192.168.1." + str(i))
    print("Starting REACH SCAN:")
    # Using multithreading, scans for reachable IPs
    with concurrent.futures.ThreadPoolExecutor(max_workers=10 ) as executor:
        future_to_ip = {executor.submit(checkIP, ip): ip for ip in list}
        for future in concurrent.futures.as_completed(future_to_ip):
            print(".", end="", flush=True)
        print("")
        

def findHostNames():
    list = open("reachable.txt", "r").readlines()
    print("Starting HOST SCAN:")
    # With multithreading, scans for hostnames
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        future_to_ip = {executor.submit(getHostName, ip): ip for ip in list}
        
        print("")
        

if(checkFile()):
    #If for some reason we need an update
    file = open("reachable.txt", "a")
    findReachable()
    file.close()
    hostFile = open("hostname.txt", "w")
    findHostNames()
else:
    #assumes the file last updated is still valid
    print("file is up to date")
    hostFile = open("hostname.txt", "w")
    findHostNames()
    
    
    
    





