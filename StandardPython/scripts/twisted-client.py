from twisted.internet import reactor
from twisted.internet.protocol import Protocol
from twisted.internet.protocol import ReconnectingClientFactory as CFactory
from twisted.internet.protocol import TCP4ClientEndpoint


class Client(Protocol):
    def __init__(self):
        reactor.callInThread(self.send_data)

    def connectionMade(self):
        print("Write your name.")

    def dataReceived(self, data):
        data = data.decode("utf-8")
        print(data)

    def sendData(self):
        while True:
            self.transport.write(input().encode("utf-8"))

class ClientFactory(CFactory):
    def buildProtocol(self, addr):
        return Client()

    def clientConnectionFailed(self, connector, reason):
        print(reason)
        CFactory.clientConnectionFailed(self, connector, reason)
    
    def clientConnectionLost(self, connector, reason):
        print(reason)
        CFactory.clientConnectionLost(self, connector, reason)

if __name__=='__main__':
    endpoint = TCP4ClientEndpoint(reactor, "localhost", 4444)
    endpoint.connect(ClientFactory())
    reactor.run()