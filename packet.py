from copy import deepcopy

class Packet:

    # Access these constants from other files
    # as Packet.TRACEROUTE or Packet.ROUTING
    TRACEROUTE = 1
    ROUTING = 2
    # Use Packet.ROUTING as the "kind" field for all packets
    # created by your implementations.


    def __init__(self, kind, srcAddr, dstAddr, content=None):
        self.kind = kind        # either TRACEROUTE or ROUTING
        self.srcAddr = srcAddr  # address of the source of the packet
        self.dstAddr = dstAddr  # address of the destination of the packet
        self.content = content  # content of the packet (must be a string)
        self.route = [srcAddr]  # DO NOT access from DSrouter or LSrouter


    def copy(self):
        p = Packet(self.kind, self.srcAddr, self.dstAddr, content=deepcopy(self.content))
        p.route = list(self.route)
        return p


    def isTraceroute(self):

        return self.kind == Packet.TRACEROUTE


    def isRouting(self):
        
        return self.kind == Packet.ROUTING


    def getContent(self):
        
        return self.content


    def addToRoute(self, addr):
        
        self.route.append(addr)


    def getRoute(self):
        
        return self.route


    def animateSend(self, src, dst, latency):
    
        if hasattr(Packet, "animate"):
            Packet.animate(self, src, dst, latency)
