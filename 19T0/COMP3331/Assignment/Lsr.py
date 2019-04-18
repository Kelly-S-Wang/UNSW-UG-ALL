# COMP3331 19T0 Assignment
# Written by Shan Wang (z5119666)
# Due: 3rd Feb. 2019

import sys, time, threading, os
from socket import *

# Link struct consists of destination router and cost
class Link:
    def __init__(self, dest, cost):
        self.dest = dest
        self.cost = cost

# Router struct consists of router id, router port and all links connected to it
class Router:
    def __init__(self, id, port):
        self.id = id
        self.port = port
        self.links = []

    def addLink(self, dest, cost):
        e = Link(dest, cost)
        self.links.append(e)

    def numOfLinks(self):
        return len(self.links)

# Build up global view of the network topology
def topology(data):
    lines = data.split("\n")
    srcInfo = lines[0].split(" ")
    srcRouter = Router(srcInfo[0], int(srcInfo[1]))
    sentRouters = set()

    for i in range(2, int(lines[1]) + 2):
        info = lines[i].split(" ")
        sentRouters.add(info[0])
        srcRouter.addLink(Router(info[0], int(info[2])), float(info[1]))
    return (srcRouter, sentRouters)

# Pack data
def formPacket(srcRouter):
    packetData = srcRouter.id + " " + str(srcRouter.port) + "\n" + str(srcRouter.numOfLinks()) + "\n"
    for link in srcRouter.links:
        packetData += link.dest.id + " " + str(link.cost) + " " + str(link.dest.port) + "\n"
    packetData = packetData[:-1]
    return packetData

# Send data
def sendPacket(port, packetData):
    hostSocket.sendto(packetData, (ip, port))

# Threading
def startThread(time, func, paras):
    t = threading.Timer(time, func, paras)
    t.setDaemon(True)
    t.start()

# Broadcast packet to neighbours every second
def broadcast(srcRouter):
    global broadcasted
    broadcasted = []
    packetData = formPacket(srcRouter)
    for link in srcRouter.links: 
        sendPacket(link.dest.port, packetData)
    startThread(update_interval, broadcast, [startRouter])

# Pop the minimum cost from queue
def priorityQueuePop(queue, cost):
    min = 0
    for i in range(len(queue)):
        if cost[queue[i]] < cost[queue[min]]: min = i
    item = queue[min]
    del queue[min]
    return (queue, item)

# Dijkstras algorithm find the optimal path
def dijkstras(srcRouter, activeRouters):

    print("Djikstra search ...")
    queue = []
    seen = []
    cost = {} # Store cost
    previous = {} # Store the previous router to trace back

    queue.append(srcRouter.id)
    cost[srcRouter.id] = 0

    while len(queue):
        # Choose the least cost unvisited router
        queue, item = priorityQueuePop(queue, cost)

        # Check if this router is active
        isActive = False
        for ar in activeRouters:
            if ar.id == item:
                isActive = True
                curr = ar
                break

        if not isActive: continue
        seen.append(curr.id)

        # Update cost and path
        for link in curr.links:
            totalCost = link.cost + float(cost[curr.id])
            if not link.dest.id in cost.keys() or totalCost < cost[link.dest.id]:
                cost[link.dest.id] = totalCost
                previous[link.dest.id] = curr.id
            if link.dest.id not in queue and link.dest.id not in seen:
                queue.append(link.dest.id)
    return (previous, cost)

# Get path by tracing back the previous and show the cost
def getPath(start, dest, previous, cost):
    curr = dest
    path = str(curr)
    while curr in previous.keys():
        path = previous[curr] + path
        curr = previous[curr]
    print ("Least cost path to router " + str(dest) + ": " + str(path) + " and the cost: " + str(cost[dest]))

# Show the path every 30 seconds
def showPaths(srcRouter):
    global activeRouters
    actives = activeRouters
    previous, cost = dijkstras(srcRouter, actives)
    for ar in actives:
        if ar.id == srcRouter.id: continue
        getPath(srcRouter.id, ar.id, previous, cost)
    startThread(route_update_interval, showPaths, [srcRouter])

# Reset heartbeat every 5 seconds
def heartbeatReset(heartbeat):
    for k in heartbeat.keys():
        heartbeat[k] = 0

# Put failure router to dead list
def getDeadList(heartbeat):
    dead = []
    for k in heartbeat.keys():
        if heartbeat[k] == 0:
            dead.append(k)
    return dead

# Update active routers and show failed routers
def updateActives(heartbeat, dead, actives):
    for ar in actives:
        if ar.id in dead:
            print ("Router " + ar.id + " failed")
            actives.remove(ar)
            del heartbeat[ar.id]
    return actives

# Check failure router, if there's no heartbeat for 5 sec, remove it from active routers list
def failureChcek():
    global heartbeat
    global activeRouters
    tempActive = activeRouters
    hb = heartbeat

    dead = getDeadList(hb) # No heartbeat, then add to dead list
    activeRouters = updateActives(hb, dead, tempActive)
    heartbeatReset(heartbeat)
    startThread(5*update_interval, failureChcek, [])


# Main program starts here
update_interval = 1
route_update_interval = 30
ip = '127.0.0.1'
activeRouters = [] # List of active routers
broadcasted = [] # Tracing broadcasted packets, reset every second
heartbeat = {} # Checking router failure


startId = sys.argv[1]
startPort = int(sys.argv[2])
startFile = open(sys.argv[3], "r").read()

print("I am Router " + startId)

packetData = startId + " " + str(startPort) + "\n" + startFile
startRouter, sentRouters = topology(packetData)

#bind socket
hostSocket = socket(AF_INET, SOCK_DGRAM)
hostSocket.bind((ip, startPort))
hostSocket.settimeout(route_update_interval)

activeRouters.append(startRouter)

broadcast(startRouter) # Broadcasting thread
showPaths(startRouter) # Searching thread
failureChcek() # Checking thread

while True:
    try:
        packetData, sender = hostSocket.recvfrom(1024)
        srcRouter, sentRouters = topology(packetData)
        sentRouters.add(srcRouter.id) # Do not broadcast to sentRouters

        #If the packet has been broadcasted, add it to sentRouters
        senderPort = sender[1]
        inActiveRouters = False
        for ar in activeRouters:
            # Update heartbeat
            if srcRouter.id == ar.id:
                heartbeat[srcRouter.id] += 1
                inActiveRouters = True
            if srcRouter.port != senderPort and srcRouter.id in heartbeat.keys() and ar.port == senderPort:
                for link in ar.links:
                    sentRouters.add(link.dest.id)

        if not inActiveRouters:
            heartbeat[srcRouter.id] = 0
            activeRouters.append(srcRouter)
            heartbeatReset(heartbeat)
            print("Router " + str(srcRouter.id) + " back now, " + str(len(activeRouters)) + " active routers")

        # Broadcast packets
        for link in startRouter.links:
            if link.dest.id not in sentRouters and link.dest.port != senderPort and srcRouter.id not in broadcasted:
                sendPacket(link.dest.port, packetData)

        broadcasted.append(srcRouter.id)

    except timeout:
        print ("timeout")
