import os
import socket
import tkinter as tk
from tkinter import filedialog
import random
import shutil
import subprocess
import socket

root = tk.Tk()
root.withdraw()
#Creates a dialog that asks the user to select (a) file(s)
file_path = filedialog.askopenfilename(multiple = True, initialdir = os.getcwd())

#Defines a random number to create a temp folder and temp port
randomNum = random.randint(11111, 99999)

#Creates a temp folder
os.makedirs("files/" + str(randomNum))
temp_path = os.path.join(os.getcwd(), os.path.normpath("files/" + str(randomNum)))

#Moves all the files to the temp folder
for file2copy in file_path:
    print(file2copy)
    shutil.copy2(file2copy, "files/" + str(randomNum))
print("Files have been moved to:", temp_path)

#Creates a temp port and tells you the IP address of the computer and the port

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("192.168.1.1", 80))
address = s.getsockname()[0]
s.close()

print("HTTP server is running at:", address + ":" + str(randomNum))
result = subprocess.run('python -m http.server ' + str(randomNum) , stdout=subprocess.PIPE, cwd=temp_path)
string = result.stdout

#Transfers the output from the python server to STDOUT
while True:
    print(result.communicate()[0])
















