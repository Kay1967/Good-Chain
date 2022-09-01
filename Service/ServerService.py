from copyreg import pickle
import socket
import time
import pickle
import select
from Service.UserService import *
from Service.SignUpService import *
from Repository.UserRepository import *
from View.LoginView import *

class ServerService:
    # def __init__(self, TransactionService, UserService, BlockService):
    #     self.socket = socket
    #     self.transactionService = TransactionService
    #     self.userService = UserService
    #     self.blockService = BlockService
    
    def __init__(self, UserService, SignUpService, userRepository):
        self.socket = socket
        self.userService = UserService
        self.signUpService = SignUpService
        self.userRepository = userRepository
       
        

    def recTransactions(self):
        port = 1233
        HEADERSIZE = 10
        BUFFER_SIZE = 10024
        server_socket = self.socket.socket(self.socket.AF_INET, self.socket.SOCK_STREAM)
        server_socket.bind(('', port))
        server_socket.setsockopt(self.socket.SOL_SOCKET, self.socket.SO_REUSEADDR, 1)
        server_socket.listen(5)
        socket = server_socket
        while True:
            ready_to_read, ready_to_write, in_error = select.select([socket], [],
                                                                    [socket], 15)
            for s in ready_to_read:
                clientsocket, addr = s.accept()
                print()
                print('from pc: zit er in a mattie')
                data = clientsocket.recv(BUFFER_SIZE)
                if data:
                    print(pickle.loads(data))
                    pre_tx = pickle.loads(data)
                    print(f"from {addr}: {pre_tx}")
                    result = self.userService.userRepository.CreateTransactionPool(pickle.loads(data)) #pre_tx[1], pre_tx[2], pre_tx[3], pre_tx[4], pre_tx[5], pre_tx[6], pre_tx[7]
                    print("I am result in serverservice from pc: ", result)
                    if result:
                        clientsocket.sendall(bytes('1', 'utf-8'))
                        
                    else:
                        clientsocket.sendall(bytes('0', 'utf-8'))
                else:
                    s.close()
                    ready_to_read.remove(s)
    
    def recHashedTx(self):
        port = 1234
        HEADERSIZE = 10
        BUFFER_SIZE = 10024
        server_socket = self.socket.socket(self.socket.AF_INET, self.socket.SOCK_STREAM)
        server_socket.bind(('', port))
        server_socket.setsockopt(self.socket.SOL_SOCKET, self.socket.SO_REUSEADDR, 1)
        server_socket.listen(5)
        socket = server_socket
        while True:
            ready_to_read, ready_to_write, in_error = select.select([socket], [],
                                                                    [socket], 15)
            for s in ready_to_read:
                clientsocket, addr = s.accept()
                print()
                print('from pc: zit er in a mattie')
                data = clientsocket.recv(BUFFER_SIZE)
                if data:
                    print(pickle.loads(data))
                    pre_tx = pickle.loads(data)
                    print(f"from {addr}: {pre_tx}")
                    result = self.userService.userRepository.CreateHashForSecurity(pickle.loads(data)) #pre_tx[1], pre_tx[2], pre_tx[3], pre_tx[4], pre_tx[5], pre_tx[6], pre_tx[7]
                    print("I am result in serverservice from pc: ", result)
                    if result:
                        clientsocket.sendall(bytes('1', 'utf-8'))
                    else:
                        clientsocket.sendall(bytes('0', 'utf-8'))
                else:
                    s.close()
                    ready_to_read.remove(s)

    def recUser(self):
        port = 1235
        HEADERSIZE = 10
        BUFFER_SIZE = 10024
        server_socket = self.socket.socket(self.socket.AF_INET, self.socket.SOCK_STREAM)
        server_socket.bind(('', port))
        server_socket.setsockopt(self.socket.SOL_SOCKET, self.socket.SO_REUSEADDR, 1)
        server_socket.listen(5)
        socket = server_socket
        while True:
            ready_to_read, ready_to_write, in_error = select.select([socket], [],
                                                                    [socket], 15)
            for s in ready_to_read:
                clientsocket, addr = s.accept()
                print()
                print(' zit er in a mattie')
                data = clientsocket.recv(BUFFER_SIZE)
                if data:
                    print(pickle.loads(data))
                    result = self.signUpService.userRepository.CreateUser(pickle.loads(data))
                    if result:
                        clientsocket.sendall(bytes('1', 'utf-8'))
                    else:
                        clientsocket.sendall(bytes('0', 'utf-8'))
                else:
                    s.close()
                    ready_to_read.remove(s)
    
    def recKeys (self):
        port = 1236
        HEADERSIZE = 10
        BUFFER_SIZE = 10024
        server_socket = self.socket.socket(self.socket.AF_INET, self.socket.SOCK_STREAM)
        server_socket.bind(('', port))
        server_socket.setsockopt(self.socket.SOL_SOCKET, self.socket.SO_REUSEADDR, 1)
        server_socket.listen(5)
        socket = server_socket
        while True:
            ready_to_read, ready_to_write, in_error = select.select([socket], [],
                                                                    [socket], 15)
            for s in ready_to_read:
                clientsocket, addr = s.accept()
                print()
                print(' zit er in a mattie')
                data = clientsocket.recv(BUFFER_SIZE)
                if data:
                    print(pickle.loads(data))
                    result = self.signUpService.userRepository.SaveKeys(pickle.loads(data))
                    if result:
                        clientsocket.sendall(bytes('1', 'utf-8'))
                    else:
                        clientsocket.sendall(bytes('0', 'utf-8'))
                else:
                    s.close()
                    ready_to_read.remove(s)

    
    def recuser_balance (self):
        port = 1237
        HEADERSIZE = 10
        BUFFER_SIZE = 10024
        server_socket = self.socket.socket(self.socket.AF_INET, self.socket.SOCK_STREAM)
        server_socket.bind(('', port))
        server_socket.setsockopt(self.socket.SOL_SOCKET, self.socket.SO_REUSEADDR, 1)
        server_socket.listen(5)
        socket = server_socket
        while True:
            ready_to_read, ready_to_write, in_error = select.select([socket], [],
                                                                    [socket], 15)
            for s in ready_to_read:
                clientsocket, addr = s.accept()
                print()
                print(' zit er in a mattie')
                data = clientsocket.recv(BUFFER_SIZE)
                if data:
                    print(pickle.loads(data))
                    result = self.signUpService.userRepository.CreateUsersBalance(pickle.loads(data))
                    if result:
                        clientsocket.sendall(bytes('1', 'utf-8'))
                    else:
                        clientsocket.sendall(bytes('0', 'utf-8'))
                else:
                    s.close()
                    ready_to_read.remove(s)

    def recDeleteTx (self):
        port = 1238
        HEADERSIZE = 10
        BUFFER_SIZE = 10024
        server_socket = self.socket.socket(self.socket.AF_INET, self.socket.SOCK_STREAM)
        server_socket.bind(('', port))
        server_socket.setsockopt(self.socket.SOL_SOCKET, self.socket.SO_REUSEADDR, 1)
        server_socket.listen(5)
        socket = server_socket
        while True:
            ready_to_read, ready_to_write, in_error = select.select([socket], [],
                                                                    [socket], 15)
            for s in ready_to_read:
                clientsocket, addr = s.accept()
                print()
                print(' zit er in a mattie')
                data = clientsocket.recv(BUFFER_SIZE)
                if data:
                    print(pickle.loads(data))
                    result = self.userService.userRepository.DeleteTransaction(pickle.loads(data))
                    if result:
                        clientsocket.sendall(bytes('1', 'utf-8'))
                    else:
                        clientsocket.sendall(bytes('0', 'utf-8'))
                else:
                    s.close()
                    ready_to_read.remove(s)
    
    def recTempBlock (self):
        port = 1239
        HEADERSIZE = 10
        BUFFER_SIZE = 10024
        server_socket = self.socket.socket(self.socket.AF_INET, self.socket.SOCK_STREAM)
        server_socket.bind(('', port))
        server_socket.setsockopt(self.socket.SOL_SOCKET, self.socket.SO_REUSEADDR, 1)
        server_socket.listen(5)
        socket = server_socket
        while True:
            ready_to_read, ready_to_write, in_error = select.select([socket], [],
                                                                    [socket], 15)
            for s in ready_to_read:
                clientsocket, addr = s.accept()
                print()
                print(' zit er in a mattie')
                data = clientsocket.recv(BUFFER_SIZE)
                if data:
                    print(pickle.loads(data))
                    result = self.userService.userRepository.CreateTempBlock(pickle.loads(data))
                    if result:
                        clientsocket.sendall(bytes('1', 'utf-8'))
                    else:
                        clientsocket.sendall(bytes('0', 'utf-8'))
                else:
                    s.close()
                    ready_to_read.remove(s)
    
    def recHashTBlock (self):
        port = 1240
        HEADERSIZE = 10
        BUFFER_SIZE = 10024
        server_socket = self.socket.socket(self.socket.AF_INET, self.socket.SOCK_STREAM)
        server_socket.bind(('', port))
        server_socket.setsockopt(self.socket.SOL_SOCKET, self.socket.SO_REUSEADDR, 1)
        server_socket.listen(5)
        socket = server_socket
        while True:
            ready_to_read, ready_to_write, in_error = select.select([socket], [],
                                                                    [socket], 15)
            for s in ready_to_read:
                clientsocket, addr = s.accept()
                print()
                print(' zit er in a mattie')
                data = clientsocket.recv(BUFFER_SIZE)
                if data:
                    print(pickle.loads(data))
                    result = self.userService.userRepository.CreateHashForBlock(pickle.loads(data))
                    if result:
                        clientsocket.sendall(bytes('1', 'utf-8'))
                    else:
                        clientsocket.sendall(bytes('0', 'utf-8'))
                else:
                    s.close()
                    ready_to_read.remove(s)
    
    def recConfirmSUser (self):
        port = 1241
        HEADERSIZE = 10
        BUFFER_SIZE = 10024
        server_socket = self.socket.socket(self.socket.AF_INET, self.socket.SOCK_STREAM)
        server_socket.bind(('', port))
        server_socket.setsockopt(self.socket.SOL_SOCKET, self.socket.SO_REUSEADDR, 1)
        server_socket.listen(5)
        socket = server_socket
        while True:
            ready_to_read, ready_to_write, in_error = select.select([socket], [],
                                                                    [socket], 15)
            for s in ready_to_read:
                clientsocket, addr = s.accept()
                print()
                print(' zit er in a mattie')
                data = clientsocket.recv(BUFFER_SIZE)
                if data:
                    print(pickle.loads(data))
                    result = self.userService.userRepository.UpdateConfirmationStatus(pickle.loads(data))
                    if result:
                        clientsocket.sendall(bytes('1', 'utf-8'))
                    else:
                        clientsocket.sendall(bytes('0', 'utf-8'))
                else:
                    s.close()
                    ready_to_read.remove(s)
    
    def recBlockchain(self):
        port = 1242
        HEADERSIZE = 10
        BUFFER_SIZE = 10024
        server_socket = self.socket.socket(self.socket.AF_INET, self.socket.SOCK_STREAM)
        server_socket.bind(('', port))
        server_socket.setsockopt(self.socket.SOL_SOCKET, self.socket.SO_REUSEADDR, 1)
        server_socket.listen(5)
        socket = server_socket
        while True:
            ready_to_read, ready_to_write, in_error = select.select([socket], [],
                                                                    [socket], 15)
            for s in ready_to_read:
                clientsocket, addr = s.accept()
                print(' zit er in a mattie')
                data = clientsocket.recv(BUFFER_SIZE)
                if data:
                    print(pickle.loads(data))
                    result = self.userService.userRepository.CreateBlockChain(pickle.loads(data))
                    if result:
                        clientsocket.sendall(bytes('1', 'utf-8'))
                    else:
                        clientsocket.sendall(bytes('0', 'utf-8'))
                else:
                    s.close()
                    ready_to_read.remove(s)
    
    def recHashBchain(self):
        port = 1243
        HEADERSIZE = 10
        BUFFER_SIZE = 10024
        server_socket = self.socket.socket(self.socket.AF_INET, self.socket.SOCK_STREAM)
        server_socket.bind(('', port))
        server_socket.setsockopt(self.socket.SOL_SOCKET, self.socket.SO_REUSEADDR, 1)
        server_socket.listen(5)
        socket = server_socket
        while True:
            ready_to_read, ready_to_write, in_error = select.select([socket], [],
                                                                    [socket], 15)
            for s in ready_to_read:
                clientsocket, addr = s.accept()
                print(' zit er in a mattie')
                data = clientsocket.recv(BUFFER_SIZE)
                if data:
                    print(pickle.loads(data))
                    result = self.userService.userRepository.CreateHashForChain(pickle.loads(data))
                    if result:
                        clientsocket.sendall(bytes('1', 'utf-8'))
                    else:
                        clientsocket.sendall(bytes('0', 'utf-8'))
                else:
                    s.close()
                    ready_to_read.remove(s)

    def recUpdateHshdTx(self):
      port = 1244
      HEADERSIZE = 10
      BUFFER_SIZE = 10024
      server_socket = self.socket.socket(self.socket.AF_INET, self.socket.SOCK_STREAM)
      server_socket.bind(('', port))
      server_socket.setsockopt(self.socket.SOL_SOCKET, self.socket.SO_REUSEADDR, 1)
      server_socket.listen(5)
      socket = server_socket
      while True:
          ready_to_read, ready_to_write, in_error = select.select([socket], [],
                                                                  [socket], 15)
          for s in ready_to_read:
              clientsocket, addr = s.accept()
              print(' zit er in a mattie')
              data = clientsocket.recv(BUFFER_SIZE)
              if data:
                  print(pickle.loads(data))
                  result = self.userService.userRepository.UpdateHashForSecurity(pickle.loads(data))
                  if result:
                      clientsocket.sendall(bytes('1', 'utf-8'))
                  else:
                      clientsocket.sendall(bytes('0', 'utf-8'))
              else:
                  s.close()
                  ready_to_read.remove(s)

    def recDelCnfrmdTx(self):
      port = 1245
      HEADERSIZE = 10
      BUFFER_SIZE = 10024
      server_socket = self.socket.socket(self.socket.AF_INET, self.socket.SOCK_STREAM)
      server_socket.bind(('', port))
      server_socket.setsockopt(self.socket.SOL_SOCKET, self.socket.SO_REUSEADDR, 1)
      server_socket.listen(5)
      socket = server_socket
      while True:
          ready_to_read, ready_to_write, in_error = select.select([socket], [],
                                                                  [socket], 15)
          for s in ready_to_read:
              clientsocket, addr = s.accept()
              print(' zit er in a mattie')
              data = clientsocket.recv(BUFFER_SIZE)
              if data:
                  print(pickle.loads(data))
                  result = self.userService.userRepository.DeleteConfirmedTransactions(pickle.loads(data))
                  if result:
                      clientsocket.sendall(bytes('1', 'utf-8'))
                  else:
                      clientsocket.sendall(bytes('0', 'utf-8'))
              else:
                  s.close()
                  ready_to_read.remove(s)
    
    def recDelTmpBlock(self):
        port = 1246
        HEADERSIZE = 10
        BUFFER_SIZE = 10024
        server_socket = self.socket.socket(self.socket.AF_INET, self.socket.SOCK_STREAM)
        server_socket.bind(('', port))
        server_socket.setsockopt(self.socket.SOL_SOCKET, self.socket.SO_REUSEADDR, 1)
        server_socket.listen(5)
        socket = server_socket
        while True:
            ready_to_read, ready_to_write, in_error = select.select([socket], [],
                                                                    [socket], 15)
            for s in ready_to_read:
                clientsocket, addr = s.accept()
                print(' zit er in a mattie')
                data = clientsocket.recv(BUFFER_SIZE)
                if data:
                    print(pickle.loads(data))
                    result = self.userService.userRepository.DeleteTempBlock(pickle.loads(data))
                    if result:
                        clientsocket.sendall(bytes('1', 'utf-8'))
                    else:
                        clientsocket.sendall(bytes('0', 'utf-8'))
                else:
                    s.close()
                    ready_to_read.remove(s)

    def recUpdateUsrBalance(self):
        port = 1247
        HEADERSIZE = 10
        BUFFER_SIZE = 10024
        server_socket = self.socket.socket(self.socket.AF_INET, self.socket.SOCK_STREAM)
        server_socket.bind(('', port))
        server_socket.setsockopt(self.socket.SOL_SOCKET, self.socket.SO_REUSEADDR, 1)
        server_socket.listen(5)
        socket = server_socket
        while True:
            ready_to_read, ready_to_write, in_error = select.select([socket], [],
                                                                    [socket], 15)
            for s in ready_to_read:
                clientsocket, addr = s.accept()
                print(' zit er in a mattie')
                data = clientsocket.recv(BUFFER_SIZE)
                if data:
                    print(pickle.loads(data))
                    result = self.userService.userRepository.UpdateUserBalance(pickle.loads(data))
                    if result:
                        clientsocket.sendall(bytes('1', 'utf-8'))
                    else:
                        clientsocket.sendall(bytes('0', 'utf-8'))
                else:
                    s.close()
                    ready_to_read.remove(s)
 
 