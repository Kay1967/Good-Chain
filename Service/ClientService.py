import socket, pickle
import time
#from Service.UserService import *

class ClientService:

  def __init__(self):
      self.TCP_IP = '172.24.35.207'
      self.BUFFER_SIZE = 10024

  def sendObject(self, transaction, tcpPort):
    try:
        print(self.TCP_IP)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.TCP_IP, tcpPort))
        s.send(pickle.dumps(transaction))
        # s.setblocking(False)
        data = s.recv(self.BUFFER_SIZE)
        if data == b'1':
            print('item successfully added to other node from pc')
            s.close()
            return True
        else:
            print('item failed to add to the other node and will be removed.0')
            s.close()
            return False
    except:
        print('item failed to add to the other node and will be removed.1')
        return False
