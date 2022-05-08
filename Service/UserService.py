from datetime import datetime as dt
import datetime as dt
from datetime import timedelta
import time
from numpy import add
from termcolor import colored
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

class UserService(Client):
  def __init__(self, tenant, userRepository):
    self.tenant = tenant
    self.userRepository = userRepository
    
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
    #valid_transactions = Client.ValidTx(self)
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
            print(f"Transaction number {transaction[0]} in the pool.")  
          except:
            raise Exception("The table is not found.")
        else:
          print("ERROR! Valid transaction is not verified.")
    else:
      print("Your balance is not enough to transfer the amount.")

    
  def CheckBalance(self):
    username = self.tenant
    chk_balance = self.userRepository.GetUserBalance(username[0])
    today =  dt.now()
    date = today.strftime("%d-%m-%Y")
    time = today.strftime("%H:%M:%S")
    balance = chk_balance[1] + chk_balance[3] + chk_balance[5] - chk_balance[2] - chk_balance[4]
    print(f"User: {username[0]}, you balance on {date} at {time} is: {balance}. ")
    
    print("Please check the last updated details of you balance:")
    
    print(f"=========================== \n"
          f"Initial_balance: {chk_balance[1]} \n"+
          f"amount_sent: {chk_balance[2]} \n"+
          f"amount_received: {chk_balance[3]} \n"+
          f"fee_paid: {chk_balance[4]} \n"+
          f"fee_gained: {chk_balance[5]} \n" 
          )
  time.sleep(0.5)
  print("I am here")

  def ExploreChain(self):
    check_block_valid = self.userRepository.GetAllFromTempBlock()
    recheck = []
    for check in check_block_valid:
      rehashed = User.hash_transaction(self, check)
      recheck.append(rehashed)  
    b = False
    hashed_before = self.userRepository.GetAllHashForBlock()
    for i in range(len(hashed_before)): 
      if hashed_before[i][1] == recheck[i]:
        b = True
        #print(f"Block number {hashed_before[i][0]} is verified {b}!")
        #time.sleep(0.2)  
      else:
        b = False
        os.system('color')
        print(f"Block number {hashed_before[i][0]} is", colored('tempered!', 'yellow'))
        time.sleep(0.2)

    print("Unprocessed Blocks")
    for i in range(len(check_block_valid)):
      print(f"=========================== \n"
            f"Id_No: {check_block_valid[i][0]} \n"+
            f"Username: {check_block_valid[i][1]} \n"+
            f"Nonce: {check_block_valid[i][2]} \n"+
            f"Previous_hash: {check_block_valid[i][3]} \n"+
            f"Data: {check_block_valid[i][4]} \n"+
            f"Duration: {check_block_valid[i][5]} \n"+
            f"Date: {check_block_valid[i][6]} \n"+
            f"Time: {check_block_valid[i][7]} \n"
            )
      time.sleep(0.5)
    

  def CheckPool(self):
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
        
        #print(f"pool number {hashed_before[i][0]} is verified {b}!")
       # time.sleep(0.2)  
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
            
     
  def CancelTransaction(self):
    username = self.tenant
    chk_tx = self.userRepository.GetFromPool()
    
    user_tx_list = []
    for i in range(len(chk_tx)):
      if chk_tx[i][1] == username[0]:
        user_tx_list.append(chk_tx[i])
    print(user_tx_list)
    for usr in user_tx_list:
      if usr[1] == username[0]:
        tx_nr = int(input("Please choose the transaction you want to delete: "))
      if usr[1] == username[0] and usr[0] == tx_nr:
        self.userRepository.DeleteTransaction(tx_nr)
        print(f"Transaction {tx_nr} was successfully deleted from the pool.")
      else:
        print(f"{username[0]}, you have not placed any transaction in the pool yet.")
        
    print("I am here")


  def MineBlock(self):
    
    Leading_zero = 2
    
    username = self.tenant
    #amount_sufficient = Client.CalcSuffAmount(self, username)
    top_valid_transactions = Client.ValidTx(self)
    #keys = Client.KeysForMining(self, username)
    if top_valid_transactions is None:
      print("The number of transactions in the pool is less than five.")
    elif Client.Already_Mined(self) == False:
      print(f"{username[0]}, you have already mined this block")
    else:    
      list_stringify_tx = []
      for tx in top_valid_transactions:
        delimiter = ','
        stringify_tx ='(' + delimiter.join([str(value) for value in tx]) + ')'
        list_stringify_tx.append(stringify_tx)
      print(list_stringify_tx)
      
      mb = BlocklService.chainblock(self, list_stringify_tx)
      print(f"gotchya")
            
      block = self.userRepository.GetLastTempBlock()
      if block is None:
        check_last = self.userRepository.GetLastBlock()
        last_date = check_last[5]
        last_time = check_last[6]
        today =  dt.now()
        date = today.strftime("%d-%m-%Y")
        time = today.strftime("%H:%M:%S")
        last_d = dt.strptime(last_date, "%d-%m-%Y")
        now_d = dt.strptime(date, "%d-%m-%Y")
        start_dt = dt.strptime(last_time, '%H:%M:%S')
        end_dt = dt.strptime(time, '%H:%M:%S')
        interval_time = end_dt - start_dt
        allowed_mins = timedelta(seconds= 180)
        if last_d <= now_d and interval_time.seconds >= allowed_mins.seconds:
          self.userRepository.CreateTempBlock(username[0], mb[0], mb[1], mb[2], mb[3], mb[4])
          block = self.userRepository.GetLastTempBlock()
          check_block = User.hash_transaction(self, block)
          self.userRepository.CreateHashForBlock(check_block)
        else:
          print(F"{username[0]}, the time intervan between your block and the last one is less than 3 minutes.")
      else:
        check_last = self.userRepository.GetLastTempBlock()
        last_date = check_last[7]
        last_time = check_last[8]
        today =  dt.now()
        date = today.strftime("%d-%m-%Y")
        time = today.strftime("%H:%M:%S")
        last_d = dt.strptime(last_date, "%d-%m-%Y")
        now_d = dt.strptime(date, "%d-%m-%Y")
        start_dt = dt.strptime(last_time, '%H:%M:%S')
        end_dt = dt.strptime(time, '%H:%M:%S')
        interval_time = end_dt - start_dt
        allowed_mins = timedelta(seconds= 180)
        print("I am mb[4]: ",mb[4])
        if last_d <= now_d and interval_time.seconds >= allowed_mins.seconds and mb[4] > 10 and mb[4] < 20:
          self.userRepository.CreateTempBlock(username[0], mb[0], mb[1], mb[2], mb[3], mb[4])
          block = self.userRepository.GetLastTempBlock()
          check_block = User.hash_transaction(self, block)
          self.userRepository.CreateHashForBlock(check_block)
        else:
          print(F"{username[0]}, the time interval between your block and the last one is less than 3 minutes.")
      print("I did it")
        
  
  def ConfirmBlock(self):
    username = self.tenant
    confirming_user = self.userRepository.GetAllUsers()
    list_confirmed = []
    for i in range(len(confirming_user)):
      list_confirmed.append(confirming_user[i][3])
    if sum(list_confirmed) == 0: 
        print(f"Welcome {username[0]}, you are the first user to confirm the block.")
    if sum(list_confirmed) == 1:
        print(f"Welcome {username[0]}, you are the second user to confirm the block.")
    if sum(list_confirmed) == 2:
        print(f"Welcome {username[0]}, you are the third user to confirm the block.")
    
    confirming_user = self.userRepository.GetAllUsers()
    list_confirmed = []
    for i in range(len(confirming_user)):
      list_confirmed.append(confirming_user[i][3])
    new_list = []
    for i in range(len(list_confirmed)):
      if list_confirmed[i] != 0:
        new_list.append(list_confirmed[i])
    if len(new_list) == 3: 
      print(f"{username[0]}, you cannot confirm anything, because three users have already confirmed the block.")     
    else:
      check_block_valid = self.userRepository.GetAllFromTempBlock()
      recheck = []
      for check in check_block_valid:
        rehashed = User.hash_transaction(self, check)
        recheck.append(rehashed)
        
      b = False
      hashed_before = self.userRepository.GetAllHashForBlock()
      for i in range(len(hashed_before)): 
        if hashed_before[i][1] == recheck[i]:
          b = True #here I have to add some code to exclude tempered blocks
          print(f"Block number {hashed_before[i][0]} is verified!")
          time.sleep(0.2)  
        else:
          b = False
          print(f"Block number {hashed_before[i][0]} is tempered!")
          time.sleep(0.2)

      if b == False:
        print(f"The invalid block cannot be loaded into the process of confirmation.")    
      else:

        mined_blocks = self.userRepository.GetAllFromTempBlock()
        list_duration = []
        for i in range(len(mined_blocks)):
          list_duration.append(mined_blocks[i][6])
        print(list_duration) # I should delete this later
        
        min_duration = min(list_duration)
        print("This is the least time taken for mining a block amongst all: ", min_duration)
        
        for i in range(len(mined_blocks)):
          if min_duration == mined_blocks[i][6]:
            block_to_confirm = mined_blocks[i]
        if block_to_confirm[1] == username[0]:
          print(f"{username[0]}, you cannot confirm your own block.")
        else:
        
          for i in range(len(mined_blocks)):
            if min_duration == mined_blocks[i][6]:
              block_to_confirm = mined_blocks[i]
              confirmation_status = 1 
              self.userRepository.UpdateConfirmationStatus(confirmation_status, username[0])

        
          confirming_users = self.userRepository.GetAllUsers()
          list_confirmed = []
          for i in range(len(confirming_users)):
            list_confirmed.append(confirming_users[i][3])
          if sum(list_confirmed) == 1: 
            print(f"{username[0]} is the first person who confirmed the block number {block_to_confirm[0]}")
          if sum(list_confirmed) == 2:
            print(f"{username[0]} is the second person who confirmed the block number {block_to_confirm[0]}")
          if sum(list_confirmed) == 3:
            print(f"{username[0]} is the third person who confirmed the block number {block_to_confirm[0]}")
          
          confirming_status = []
          for i in range(len(confirming_users)):
            if confirming_users[i][3] != 0:
              confirming_status.append(confirming_users[i][3])
          if len(confirming_status) == 3:
            top_valid_tx = Client.ValidTx(self)
            Blc = self.userRepository.GetLastBlock()
            B = self.userRepository.GetAllFromTempBlock()
            
            for i in range(len(B)):
              if B[i][6] == min_duration and B[i][3] == Blc[2] and B[i][5] == Blc[4]:
                print(f"{B[i][0]} is already added to the Blockchain.")
              else:
                if B[i][6] == min_duration:
                  add_block = B[i]
                  if Blc[4] == add_block[3]:
                    self.userRepository.CreateBlockChain(add_block[2], add_block[3], add_block[4], add_block[5])
                  
                    block_in_chain = self.userRepository.GetLastBlock()
                    check_blockchain = User.hash_transaction(self, block_in_chain)
                    self.userRepository.CreateHashForChain(check_blockchain)
                    print (f"Success! Valid block is {len(confirming_status)} times verified and added to the chain.")
                    for i in range(len(B)):
                      self.userRepository.DeleteTempBlock(B[i][0])
                      print(f"Temporary blocks were deleted.")
                  else:
                    print ("Error! Valid block is not verified.")
                
          # user balance must be updated accordingly
          if len(confirming_status) == 3: 
            for i in range(len(top_valid_tx)):
              if top_valid_tx[i][1] == add_block[1]:
                fee_received = 0
                fee_gained = 0
                for j in range(len(top_valid_tx)):
                  fee_received += top_valid_tx[j][4]
                previous_fee = self.userRepository.GetUserBalance(top_valid_tx[i][1])
                fee_gained = fee_received + previous_fee[5]
                status = 'fee_gained'
                self.userRepository.UpdateUserBalance(status, fee_gained, top_valid_tx[i][1])
            
            for i in range(len(top_valid_tx)):
              if top_valid_tx[i][1] == add_block[1]:
                mined_reward = 50
                previous_reward = self.userRepository.GetUserBalance(top_valid_tx[i][1])
                mined_reward = mined_reward + previous_reward[6]
                status = 'mined_reward'
                self.userRepository.UpdateUserBalance(status, mined_reward, top_valid_tx[i][1])
            
            users_balance = self.userRepository.GetBalance()
            user_list = []
            for i in range(len(users_balance)):
              user_list.append(users_balance[i][0]) 
            for user in user_list:
              amount_sent = 0
              tx_paid = 0
              for i in range(len(top_valid_tx)):
                if top_valid_tx[i][1] == user:
                  tx_paid += top_valid_tx[i][3]
                  previous_sent = self.userRepository.GetUserBalance(user)
                  amount_sent = tx_paid + previous_sent[2]

              status = 'amount_sent'
              self.userRepository.UpdateUserBalance(status, amount_sent, user)

            for user in user_list:
              fee_sent = 0
              fee_paid = 0
              for i in range(len(top_valid_tx)):
                if top_valid_tx[i][1] == user:
                  fee_sent += top_valid_tx[i][4]
                  previous_paid = self.userRepository.GetUserBalance(user)
                  fee_paid = fee_sent + previous_paid[4]
              status = 'fee_paid'
              self.userRepository.UpdateUserBalance(status, fee_paid, user)

            for user in user_list:
              tx_received = 0
              amount_received = 0
              for i in range(len(top_valid_tx)):
                if top_valid_tx[i][2] == user:
                  tx_received += top_valid_tx[i][3]
                  previous_received = self.userRepository.GetUserBalance(user)
                  amount_received = tx_received + previous_received[3]
              status = 'amount_received' 
              self.userRepository.UpdateUserBalance(status, amount_received, user)   
              

            # update the status of validators
            for user in user_list:
              confirmation_status = 0 
              self.userRepository.UpdateConfirmationStatus(confirmation_status, user)
              print("I am here!")
            #probably only delete the block which is chained

            
            
          print("Seems everything is working seamlessly")