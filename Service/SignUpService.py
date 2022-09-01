from ast import Raise
from datetime import datetime as dt
from Component.UserInterface import *
import Transactions
from Transactions.Signature import *
from Transactions.Asym import *
from Service.ServerService import *
from Service.ClientService import *
from Service.LoginService import *
from Domain.User import *
import View
from View.LoginView import *
import hashlib
from hashlib import sha256

hash_func = lambda x: sha256(x.encode('utf-8')).hexdigest()

class SignUpService:
  Tx_No = None
  Sender_username = None
  Receiver_username = None
  Tx_value = None
  Tx_fee = None
  amount_sent = None
  amount_received = None
  fee_paid = None
  fee_gained = None
  
  loggedin = False
  prv_key, pub_key = Transactions.Asym.generate_keys()

  def __init__(self, userRepository):
    
    self.userRepository = userRepository
    self.clientService = ClientService()
    #self.loginView = LoginView()
    
    
  def SignUp(self):
    
    username = input("please register a new username: ") 
    def reg_user():
      user_name = username
      #try:
      users_exist = self.userRepository.GetAllUsers()
      for user in users_exist:
        if user_name == user[0]:
          print("this username is already taken, please make another one.")
          SignUpService.SignUp(self)
      
    reg_user()
    
    def reg_pass():
      amount_sent = None
      amount_received = None
      fee_paid = None
      fee_gained = None
      password = input("please enter a password: ")
      hashed_pwd = hash_func(password)
      password_repeat = input("please repeat your password: ")
      hashed_rePwd = hash_func(password_repeat)
    
      if hashed_pwd == hashed_rePwd:
        try:
          initialbalance=50
          confirmation_status = 0
          today =  dt.now()
          date = today.strftime("%d-%m-%Y")
          time = today.strftime("%H:%M:%S")
          #hashed_pwd = hash_func(password)
          init_user = (username, hashed_pwd, initialbalance, confirmation_status, date, time)
          amount_sent = 0
          amount_received = 0
          fee_paid = 0
          fee_gained = 0
          mined_reward = 0
          usr_balance = (username, initialbalance, amount_sent, amount_received, fee_paid, fee_gained, mined_reward)
          
          public_key = SignUpService.pub_key
          private_key = SignUpService.prv_key
          prv_ser = private_key.private_bytes(
                      encoding=serialization.Encoding.PEM,
                      format=serialization.PrivateFormat.TraditionalOpenSSL,
                      encryption_algorithm=serialization.NoEncryption()  
                      )
          pbc_ser = public_key.public_bytes(
                  encoding=serialization.Encoding.PEM,
                  format=serialization.PublicFormat.SubjectPublicKeyInfo
                  )
          byte_password = bytes(str(password), 'UTF-8')
          encrypt_password = Transactions.Asym.encrypt(byte_password, public_key)
          keys_init = (username, encrypt_password, pbc_ser, prv_ser, date, time)
          
          self.userRepository.CreateUser(init_user)
          self.userRepository.SaveKeys(keys_init)
          self.userRepository.CreateUsersBalance(usr_balance)
          
          usr_to_match = self.userRepository.GetUser(init_user[0])
          signup_result= (usr_to_match[1], usr_to_match[2], usr_to_match[3], usr_to_match[4], usr_to_match[5], usr_to_match[6])
          user_result = self.clientService.sendObject(signup_result, 1235)
          
          if user_result == False:
            self.userRepository.DeleteUserName(usr_to_match[0])
          
          keys_return = self.userRepository.GetKeys(keys_init[0])
          keys_result = (keys_return[1], keys_return[2], keys_return[3], keys_return[4], keys_return[5], keys_return[6])
          keys_sent = self.clientService.sendObject(keys_result, 1236)
         
          if keys_sent == False:
            self.userRepository.DeleteKeys(keys_return[0])

          usrbalance_return = self.userRepository.GetLastUserBalance(usr_balance[0])
          usrbalance_result = (usrbalance_return[1], usrbalance_return[2], usrbalance_return[3], usrbalance_return[4], usrbalance_return[5], usrbalance_return[6], usrbalance_return[7])
          usrbalance_sent = self.clientService.sendObject(usrbalance_result, 1237)

          if usrbalance_sent == False:
            self.userRepository.DeleteUsersBalance(usrbalance_return[0])
            
          print("I am sent from the pc: ", user_result)
          print("I am sent from the pc: ", keys_sent)
          print("I am sent from the pc: ", usrbalance_sent)
          

        except:
          raise Exception ("password does not match!")
      if user_result == True or user_result == False:
        LoginView.GetMenu(self)
       
      else:
        print("password does not match, try again!")
        reg_pass()
    reg_pass()


    