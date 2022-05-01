from datetime import datetime as dt
import time
#from Domain.User import *

import tabulate
from tabulate import tabulate
import Transactions
from Transactions.Transaction import *
from Transactions.TxBlock import *
from Repository.UserRepository import *
import Domain
import Service
from Domain.User import *
from Domain.Client import *
from Service.BlockService import *
from Component.UserInterface import *
#from Repository.ClientRepository import *

# every actions in the context of an advisor
class UserService:
  def __init__(self, tenant, userRepository):
    self.tenant = tenant
    self.userRepository = userRepository
    
  def CreateAdvisor(self):
    pass
    
  def TransferCoins(self):
    receiver_name = input("please enter the receiver name: ")
    checked_receiver = User.CheckReceiver(self, receiver_name)
    if (receiver_name == checked_receiver):
      print("Hi, I am ", checked_receiver, "the receiver.")
    else:
      raise ValueError("The given receiver_name is invalid.") 
   
    username = self.tenant
    print("Hi, I am ", username[0], "the sender.")
    if username[0] == checked_receiver:
      raise ValueError ("You cannot send money to yourself!")
    username = self.tenant
    amount_sufficient = Client.CalcSuffAmount(self, username)
    valid_transactions = Client.ValidTx(self)
    keys = Client.KeysForMining(self, username)
       
    amount_to_send = float(input("please enter the amount you would like to send: "))
    if amount_to_send <= 0:
      raise ValueError ("The amount you will send cannot be zero or less than 0.")
    transaction_fee = float(input("please enter the fee you will pay: "))
    if transaction_fee < 0:
      raise ValueError ("The fee you will pay cannot less than zero.")
    
    if amount_sufficient > amount_to_send + transaction_fee:
      print(f"Your balance is {amount_sufficient}, you may proceed!")
    else:
      raise ValueError (f"Your balance is {amount_sufficient}, it is not enough to make a transaction.")
    tx = Tx()
    if amount_sufficient > 0 and amount_to_send > 0 and transaction_fee >= 0 and username[0] != checked_receiver and amount_to_send > transaction_fee:
      tx.add_input(keys[0], amount_to_send)
      tx.add_output(keys[1], amount_to_send)
      tx.sign(keys[2])
      #self.userRepository.CreateTransactionPool(username[0], checked_receiver, amount_to_send, transaction_fee)
      #print(f"transaction is in the pool in pending mode")
      for sign in tx.sigs:
        ver = verify(tx.variadic_arity(), sign, keys[0])
        if ver == True:
          print(f"SUCCESS! Valid transaction is verified.")
          try:
            self.userRepository.CreateTransactionPool(username[0], checked_receiver, amount_to_send, transaction_fee)
            transaction = self.userRepository.GetLastFromPool()
            check_transaction = User.hash_transaction(self, transaction)
            self.userRepository.CreateHashForSecurity(check_transaction)
            print(f"Transaction number {transaction[0]} in the pool is in {transaction[5]} mode.")  
          except:
            raise Exception("The table is not found.")
        else:
          print("ERROR! Valid transaction is not verified.")
    else:
      print("Your balance is not enough to transfer the amount.")

    
  def CheckBalance(self):
    
    print("I am here")

      

  def ExploreChain(self):
    # if self.tenant is not Advisor and self.tenant is not SysAdmin and self.tenant is not SuperAdmin:
    # Haspermission is a method that gives back a boolean based on if the tenant has the permission UpdateAdvisorPassword
    # if not self.tenant.HasPermission(Permission.UpdateAdvisorPassword):
    #   print("Unauthorized")
    #   self.loggingRepository.CreateLog(self.tenant.username, f"{self.UpdatePasswordForAdvisor.__name__}", "Unauthorized", 1)
    #   return

    # if type(self.tenant) is Advisor:
    #   advisor = self.tenant
    #   print("Password criteria:\nCannot be the same as old password\nBetween 7 and 31 characters\nWith atleast one uppercase, one lowercase and one special\n")
    #   newPassword = input("please enter a new password: ")
    #   try: self.tenant.UpdatePassword(newPassword)
    #   except ValueError as error: self.CreateLogFromException(self.UpdatePasswordForAdvisor.__name__, error); return
    # else:
    #   try:
    #     advisor = self.GetAndValidateAdvisor()
    #     advisor.GenerateAndUpdatePassword() 
    #   except ValueError as error: self.CreateLogFromException(self.UpdatePasswordForAdvisor.__name__, error); return    
    
    # self.userRepository.UpdatePassword(advisor.username, advisor.password)  
    # self.loggingRepository.CreateLog(self.tenant.username, f"{self.UpdatePasswordForAdvisor.__name__}: {advisor.username}", "Success", "0")
    # print("New Password for " + advisor.username + ". Password: " + advisor.password)
    print("I am here")

  def CheckPool(self):
    check_pool_valid = self.userRepository.GetFromPool()
    recheck = []
    for check in check_pool_valid:
      rehashed = User.hash_transaction(self, check)
      recheck.append(rehashed)
      #return recheck
    b = False
    hashed_before = self.userRepository.GetAllHashForSecurity()
    for i in range(len(hashed_before)): 
      if hashed_before[i][1] == recheck[i]:
        b = True
        print(f"pool number {hashed_before[i][0]} is verified {b}!")
        time.sleep(0.2)  
      else:
        b = False
        print(f"pool number {hashed_before[i][0]} is tempered! {b}")
        time.sleep(0.2)
        
    print("Unprocessed transactions")
    for i in range(len(check_pool_valid)):
      print(f"=========================== \n"
            f"Tx_No: {check_pool_valid[i][0]} \n"+
            f"Sender: {check_pool_valid[i][1]} \n"+
            f"Receiver: {check_pool_valid[i][2]} \n"+
            f"Tx_value: {check_pool_valid[i][3]} \n"+
            f"Tx_fee: {check_pool_valid[i][4]} \n"
            )
      time.sleep(0.5)
            #f"Date: {all_blocks[i][5]} \n"+
            #f"Time: {all_blocks[i][6]} \n"
     

        
        
  def CancelTransaction(self):
    if self.CheckPool() == False:
      print("assignment my ass!")

    # username = input("please enter username: ")
    # user = self.userRepository.GetUser(username)
    # if type(user) is not Advisor:
    #   raise ValueError("User is not an advisor", True)

    # return user
    print("I am here")
  
  def MineBlock(self):
    
    Leading_zero = 2
    #Gn = CBlock("Genesis", None)
    #Gn.mine(Leading_zero)
    username = self.tenant
    amount_sufficient = Client.CalcSuffAmount(self, username)
    valid_transactions = Client.ValidTx(self)
    keys = Client.KeysForMining(self, username)
      
    if len(valid_transactions) <= 3 and len(valid_transactions) >= 3:
      list_stringify_tx = []
      for tx in valid_transactions:
        delimiter = ','
        stringify_tx ='(' + delimiter.join([str(value) for value in tx]) + ')'
        list_stringify_tx.append(stringify_tx)
      print(list_stringify_tx)
      mb = BlocklService.chainblock(self, list_stringify_tx)
      print(f"gotchya")

    # if count >= 1 and count <= 1:
    #   if sufficient_amount > 0 and amount_to_send > 0 and transaction_fee > 0  and amount_to_send > transaction_fee:
    #     claimed = [] 
    #     for i in range(len(hashed_before)): 
    #       if hashed_before[i][1] == recheck[i]:
    #         claimed.append(hashed_before[i][1])
    #       mb = BlocklService.chainblock(self, claimed)
    print("I did it")
          
           
          
          
      #     B = TxBlock(root)
      #     B.addTx(transaction_list[1])
      # for b in [root, B]:
      #   if b.is_valid():
      #       print ("Success! Valid block is verified.")
      #   else:
      #       print ("Error! Valid block is not verified.")


          
      #     tx.sign(prvKey_sender)
      #     for sign in tx.sigs:
      #       ver = verify(tx.bytesTostr(), sign, pbcKey_sender)
              
      #       if ver == True:
      #         try:
      #           b = TxBlock(tx) 
      #           for b in [b]:
      #             if b.is_valid():
      #               print ("Success! Valid block is verified.")
      #             else:
      #               print ("Error! Valid block is not verified.") 
      #         except:
      #           raise ValueError ("wrong shyte")



    print("I am here")