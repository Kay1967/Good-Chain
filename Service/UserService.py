import os
from datetime import datetime as dt
import datetime as dt
from datetime import timedelta
import time
import socket
from xmlrpc.client import Server
#from numpy import add
from termcolor import colored
#from tabulate import tabulate
import Transactions
from Transactions.Transaction import *
from Transactions.TxBlock import *
from Repository.UserRepository import *
import Domain
import Service
from Domain.User import *
from Domain.Client import *
#from Domain.ServerClient import *
#from Domain.ClientServer import *
from Service.BlockService import *
from Component.UserInterface import *
from Service.ServerService import *
from Service.ClientService import *
from Service.LoginService import *

class UserService(Client):
  def __init__(self, tenant, userRepository):
    self.tenant = tenant
    self.userRepository = userRepository
    # self.TCP_IP = '172.25.237.64'
    # self.BUFFER_SIZE = 10024
    self.clientService = ClientService()
    
    #self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
  def TransferCoins(self):
    receiver_name = input("please enter the receiver name: ")
    checked_receiver = User.CheckReceiver(self, receiver_name)
    if (receiver_name == checked_receiver):
      print("This is: ", checked_receiver, "the receiver.")
    else:
      raise ValueError("The given receiver_name is invalid.") 
   
    username = self.tenant
    print("This is: ", username[1], "the sender.")
    if username[1] == checked_receiver:
      raise ValueError ("You cannot send money to yourself!")
    username = self.tenant
    amount_sufficient = Client.CalcSuffAmount(self, username)
    
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
      signature = str(bytes(tx.sigs[0]))
      #signature = tx.sigs[0]
      print(signature)
    
      try:
          today =  dt.now()
          date = today.strftime("%d-%m-%Y")
          time = today.strftime("%H:%M:%S") 
          tx_to_db = (username[1], checked_receiver, amount_to_send, transaction_fee, signature, date, time)
          self.userRepository.CreateTransactionPool(tx_to_db)
          transaction = self.userRepository.GetLastFromPool()
          tx_return = (transaction[1], transaction[2], transaction[3], transaction[4], transaction[5], transaction[6], transaction[7])
          #tx_result = self.clientService.sendObject(self.userRepository.GetLastFromPoolId(transaction[0]), 1233) 
          tx_result = self.clientService.sendObject(tx_return, 1233)     
          print("Tx is sent from pc ", tx_result)
          check_transaction = User.hash_transaction(self, transaction)
          transaction_status = 0
          hashed_tx = (check_transaction, transaction_status)
          self.userRepository.CreateHashForSecurity(hashed_tx)
          hash_for_result = self.clientService.sendObject(hashed_tx, 1234)
          print("Hashed Tx is sent from pc ", hash_for_result)
          print(f"Transaction number {transaction[0]} is in the pool now.") 
          print("I am here")
          if tx_result == False:
            self.userRepository.DeleteTransaction(transaction[0]) 
          
          tx_to_verify = self.userRepository.GetFromPool()
          for i in range(len(tx_to_verify)):
            if tx_to_verify[i][1] != username[1]:
              tx_for_key = tx_to_verify[i][1]
              rx_for_rec = tx_to_verify[i][2]
              amount_to_send = tx_to_verify[i][3]
              search_savekeys= self.userRepository.GetKeys(tx_for_key)
              search_savedkeys= self.userRepository.GetKeys(rx_for_rec)
              pbcKey_sender = search_savekeys[3]
              pbcKey_receiver = search_savedkeys[3]
              prvKey_sender =  search_savekeys[4]
              pbcKS = serialization.load_pem_public_key(pbcKey_sender)
              prvKS= serialization.load_pem_private_key(prvKey_sender,password=None)
              pbcKR = serialization.load_pem_public_key(pbcKey_receiver)
              tx = Tx()
              tx.add_input(pbcKS, amount_to_send)
              tx.add_output(pbcKR, amount_to_send)
              tx.sign(prvKS)
              signy= tx_to_verify[i][5]
              signy1 = tx.sigs[0]
              ver = verify(tx.variadic_arity(), signy, pbcKS)
              if ver == True: 
                print(f"SUCCESS! Valid transaction number {tx_to_verify[i][0]} is verified.")
              else:
                print("ERROR! Valid transaction is not verified.")
      except:
          raise Exception("The table is not found.")
      #else:
          #print("ERROR! Valid transaction is not verified.")
    else:
      print("Your balance is not enough to transfer the amount.")
    
    
  def CheckBalance(self):
    username = self.tenant
    chk_balance = self.userRepository.GetUserBalance(username[0])
    today =  dt.now()
    date = today.strftime("%d-%m-%Y")
    time = today.strftime("%H:%M:%S")
    balance = chk_balance[1] + chk_balance[3] + chk_balance[5] + chk_balance[6] - chk_balance[2] - chk_balance[4]
    print(f"User: {username[0]}, you balance on {date} at {time} is: {balance}. ")
    
    print("Please check the last updated details of you balance:")
    
    print(f"=========================== \n"
          f"Initial_balance: {chk_balance[1]} \n"+
          f"amount_sent: {chk_balance[2]} \n"+
          f"amount_received: {chk_balance[3]} \n"+
          f"fee_paid: {chk_balance[4]} \n"+
          f"fee_gained: {chk_balance[5]} \n"+
          f"mined_reward: {chk_balance[6]} \n" 
          )
  time.sleep(0.5)
  
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
      else:
        b = False
        os.system('color')
        print(f"Block number {hashed_before[i][0]} is", colored('tempered!', 'yellow'))
        time.sleep(0.2)

    print("Unprocessed Blocks:")
    if len(check_block_valid) > 0:
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
    else:
      print("No block has been mined yet.")

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
        
      else:
        b = False
        print(f"pool number {hashed_before[i][0]} is tempered! {b}")
        time.sleep(0.2)
        
    print("Unprocessed transactions:")
    if len(check_pool_valid) > 0:
      for i in range(len(check_pool_valid)):
        print(f"=========================== \n"
              f"Tx_No: {check_pool_valid[i][0]} \n"+
              f"Sender: {check_pool_valid[i][1]} \n"+
              f"Receiver: {check_pool_valid[i][2]} \n"+
              f"Tx_value: {check_pool_valid[i][3]} \n"+
              f"Tx_fee: {check_pool_valid[i][4]} \n"
              )
        time.sleep(0.5)
    else:
      print("No transaction has been loaded into the pool")
         
  def CancelTransaction(self):
    username = self.tenant
    chk_tx = self.userRepository.GetFromPool()
    
    user_tx_list = []
    for i in range(len(chk_tx)):
      if chk_tx[i][1] == username[1]:
        user_tx_list.append(chk_tx[i])
    print(user_tx_list)
    for i in range(len(user_tx_list)):
      if user_tx_list[i][1] == username[1]:
        print(user_tx_list[i][1])
        tx_nr = int(input("Please choose the transaction you want to delete: "))
        print(user_tx_list[i][0])
      if user_tx_list[i][1] == username[1] and user_tx_list[i][0] == tx_nr:

        self.userRepository.DeleteTransaction(tx_nr)
        delete_result = self.clientService.sendObject(tx_nr, 1238)

        print(f"Transaction {tx_nr} was successfully deleted from the pool.")
      #else:
        #print(f"{username[1]}, you have not placed any transaction in the pool yet.")
        


  def MineBlock(self):
    
    Leading_zero = 2
    
    username = self.tenant
    
    top_valid_transactions = Client.ValidTx(self)
  
    if top_valid_transactions is None:
      print("The number of transactions in the pool is less than five.")
    elif Client.Already_Mined(self) == False:
      print(f"{username[1]}, you have already mined this block")
    else:    
      list_stringify_tx = []
      for tx in top_valid_transactions:
        delimiter = ','
        stringify_tx ='(' + delimiter.join([str(value) for value in tx]) + ')'
        list_stringify_tx.append(stringify_tx)
      
      
      mb = BlocklService.chainblock(self, list_stringify_tx)
      
            
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
          temp_block = (username[1], mb[0], mb[1], mb[2], mb[3], mb[4], date, time)
          self.userRepository.CreateTempBlock(temp_block)
          block = self.userRepository.GetLastTempBlock()
          tempB = (block[1], block[2], block[3], block[4], block[5], block[6], block[7], block[8])
          check_block = User.hash_transaction(self, block)
          self.userRepository.CreateHashForBlock(check_block)
          block_result = self.clientService.sendObject(tempB, 1239)
          hashT_result = self.clientService.sendObject(check_block, 1240)
          if block_result == False:
            self.userRepository.DeleteTempBlock(block[0])
        else:
          print(F"{username[1]}, the time interval between your block and the last one is less than 3 minutes.")
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
        
        if last_d <= now_d and interval_time.seconds >= allowed_mins.seconds and mb[4] > 10 and mb[4] < 20:
          temp_block = (username[1], mb[0], mb[1], mb[2], mb[3], mb[4], date, time)
          self.userRepository.CreateTempBlock(temp_block)
          block = self.userRepository.GetLastTempBlock()
          tempB = (block[1], block[2], block[3], block[4], block[5], block[6], block[7], block[8])
          check_block = User.hash_transaction(self, block)
          self.userRepository.CreateHashForBlock(check_block)
          block_result = self.clientService.sendObject(tempB, 1239)
          hashT_result = self.clientService.sendObject(check_block, 1240)
          if block_result == False:
            self.userRepository.DeleteTempBlock(block[0])
        else:
          print(F"{username[1]}, the time interval between your block and the last one is less than 3 minutes.")
      
        
  
  def ConfirmBlock(self):
    username = self.tenant
    confirming_user = self.userRepository.GetAllUsers()
    list_confirmed = []
    for i in range(len(confirming_user)):
      list_confirmed.append(confirming_user[i][4])
    if sum(list_confirmed) == 0: 
        print(f"Welcome {username[1]}, you are the first user to confirm the block.")
    if sum(list_confirmed) == 1:
        print(f"Welcome {username[1]}, you are the second user to confirm the block.")
    if sum(list_confirmed) == 2:
        print(f"Welcome {username[1]}, you are the third user to confirm the block.")
    
    confirming_user = self.userRepository.GetAllUsers()
    list_confirmed = []
    for i in range(len(confirming_user)):
      list_confirmed.append(confirming_user[i][4])
    new_list = []
    for i in range(len(list_confirmed)):
      if list_confirmed[i] != 0:
        new_list.append(list_confirmed[i])
    if len(new_list) == 3: 
      print(f"{username[1]}, you cannot confirm anything, because three users have already confirmed the block.")     
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
          b = True 

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
        
        
        min_duration = min(list_duration)
        print("This is the least time taken for mining a block amongst all: ", min_duration)
        
        for i in range(len(mined_blocks)):
          if min_duration == mined_blocks[i][6]:
            block_to_confirm = mined_blocks[i]
        if block_to_confirm[1] == username[1]:
          print(f"{username[1]}, you cannot confirm your own block.")
        else:
        
          for i in range(len(mined_blocks)):
            if min_duration == mined_blocks[i][6]:
              block_to_confirm = mined_blocks[i]
              confirmation_status = 1
              confirms = (confirmation_status, username[1])
              self.userRepository.UpdateConfirmationStatus(confirms)
              user_result = self.clientService.sendObject(confirms, 1241)  

        
          confirming_users = self.userRepository.GetAllUsers()
          list_confirmed = []
          for i in range(len(confirming_users)):
            list_confirmed.append(confirming_users[i][4])
          if sum(list_confirmed) == 1: 
            print(f"{username[1]} is the first person who confirmed the block number {block_to_confirm[0]}")
          if sum(list_confirmed) == 2:
            print(f"{username[1]} is the second person who confirmed the block number {block_to_confirm[0]}")
          if sum(list_confirmed) == 3:
            print(f"{username[1]} is the third person who confirmed the block number {block_to_confirm[0]}")
          
          confirming_status = []
          for i in range(len(confirming_users)):
            if confirming_users[i][4] != 0:
              confirming_status.append(confirming_users[i][4])
          if len(confirming_status) == 3:
            top_valid_tx = Client.ValidTx(self)
            Blc = self.userRepository.GetLastBlock()
            B = self.userRepository.GetAllFromTempBlock()
            
            for i in range(len(B)):
              if B[i][6] == min_duration and B[i][3] == Blc[2] and B[i][5] == Blc[4] and B[i][3]== B[i][5]:
                print(f"{B[i][0]} is already added to the Blockchain.")
              else:
                if B[i][6] == min_duration:
                  add_block = B[i]
                  if Blc[4] == add_block[3]:
                    today =  dt.now()
                    date = today.strftime("%d-%m-%Y")
                    time = today.strftime("%H:%M:%S")
                    addBlc= (add_block[2], add_block[3], add_block[4], add_block[5], date, time)
                    self.userRepository.CreateBlockChain(addBlc)

                    block_in_chain = self.userRepository.GetLastBlock()
                    blc_for_server = (block_in_chain[1], block_in_chain[2], block_in_chain[3], block_in_chain[4], block_in_chain[5], block_in_chain[6])
                    check_blockchain = User.hash_transaction(self, block_in_chain)
                    self.userRepository.CreateHashForChain(check_blockchain)
                    print (f"Success! Valid block is {len(confirming_status)} times verified and added to the chain.")
                    chain_result = self.clientService.sendObject(blc_for_server, 1242)
                    HashCH_result = self.clientService.sendObject(check_blockchain, 1243)
                    top_valid_transactions = Client.ValidTx(self)
                    
                    verified_list = top_valid_transactions
                    
                    hashed_vl = []
                    for vl in verified_list:
                      hash_vl = User.hash_transaction(self, vl)
                      hashed_vl.append(hash_vl)
                    hashed_transactions = self.userRepository.GetAllHashForSecurity()
                    for i in range(len(hashed_transactions)): 
                      if hashed_transactions[i][1] == hashed_vl[i]:
                        ht_txNo = hashed_transactions[i][0]
                        transaction_status = 1
                        tx_numbers = (transaction_status, ht_txNo) 
                        self.userRepository.UpdateHashForSecurity(tx_numbers)
                        updateHS_result = self.clientService.sendObject(tx_numbers, 1244)
                    
                    delete_mined_tx = self.userRepository.GetAllHashForSecurity()
                    
                    for i in range(len(delete_mined_tx)): 
                      if delete_mined_tx[i][2] == 1:
                        tx_status = delete_mined_tx[i][2] 
                        tx_number = delete_mined_tx[i][0]
                        print(tx_number)
                        self.userRepository.DeleteConfirmedTransactions(tx_number)
                        print(f"Confirmed transaction number {tx_number} was deleted.")
                        updateHS_result = self.clientService.sendObject(tx_number, 1245)
                    for i in range(len(B)):
                      self.userRepository.DeleteTempBlock(B[i][0])
                      DelTB_result = self.clientService.sendObject(B[i][0], 1246)
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
                fee_gained = fee_received + previous_fee[6] # it was [5]
                status = 'fee_gained'
                values_update = (status, fee_gained, top_valid_tx[i][1])
                self.userRepository.UpdateUserBalance(values_update)
                fee_result = self.clientService.sendObject(values_update, 1247)
            
            for i in range(len(top_valid_tx)):
              if top_valid_tx[i][1] == add_block[1]:
                mined_reward = 50
                previous_reward = self.userRepository.GetUserBalance(top_valid_tx[i][1])
                mined_reward = mined_reward + previous_reward[7] # it was [6]
                status = 'mined_reward'
                values_update = (status, mined_reward, top_valid_tx[i][1])
                self.userRepository.UpdateUserBalance(values_update)
                reward_result = self.clientService.sendObject(values_update, 1247)
            users_balance = self.userRepository.GetBalance()
            user_list = []
            for i in range(len(users_balance)):
              user_list.append(users_balance[i][1]) # it was [0]
            for user in user_list:
              amount_sent = 0
              tx_paid = 0
              for i in range(len(top_valid_tx)):
                if top_valid_tx[i][1] == user:
                  tx_paid += top_valid_tx[i][3]
                  previous_sent = self.userRepository.GetUserBalance(user)
                  amount_sent = tx_paid + previous_sent[3] # it was [2]

              status = 'amount_sent'
              values_update = (status, amount_sent, user)
              self.userRepository.UpdateUserBalance(values_update)
              amount_result = self.clientService.sendObject(values_update, 1247)
            for user in user_list:
              fee_sent = 0
              fee_paid = 0
              for i in range(len(top_valid_tx)):
                if top_valid_tx[i][1] == user:
                  fee_sent += top_valid_tx[i][4]
                  previous_paid = self.userRepository.GetUserBalance(user)
                  fee_paid = fee_sent + previous_paid[5] # it was [4]
              status = 'fee_paid'
              values_update = (status, fee_paid, user)
              self.userRepository.UpdateUserBalance(values_update)
              fpaid_result = self.clientService.sendObject(values_update, 1247)

            for user in user_list:
              tx_received = 0
              amount_received = 0
              for i in range(len(top_valid_tx)):
                if top_valid_tx[i][2] == user:
                  tx_received += top_valid_tx[i][3]
                  previous_received = self.userRepository.GetUserBalance(user)
                  amount_received = tx_received + previous_received[4] # it was [3]
              status = 'amount_received' 
              values_update = (status, amount_received, user)
              self.userRepository.UpdateUserBalance(values_update)
              recamount_result = self.clientService.sendObject(values_update, 1247)  
              

            # update the status of validators
            for user in user_list:
              confirmation_status = 0 
              confirms = (confirmation_status, user)
              self.userRepository.UpdateConfirmationStatus(confirms)
              updtstatus = self.clientService.sendObject(confirms, 1241)  
  

  # def sendObject(self, transaction, tcpPort):
  #     try:
  #         s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  #         s.connect((self.TCP_IP, tcpPort))
  #         s.send(pickle.dumps(transaction))
  #         # s.setblocking(False)
  #         data = s.recv(self.BUFFER_SIZE)
  #         if data == b'1':
  #             print('item successfully added to other node')
  #             s.close()
  #             return True
  #         else:
  #             print('item failed to add to the other node and will be removed.0')
  #             s.close()
  #             return False
  #     except:
  #         print('item failed to add to the other node and will be removed.1')
  #         return False