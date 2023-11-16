import time
import sys
import thread
import Queue


class Router:

    def __init__(self, addr, heartbeatTime = None):
    
        self.addr = addr            # address of router
        self.nextFreePort = 1
        self.portMap = {}           # links indexed by port
        self.linkMap = {}
        self.linkChanges = Queue.Queue()


    def changeLink(self, change):
       
        self.linkChanges.put(change)


    def addLink(self, endpointAddr, link, cost):
        
        if link in self.portMap:
            port = self.removeLink(link)
        else:
            port = self.nextFreePort
            self.nextFreePort += 1
        
        self.portMap[link] = port
        self.linkMap[port] = link
        self.handleNewLink(port, endpointAddr, cost)


    def removeLink(self, link):
    
        port = self.portMap[link]
        del self.portMap[link]
        del self.linkMap[port]
        self.handleRemoveLink(port)

        return port


    def runRouter(self):
    
        while True:
            time.sleep(0.1)
            timeMillisecs = int(round(time.time() * 1000))
            try:
                change = self.linkChanges.get_nowait()
                if change[0] == "up":
                    self.addLink(*change[1:])
                elif change[0] == "down":
                    self.removeLink(*change[1:])
            except Queue.Empty:
                pass
            for link, port in self.portMap.items():
                packet = link.recv(self.addr)
                if packet:
                    self.handlePacket(port, packet)
            self.handleTime(timeMillisecs)


    def send(self, port, packet):
        
        try:
            self.linkMap[port].send(packet, self.addr)
        except KeyError:
            pass

   


    def handlePacket(self, port, packet):
        
        # default implementation sends packet back out the port it arrived
        self.send(port, packet)


    def handleNewLink(self, port, endpoint, cost):
        
        pass


    def handleRemoveLink(self, port):
        
        pass


    def handleTime(self, timeMillisecs):
        
        pass


    def debugString(self):
        
        return "Mirror router: address {}".format(self.addr)
