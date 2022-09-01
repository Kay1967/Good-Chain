import os
import time
from threading import Thread
from datetime import datetime as dt
from Component.UserInterface import *
import pickle
import Domain
import socket
from termcolor import colored
import Service
from Service.SignUpService import *
import Transactions
from Transactions.Asym import *
from Service.UserService import *
from Domain.User import *
from View.LoginView import *
from Service.ClientService import *
from Service.ServerService import *

class LoginService:
  loggedin = False

  def __init__ (self, userRepository, userService, serverService, clientService): #, serverService, clientService
    self.userRepository = userRepository
    self.userService = userService
    self.serverService = serverService
    self.clientService = clientService
    #self.socket = socket.socket()
    #self.socket = socket #.socket(socket.AF_INET, socket.SOCK_STREAM)
  def serverOn(self):
    recTransaction = Thread(target=self.serverService.recTransactions)
    recHashedTx = Thread(target=self.serverService.recHashedTx)
    recUser = Thread(target=self.serverService.recUser)
    recKeys = Thread(target=self.serverService.recKeys)
    recUser_Balance = Thread(target=self.serverService.recuser_balance)
    recDeleteTx = Thread(target=self.serverService.recDeleteTx)
    recTempBlock = Thread(target=self.serverService.recTempBlock)
    recHashTBlock = Thread(target=self.serverService.recHashTBlock)
    recConfirmSUser = Thread(target=self.serverService.recConfirmSUser)
    recBlockchain = Thread(target=self.serverService.recBlockchain)
    recHashBchain = Thread(target=self.serverService.recHashBchain)
    recUpdateHshdTx = Thread(target=self.serverService.recUpdateHshdTx)
    recDelCnfrmdTx = Thread(target=self.serverService.recDelCnfrmdTx)
    recDelTmpBlock = Thread(target=self.serverService.recDelTmpBlock)
    recUpdateUsrBalance = Thread(target=self.serverService.recUpdateUsrBalance)
    
    recTransaction.start()
    recHashedTx.start()
    print("server is on...")
    recUser.start()
    recKeys.start()
    recUser_Balance.start()
    recDeleteTx.start()
    recTempBlock.start()
    recHashTBlock.start()
    recConfirmSUser.start()
    recBlockchain.start()
    recHashBchain.start()
    recUpdateHshdTx.start()
    recDelCnfrmdTx.start()
    recDelTmpBlock.start()
    recUpdateUsrBalance.start()
     
    
  def checks(self):
    check_pool_valid = self.userRepository.GetFromPool()
    recheck = []
    for check in check_pool_valid:
      rehashed = User.hash_transaction(self, check)
      recheck.append(rehashed)
    b = False
    hashed_before = self.userRepository.GetAllHashForSecurity()
    
    for i in range(len(hashed_before)): 
      if hashed_before[i][1] == recheck[i]:
        b = True
      else:
        b = False
        os.system('color')
        print(f"pool number {hashed_before[i][0]} is", colored('tempered!', 'blue'))
        time.sleep(0.2)

    check_chain_valid = self.userRepository.GetAllBlocks()
    recheck = []
    for i in range(len(check_chain_valid)):
      if check_chain_valid[i][3] == 'Genesis':
        hash_gen = (check_chain_valid[i][0], check_chain_valid[i][1], check_chain_valid[i][2], check_chain_valid[i][3], check_chain_valid[i][4])
        rehashed = User.hash_transaction(self, hash_gen)
        recheck.append(rehashed)
      else:
        check = check_chain_valid[i]
        rehashed = User.hash_transaction(self, check)
        recheck.append(rehashed)
    
    b = False
    hashed_before = self.userRepository.GetAllHashForChain()
    for i in range(len(hashed_before)): 
      if hashed_before[i][1] == recheck[i]:
        b = True
      elif hashed_before[i][1] != recheck[i]:
        b = False
        os.system('color')
        print(f"Block number {hashed_before[i][0]} in the chain is", colored('tempered!', 'red'))
        time.sleep(0.2)  

  
  def GenesisBlock(self):
    bb = BlocklService.Block(self)
    return bb

  def login(self):
    username = input("please enter username: ")
    password = input("please enter password: ")

    try:
      user = self.userRepository.GetUser(username, True)
      key =  self.userRepository.GetKeys(username)
      private_key = serialization.load_pem_private_key(key[4],password=None)
      public_key = serialization.load_pem_public_key(key[3])
      unhashed_password = Transactions.Asym.decrypt(key[2], private_key)
      encoding = 'UTF-8' 
      check_pass = unhashed_password.decode(encoding)
      if user == None or check_pass != password:  # An empty result evaluates to False.
          raise ValueError(f"Login Try with: Username: {username} {password} ", False)
      else:
          self.loggedin = True
          self.tenant = user
          
    except ValueError as error: self.CreateLogFromException(self.login.__name__, error); return

  def close():
    pass
    

  def logout(self):
    self.loggedin = 0
    self.loggedin_user = None
    self.admin_is_loggedin = 0


  def close(self):
    
    pass

  def CreateLogFromException(self, descriptionOfActivity, exception):
    showUser = exception.args[1]
    if showUser:
      print(exception.args[0])
    else:
      print("Login failed fucker")
    