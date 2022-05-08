from ast import Raise
from datetime import datetime as dt
from Component.UserInterface import *
import Transactions
from Transactions.Signature import *
from Transactions.Asym import *



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
      print("yay")
      password = input("please enter a password: ")
      password_repeat = input("please repeat your password: ")
    
      if password == password_repeat:
        try:
          initialbalance=50
          confirmation_status = 0
          self.userRepository.CreateUser(username, password, initialbalance, confirmation_status)
         
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
          self.userRepository.SaveKeys(username, encrypt_password, pbc_ser, prv_ser)
          self.userRepository.CreateUsersBalance(username, initialbalance, amount_sent = 0, amount_received = 0, fee_paid = 0, fee_gained = 0, mined_reward = 0)
        except:
          raise Exception ("password does not match!")
      else:
        print("password does not match, try again!")
        reg_pass()
    reg_pass()


    