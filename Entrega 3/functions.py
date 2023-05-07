import socket
import json
import random
import os

fileFolder = "resources"
fileName = "Table.json"
filePath = os.path.join(fileFolder, fileName)
#newClient = ["Fabricio", 2]
#clientSocket = "192.168.0.0:225"
#addClient(newClient, clientSocket)

def addClient (newClient, clientSocket):
    client = {
        "name": newClient[0],
        "table": newClient[1],
        "bill": 0,
        "socket": clientSocket,
        "orders": []
    }
    
    with open(filePath, "r+") as file:
        fileData = json.load(file)
        fileData["clients"].append(client)
        file.seek(0)
        json.dump(fileData, file, indent=4)
        