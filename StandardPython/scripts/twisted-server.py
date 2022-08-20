from twisted import reactor, protocol
from twisted.internet.protocol import Protocol, connectionDone
from twisted.internet.protocol import ServerFactory as SFactory
from twisted.internet.endpoints import TCP4ServerEndpoint

class Server(Protocol):
    def __init__(self.users):
        self.users = users
        self.name = ""

    def connectionMade(self):
        print("New connection")

    def addUser(self, name):

        if name not in self.users:
            self.users[self] = name
            self.name = name
            
        else:
            self.transport.write("Entered username is already in use".encode("utf-8"))

    def dataReceived(self, data):
        data = data.decode("utf-8")

        if not self.name:
            self.addUser(data)
            return

        for protocol, name in self.users.keys():
            if protocol != self:
                protocol.transport.write(f"{self.name}: {data}".encode("utf-8"))

    def connectionLost(self, reason=connectionDone):
        del self.users[self]

class ServerFactory(SFactory):
    def __init__(self):
        self.users = {}

    def build_protocol(self, addr):
        return Server(self.users)

if __name__=='__main__':
    endpoint = TCP4ServerEndpoint(reactor, 4444)
    endpoint.listen(ServerFactory())
    reactor.run()