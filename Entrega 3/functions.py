import json
import os
import time

fileFolder = "resources"
fileName = "Table.json"
filePath = os.path.join(fileFolder, fileName)

def getDefaultMessage():
    localTime = time.localtime()
    if len(str(localTime[4])) == 1: # Quando o horário for, por exemplo, 12:03 ele apareceria 12:3
        defaultMessage = str(localTime[3]) + ":0" + str(localTime[4]) + " CIntofome: "
    else:
        defaultMessage = str(localTime[3]) + ":" + str(localTime[4]) + " CIntofome: "
    return defaultMessage

def addClient(newClient, clientSocket):
    client = {
        "name": newClient[0],
        "table": newClient[1],
        "bill": 0.00,
        "socket": clientSocket,
        "orders": []
    }
    
    with open(filePath, "r+") as file:
        fileData = json.load(file)
        fileData["clients"].append(client)
        file.seek(0)
        json.dump(fileData, file, indent=4)

def delClient(clientSocket):
    file  = json.load(open(filePath))
                                                 
    for i in range(len(file["clients"])):
        if file["clients"][i]["socket"] == clientSocket:
            file["clients"].pop(i)
            break
                               
    open(filePath, "w").write(
        json.dumps(file, sort_keys = True, indent = 4)
    )
        
def addOrder(order, menu, clientSocket):
    with open(filePath, "r+") as file:
        fileData = json.load(file)
        idx = 0
        for i in fileData["clients"]:
            if fileData["clients"][idx]["socket"] == clientSocket:
                fileData["clients"][idx]["orders"].append(order)
                fileData["clients"][idx]["bill"] += menu[int(order) - 1][2]
            idx += idx
    with open(filePath, "w") as file:
        json.dump(fileData, file, indent=4)
    
def getIndividualBill(menu, clientSocket):
    with open(filePath, "r+") as file:
        fileData = json.load(file)
        idx = 0
        bill = []
        name = ""
        data = ""
        total = ""
        for i in fileData["clients"]:
            if fileData["clients"][idx]["socket"] == clientSocket:
                name = fileData["clients"][idx]["name"]
                total = fileData["clients"][idx]["bill"]
                break
            idx += idx
        
        for i in menu:
            for j in fileData["clients"][idx]["orders"]:
                if i[0] == int(j):
                    bill.append([i[1], i[2]])
                    
        data += "| " + name + " |\n"
        for i in bill:
            data += i[0] + " => " + "R$" + str(i[1]) + "\n"
            data += "-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-\n"
        data += "Total - R$" + str(total) + "\n"
        data += "-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-\n"
        
    return(data, total)
    
def getTableBill(menu, clientSocket):
    tableTotal = 0.0
    file = json.load(open(filePath))
    tableOrders = []
    data = ""
    tableNumber = 0
    for i in range(len(file["clients"])): # Pega a mesa do cliente.
        if file["clients"][i]["socket"] == clientSocket:
            tableNumber = file["clients"][i]["table"]
    
    for i in range(len(file["clients"])): # pega todos os pedidos de cada cliente da mesa especifica
        if file["clients"][i]["table"] == tableNumber:
            tableOrders.append((file["clients"][i]["name"], file["clients"][i]["orders"], file["clients"][i]['bill']))
            
    for i in range(len(tableOrders)):
        name, orders, individualBill = tableOrders[i]
        data += "| " + name + " |\n"
        for j in range(len(orders)):
            a, item, price = menu[int(orders[j])- 1]
            data += item + " => " + "R$" + str(price) + "\n"
            data += "-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-\n"
        
        data += "Total - R$" + str(individualBill) + "\n"
        data += "-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-\n"
        tableTotal += individualBill
        
    data += "Total da mesa - R$" + str(tableTotal) + "\n"
    data += "-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-\n"
    return (data, tableTotal)

def getPayMessage(menu, clientSocket):
    tableTotal = getTableBill(menu, clientSocket)[1]
    individualTotal = getIndividualBill(menu, clientSocket)[1]
    data = "Sua conta foi R$" + str(individualTotal) + " e a da mesa R$ " + str(tableTotal) + ". Digite o valor a ser pago:"
    return (data, tableTotal, individualTotal)

def getTableSize(clientSocket):
    file  = json.load(open(filePath))
    size = 0
    for i in range(len(file["clients"])):
        if file["clients"][i]["socket"] == clientSocket:
            table = file["clients"][i]["table"]
            
    for i in range(len(file["clients"])):
        if file["clients"][i]["table"] == table:
            size += 1
            
    return size, table
        
    
def payBill(payment, individualTotal, clientSocket):
    with open(filePath, "r+") as file:
        fileData = json.load(file)
        for i in range(len(fileData["clients"])):
            if fileData["clients"][i]["socket"] == clientSocket:
                fileData["clients"][i]["bill"] = 0.0
                fileData["clients"][i]["orders"] = []
    with open(filePath, "w") as file:
        json.dump(fileData, file, indent=4)
                    
    if payment > individualTotal:
        with open(filePath, "r+") as file:
            fileData = json.load(file)
            tableSize, table = getTableSize(clientSocket)
            change = payment - individualTotal
            value = change/(tableSize - 1)
            for i in range(len(fileData["clients"])):
                if fileData["clients"][i]["table"] == table and fileData["clients"][i]["socket"] != clientSocket:
                    fileData["clients"][i]["bill"] -= value
                    
        with open(filePath, "w") as file:
            json.dump(fileData, file, indent=4)

def getMenu(menu):
    data = ""
    data += "ID | Comida | Preço\n"
    for i in range(len(menu)):
        data += "                 " + str(menu[i][0]) + " " + menu[i][1] + " " + str(menu[i][2]) + "\n"
    return data