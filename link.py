import thread
import sys
import Queue
import time
import threading
from types import StringType


class Link:
    def __init__(self, e1, e2, latency, latencyMultiplier):
        self.q12 = Queue.Queue()
        self.q21 = Queue.Queue()
        self.latency = latency * latencyMultiplier
        self.latencyMultiplier = latencyMultiplier
        self.e1 = e1
        self.e2 = e2


    def send_helper(self, packet, src):
    
        if src == self.e1:
            packet.addToRoute(self.e2)
            packet.animateSend(self.e1, self.e2, self.latency)
            time.sleep(self.latency / float(1000))
            self.q12.put(packet)
        elif src == self.e2:
            packet.addToRoute(self.e1)
            packet.animateSend(self.e2, self.e1, self.latency)
            time.sleep(self.latency / float(1000))
            self.q21.put(packet)
        sys.stdout.flush()


    def send(self, packet, src):
    
        if packet.content:
            assert type(packet.content) is StringType, \
                   "Packet content must be a string"
        p = packet.copy()
        thread.start_new_thread(self.send_helper, (p, src))


    def recv(self, dst, timeout=None):
    
        if dst == self.e1:
            try:
                packet = self.q21.get_nowait()
                return packet
            except Queue.Empty:
                return None
        elif dst == self.e2:
            try:
                packet = self.q12.get_nowait()
                return packet
            except Queue.Empty:
                return None


    def changeLatency(self, latency):
       
        self.latency = latency * self.latencyMultiplier
