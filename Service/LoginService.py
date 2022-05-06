import os
import time

from datetime import datetime as dt
from Component.UserInterface import *

import Domain

from termcolor import colored
import Service
from Service.SignUpService import *
import Transactions
from Transactions.Asym import *
from Service.UserService import *

class LoginService:
  loggedin = False

  def __init__ (self, userRepository, userService):
    self.userRepository = userRepository
    self.userService = userService
    
  def checks(self):
    check_pool_valid = self.userRepository.GetFromPool()
    recheck = []
    for check in check_pool_valid:
      rehashed = User.hash_transaction(self, check)
      recheck.append(rehashed)
    
    hashed_before = self.userRepository.GetAllHashForSecurity()
    for i in range(len(hashed_before)): 
      if hashed_before[i][1] == recheck[i]:
        print(f"pool number {hashed_before[i][0]} is verified!")
        time.sleep(0.2)  
      else:
        os.system('color')
        print(f"pool number {hashed_before[i][0]} is", colored('tempered!', 'blue'))
        time.sleep(0.2)

    check_chain_valid = self.userRepository.GetAllBlocks()
    recheck = []
    for check in check_chain_valid:
      rehashed = User.hash_transaction(self, check)
      recheck.append(rehashed)
    
    b = False
    hashed_before = self.userRepository.GetAllHashForChain()
    for i in range(len(hashed_before)): 
      if hashed_before[i][1] == recheck[i]:
        b = True
        print(f"Block number {hashed_before[i][0]} in the chain is verified!")
        time.sleep(0.2)  
      else:
        b = False
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
      private_key = serialization.load_pem_private_key(key[3],password=None)
      public_key = serialization.load_pem_public_key(key[2])
      unhashed_password = Transactions.Asym.decrypt(key[1], private_key)
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
      print("Login failed")
    