from heapq import nlargest
from operator import itemgetter
import re
from Repository.UserRepository import *
from Service.UserService import *
from Service.BlockService import *
import socket, pickle
import time

class Client:
  

#class ClientService:

  #def __init__(self):
  #TCP_IP = '127.0.0.1'#'172.25.237.64'
  #BUFFER_SIZE = 1024
  valid_tx = None
  already_mined = None
  sufficient_balance = None
  def __init__(self, tenant, userRepository):
    self.tenant = tenant
    self.userRepository = userRepository
    self.TCP_IP = '172.25.237.64'
    self.BUFFER_SIZE = 1024
    #self.userService = userService

  def CalcSuffAmount(self, tenant):
    username = tenant
    user_turnover = self.userRepository.GetUserBalance(username[1])
    if username[1] == user_turnover[1] and user_turnover[3] is None and user_turnover[4] is None and user_turnover[5] is None and user_turnover[6] is None:
      amount_sent = 0
      amount_received = 0
      fee_paid = 0
      fee_gained = 0
      minied_reward = 0
      initial_balance = user_turnover[2]
      sufficient_amount = initial_balance + amount_received - amount_sent - fee_paid + fee_gained + mined_reward
      print(sufficient_amount)
      return sufficient_amount

    elif  username[1] == user_turnover[1] and user_turnover[3] is not None and user_turnover[4] is not None and user_turnover[5] is not None and user_turnover[6] is not None:
      initial_balance = user_turnover[2]
      amount_sent = user_turnover[3]
      amount_received = user_turnover[4]
      fee_paid = user_turnover[5]
      fee_gained = user_turnover[6]
      mined_reward = user_turnover[7]
      sufficient_amount = initial_balance + amount_received - amount_sent - fee_paid + fee_gained + mined_reward
      print(f"Last balance: {sufficient_amount}")
      return sufficient_amount 

  def ValidTx(self):
    check_pool_valid = self.userRepository.GetFromPool()
    hashed_before = self.userRepository.GetAllHashForSecurity()
    recheck = []
    for check in check_pool_valid:
      rehashed = User.hash_transaction(self, check)
      recheck.append(rehashed)
    list_validTx = [] 
    for i in range(len(hashed_before)): 
      if hashed_before[i][1] == recheck[i]:
        list_validTx.append(hashed_before[i])
    
    txlist_for_mine = []
    tempered = []
    for i in range(len(check_pool_valid)):
      for j in range(len(list_validTx)):
        if check_pool_valid[i][0] == list_validTx[j][0]:
          txlist_for_mine.append(check_pool_valid[i])
    tempered = [item for item in check_pool_valid if item not in txlist_for_mine] 
    for tmprd in tempered: 
      print(f"Tempered transaction(s) number {tmprd[0]} is/are not loaded into the block.")
    #return txlist_for_mine
    if len(txlist_for_mine) >= 1  and len(txlist_for_mine) <= 10:
      count = len(txlist_for_mine)
      top_largest = nlargest(count, check_pool_valid, key=itemgetter(4))
      return txlist_for_mine

  def KeysForMining(self, tenant):

      object_sender = self.userRepository.GetKeys(tenant[1])
      if object_sender is not None:
        pubkey_sender = object_sender[3]
        prvkey_sender = object_sender[4]
        pbcKey_sender = serialization.load_pem_public_key(pubkey_sender)
        prvKey_sender = serialization.load_pem_private_key(prvkey_sender,password=None)
      object_receiver = self.userRepository.GetKeys(tenant[1])
      if object_receiver is not None:
        pubkey_receiver = object_receiver[3]
        pbcKey_receiver = serialization.load_pem_public_key(pubkey_receiver)

        return pbcKey_sender, pbcKey_receiver, prvKey_sender
  
  def Already_Mined(self):
    username = self.tenant
    top_valid_transactions = self.ValidTx()
    list_stringify_tx = []
    for tx in top_valid_transactions:
      delimiter = ','
      stringify_tx ='(' + delimiter.join([str(value) for value in tx]) + ')'
      list_stringify_tx.append(stringify_tx)
    
    mb = BlocklService.chainblock(self, list_stringify_tx)
    
    already_mined = self.userRepository.GetAllFromTempBlock()
    new_list_block = []
    list_stringify_data = []
    for i in range(len(already_mined)):
      alm = already_mined[i][4]
      list_stringify_data = alm.split(" - ")
      new_list_block.append(list_stringify_data)
    
    b = True
    for i in range(len(already_mined)):
      if already_mined[i][1] == username[0] and already_mined[i][3] == mb[1]:
        print(f"{username[0]}")
        b = False
    
    c = True
    for nlist in new_list_block:
      if set(nlist) == set(list_stringify_tx):
        c = False
      

    if b == False and c == False:
      return False
    else:
      return True
    
  def sendObject(self, transaction, tcpPort):
      try:
          s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
          s.connect((self.TCP_IP, tcpPort))
          s.send(pickle.dumps(transaction))
          # s.setblocking(False)
          data = s.recv(self.BUFFER_SIZE)
          if data == b'1':
              print('item successfully added to other node')
              s.close()
              return True
          else:
              print('item failed to add to the other node and will be removed.0')
              s.close()
              return False
      except:
          print('item failed to add to the other node and will be removed.1')
          return False
