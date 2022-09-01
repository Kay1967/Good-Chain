import os
import string
import random
from termcolor import colored
import time
from sys import hash_info
import Repository
from  Repository.UserRepository import *
from datetime import datetime as dt
import hashlib
from hashlib import sha256
from Service.BlockService import *

from copyreg import pickle
import socket
import time
import pickle
import select
from threading import Thread

hash_func = lambda x: sha256(x.encode('utf-8')).hexdigest()

class User:
    
    def __init__(self, username, userRepository, UserService, SignUpService, LoginService):
      self.username = username
      self.userRepository = userRepository
      self.socket = socket
      self.userService = UserService
      self.signUpService = SignUpService
      self.loginService =LoginService


    def CheckReceiver(self, username):
      self.username = username
      receiver_name = self.userRepository.GetAllUsers()
      for receiver in receiver_name:

        if receiver[1] == username:
          
          return receiver[1]

      else:
        raise ValueError(f"This user has not signed up yet.")
          

    def hash_transaction(self, transaction):
      hash_info = hash_func(str(transaction))
      return hash_info





    # def __init__(self, TransactionService, UserService, BlockService):
    #     self.socket = socket
    #     self.transactionService = TransactionService
    #     self.userService = UserService
    #     self.blockService = BlockService
    
        
        

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
            #if len(ready_to_read) == 0:

            for s in ready_to_read:
                
                clientsocket, addr = s.accept()
                print(' zit er in a mattie')
                data = clientsocket.recv(BUFFER_SIZE)
                if data:
                    print(pickle.loads(data))
                    pre_tx = pickle.loads(data)
                    print(f"from {addr}: {pre_tx}")
                    result = self.userRepository.CreateTransactionPool(pre_tx[1], pre_tx[2], pre_tx[3], pre_tx[4])
                    if result:
                        clientsocket.sendall(bytes('1', 'utf-8'))
                    else:
                        clientsocket.sendall(bytes('0', 'utf-8'))
                else:
                    s.close()
                    ready_to_read.remove(s)

    # def recUser(self):
    #     port = 1234
    #     HEADERSIZE = 10
    #     BUFFER_SIZE = 10024
    #     server_socket = self.socket.socket(self.socket.AF_INET, self.socket.SOCK_STREAM)
    #     server_socket.bind(('', port))
    #     server_socket.setsockopt(self.socket.SOL_SOCKET, self.socket.SO_REUSEADDR, 1)
    #     server_socket.listen(5)
    #     socket = server_socket
    #     while True:
    #         ready_to_read, ready_to_write, in_error = select.select([socket], [],
    #                                                                 [socket], 6)
    #         for s in ready_to_read:
    #             clientsocket, addr = s.accept()
    #             print(' zit er in a mattie')
    #             data = clientsocket.recv(BUFFER_SIZE)
    #             if data:
    #                 print(pickle.loads(data))
    #                 result = self.userService.userRepo.addUser(pickle.loads(data))
    #                 if result:
    #                     clientsocket.sendall(bytes('1', 'utf-8'))
    #                 else:
    #                     clientsocket.sendall(bytes('0', 'utf-8'))
    #             else:
    #                 s.close()
    #                 ready_to_read.remove(s)

    # def recBlockchain(self):
    #     port = 1235
    #     HEADERSIZE = 10
    #     BUFFER_SIZE = 10024
    #     server_socket = self.socket.socket(self.socket.AF_INET, self.socket.SOCK_STREAM)
    #     server_socket.bind(('', port))
    #     server_socket.setsockopt(self.socket.SOL_SOCKET, self.socket.SO_REUSEADDR, 1)
    #     server_socket.listen(5)
    #     socket = server_socket
    #     while True:
    #         ready_to_read, ready_to_write, in_error = select.select([socket], [],
    #                                                                 [socket], 15)
    #         for s in ready_to_read:
    #             clientsocket, addr = s.accept()
    #             print(' zit er in a mattie')
    #             data = clientsocket.recv(BUFFER_SIZE)
    #             if data:
    #                 print(pickle.loads(data))
    #                 result = self.blockService.blockRepo.addBlock(pickle.loads(data))
    #                 if result:
    #                     clientsocket.sendall(bytes('1', 'utf-8'))
    #                 else:
    #                     clientsocket.sendall(bytes('0', 'utf-8'))
    #             else:
    #                 s.close()
    #                 ready_to_read.remove(s)

    # def recBlockVerification(self):
    #     port = 3125
    #     HEADERSIZE = 10
    #     BUFFER_SIZE = 10024
    #     server_socket = self.socket.socket(self.socket.AF_INET, self.socket.SOCK_STREAM)
    #     server_socket.bind(('', port))
    #     server_socket.setsockopt(self.socket.SOL_SOCKET, self.socket.SO_REUSEADDR, 1)
    #     server_socket.listen(5)
    #     socket = server_socket
    #     while True:
    #         ready_to_read, ready_to_write, in_error = select.select([socket], [],
    #                                                                 [socket], 15)
    #         for s in ready_to_read:
    #             clientsocket, addr = s.accept()
    #             print(' zit er in a mattie')
    #             data = clientsocket.recv(BUFFER_SIZE)
    #             if data:
    #                 print(pickle.loads(data))
    #                 result = self.userRepository(pickle.loads(data))
    #                 if result:
    #                     clientsocket.sendall(bytes('1', 'utf-8'))
    #                 else:
    #                     clientsocket.sendall(bytes('0', 'utf-8'))
    #             else:
    #                 s.close()
    #                 ready_to_read.remove(s)
 
