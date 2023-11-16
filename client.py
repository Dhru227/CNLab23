import time
import sys
import Queue
from packet import Packet


class Client:
    def __init__(self, addr, allClients, sendRate, updateFunction):
        self.addr = addr
        self.allClients = allClients
        self.sendRate = sendRate
        self.lastTime = 0
        self.link = None
        self.updateFunction = updateFunction
        self.sending = True
        self.linkChanges = Queue.Queue()


    def changeLink(self, change):
    
        self.linkChanges.put(change)


    def handlePacket(self, packet):
       
        if packet.kind == Packet.TRACEROUTE:
            self.updateFunction(packet.srcAddr, packet.dstAddr, packet.route)


    def sendTraceroutes(self):
        for dstClient in self.allClients:
            packet = Packet(Packet.TRACEROUTE, self.addr, dstClient)
            if self.link:
                self.link.send(packet, self.addr)
            self.updateFunction(packet.srcAddr, packet.dstAddr, [])


    def handleTime(self, timeMillisecs):
        if self.sending and (timeMillisecs - self.lastTime > self.sendRate):
            self.sendTraceroutes()
            self.lastTime = timeMillisecs


    def runClient(self):
        while True:
            time.sleep(0.1)
            timeMillisecs = int(round(time.time() * 1000))
            try:
                change = self.linkChanges.get_nowait()
                if change[0] == "up":
                    self.link = change[1]
                # don't disconnect clients...
            except Queue.Empty:
                pass
            if self.link:
                packet = self.link.recv(self.addr)
                if packet:
                    self.handlePacket(packet)
            self.handleTime(timeMillisecs)


    def lastSend(self):
        self.sending = False
        self.sendTraceroutes()
