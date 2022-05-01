import os
import time

from datetime import datetime as dt
from Component.UserInterface import *
# from Domain.Advisor import Advisor
# from Domain.SuperAdmin import SuperAdmin
# from Domain.SysAdmin import SysAdmin
import Domain
#from Domain.User import *
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
    
    #self.loggingRepository = loggingRepository
    #self.permissionRepository = permissionRepository
  def checks(self):
    #self.userService.CheckPool()
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
          #self.setPermissions()
          #self.userRepository.UpdateLastLogin(dt.now(), self.tenant.username)
    except ValueError as error: self.CreateLogFromException(self.login.__name__, error); return

  # def setPermissions(self):
  #   if type(self.tenant) is Advisor:
  #       self.tenant.hasPermissions = self.permissionRepository.GetAllPermissionsForAdvisor()
  #   if type(self.tenant) is SysAdmin:
  #       self.tenant.hasPermissions = self.permissionRepository.GetAllPermissionsForSysAdmin()
  #   if type(self.tenant) is SuperAdmin:
  #       self.tenant.hasPermissions = self.permissionRepository.GetAllPermissionsForSuperAdmin()

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
    #self.loggingRepository.CreateLog("Anonymous", descriptionOfActivity, f"ValueError:{exception.args[0]}", "1")
