# # from copyreg import pickle
# # import socket
# # import time
# # import pickle
# # import select
# # import threading
# # from Service.UserService import *

# # #from client3 import receive
# # port = 3125
# # class Server:
# #    #this socket is just for accepting connection
# #   port = 3125
# #   HEADERSIZE = 10
# #   BUFFER_SIZE = 1024
# #   def __init__(self):
# #     self.port = 3125
    
# #   #class Server_Client:
# #   def newServerConnection(ip_addr): 
# #     server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# #     server_socket.bind ((ip_addr, port))
# #     server_socket.listen(5)
# #     return server_socket


# #   def recObj(self, socket):  
# #     #print (f"Connection from {} has been established!")
# #     ready_to_read, ready_to_write, in_error = select.select([socket], [],
# #     [socket], 15)

    
# #     if socket in ready_to_read:
# #       #print("something good")
# #       client_socket, addr = socket.accept() # accept method returns a socket and an address and this socket is for communication 
# #       print(f"message cromes from this address: {addr}")
# #       all_data = b''
# #       while True:
# #         data = client_socket.recv(self.BUFFER_SIZE)
# #         if not data:
# #           break
# #         all_data = all_data + data
# #       return pickle.loads(all_data)
# #     return None


# #   def sendObj(ip_addr, blk):
# #     soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# #     soc.connect((ip_addr, port))
# #     msg = pickle.dumps(blk)
# #     print(msg)
# #     soc.send(msg)

# #     soc.close()
# #     return False

# #   #receive_thread = threading.Thread(target=recObj, args=(server_socket,))
# #   #receive_thread.start()
# #   #print("this is recobj thread: ", receive_thread)

# from copyreg import pickle
# import socket
# import time
# import pickle
# import select

# class ServerService:
#     # def __init__(self, TransactionService, UserService, BlockService):
#     #     self.socket = socket
#     #     self.transactionService = TransactionService
#     #     self.userService = UserService
#     #     self.blockService = BlockService
#     def __init__(self, UserService, SignUpService):
#         self.socket = socket
#         self.userService = UserService
#         self.signUpService = SignUpService
        

#     def recTransactions(self):
#         port = 3125
#         HEADERSIZE = 10
#         BUFFER_SIZE = 10024
#         server_socket = self.socket.socket(self.socket.AF_INET, self.socket.SOCK_STREAM)
#         server_socket.bind(('', port))
#         server_socket.setsockopt(self.socket.SOL_SOCKET, self.socket.SO_REUSEADDR, 1)
#         server_socket.listen(5)
#         socket = server_socket
#         while True:
#             ready_to_read, ready_to_write, in_error = select.select([socket], [],
#                                                                     [socket], 15)
#             for s in ready_to_read:
#                 clientsocket, addr = s.accept()
#                 print(' zit er in a mattie')
#                 data = clientsocket.recv(BUFFER_SIZE)
#                 if data:
#                     print(pickle.loads(data))
#                     result = pickle.loads(data)
#                     if result:
#                         clientsocket.sendall(bytes('1', 'utf-8'))
#                     else:
#                         clientsocket.sendall(bytes('0', 'utf-8'))
#                 else:
#                     s.close()
#                     ready_to_read.remove(s)

#     def recUser(self):
#         port = 1234
#         HEADERSIZE = 10
#         BUFFER_SIZE = 10024
#         server_socket = self.socket.socket(self.socket.AF_INET, self.socket.SOCK_STREAM)
#         server_socket.bind(('', port))
#         server_socket.setsockopt(self.socket.SOL_SOCKET, self.socket.SO_REUSEADDR, 1)
#         server_socket.listen(5)
#         socket = server_socket
#         while True:
#             ready_to_read, ready_to_write, in_error = select.select([socket], [],
#                                                                     [socket], 15)
#             for s in ready_to_read:
#                 clientsocket, addr = s.accept()
#                 print(' zit er in a mattie')
#                 data = clientsocket.recv(BUFFER_SIZE)
#                 if data:
#                     print(pickle.loads(data))
#                     result = self.userService.userRepo.addUser(pickle.loads(data))
#                     if result:
#                         clientsocket.sendall(bytes('1', 'utf-8'))
#                     else:
#                         clientsocket.sendall(bytes('0', 'utf-8'))
#                 else:
#                     s.close()
#                     ready_to_read.remove(s)

#     def recBlockchain(self):
#         port = 1235
#         HEADERSIZE = 10
#         BUFFER_SIZE = 10024
#         server_socket = self.socket.socket(self.socket.AF_INET, self.socket.SOCK_STREAM)
#         server_socket.bind(('', port))
#         server_socket.setsockopt(self.socket.SOL_SOCKET, self.socket.SO_REUSEADDR, 1)
#         server_socket.listen(5)
#         socket = server_socket
#         while True:
#             ready_to_read, ready_to_write, in_error = select.select([socket], [],
#                                                                     [socket], 15)
#             for s in ready_to_read:
#                 clientsocket, addr = s.accept()
#                 print(' zit er in a mattie')
#                 data = clientsocket.recv(BUFFER_SIZE)
#                 if data:
#                     print(pickle.loads(data))
#                     result = self.blockService.blockRepo.addBlock(pickle.loads(data))
#                     if result:
#                         clientsocket.sendall(bytes('1', 'utf-8'))
#                     else:
#                         clientsocket.sendall(bytes('0', 'utf-8'))
#                 else:
#                     s.close()
#                     ready_to_read.remove(s)

#     def recBlockVerification(self):
#         port = 1236
#         HEADERSIZE = 10
#         BUFFER_SIZE = 10024
#         server_socket = self.socket.socket(self.socket.AF_INET, self.socket.SOCK_STREAM)
#         server_socket.bind(('', port))
#         server_socket.setsockopt(self.socket.SOL_SOCKET, self.socket.SO_REUSEADDR, 1)
#         server_socket.listen(5)
#         socket = server_socket
#         while True:
#             ready_to_read, ready_to_write, in_error = select.select([socket], [],
#                                                                     [socket], 15)
#             for s in ready_to_read:
#                 clientsocket, addr = s.accept()
#                 print(' zit er in a mattie')
#                 data = clientsocket.recv(BUFFER_SIZE)
#                 if data:
#                     print(pickle.loads(data))
#                     result = self.transactionService.transactionRepo.addTransaction(pickle.loads(data))
#                     if result:
#                         clientsocket.sendall(bytes('1', 'utf-8'))
#                     else:
#                         clientsocket.sendall(bytes('0', 'utf-8'))
#                 else:
#                     s.close()
#                     ready_to_read.remove(s)
 