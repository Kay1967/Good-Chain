import re
from Repository.UserRepository import *
from Service.UserService import *

class Client:
  valid_tx = None
  sufficient_balance = None
  def __init__(self, tenant, userRepository):
    self.tenant = tenant
    self.userRepository = userRepository

  def CalcSuffAmount(self, tenant):
    username = tenant
    user_turnover = self.userRepository.GetUserBalance(username[0])
    if username[0] == user_turnover[0] and user_turnover[2] is None and user_turnover[3] is None and user_turnover[4] is None and user_turnover[5] is None:
      amount_sent = 0
      amount_received = 0
      fee_paid = 0
      fee_gained = 0
      initial_balance = user_turnover[1]
      sufficient_amount = initial_balance + amount_received - amount_sent - fee_paid + fee_gained
      print(sufficient_amount)
      return sufficient_amount

    elif  username[0] == user_turnover[0] and user_turnover[2] is not None and user_turnover[3] is not None and user_turnover[4] is not None and user_turnover[5] is not None:
      initial_balance = user_turnover[1]
      amount_sent = user_turnover[2]
      amount_received = user_turnover[3]
      fee_paid = user_turnover[4]
      fee_gained = user_turnover[5]
      sufficient_amount = initial_balance + amount_received - amount_sent - fee_paid + fee_gained
      print(sufficient_amount)
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
    for i in range(len(check_pool_valid)):
      for j in range(len(list_validTx)):
        if check_pool_valid[i][0] == list_validTx[j][0]:
          txlist_for_mine.append(check_pool_valid[i])
    return txlist_for_mine

  def KeysForMining(self, tenant):
    # txlist_for_keys = self.Validtx()
    # for keys in txlist_for_keys:
      object_sender = self.userRepository.GetKeys(tenant[0])
      if object_sender is not None:
        pubkey_sender = object_sender[2]
        prvkey_sender = object_sender[3]
        pbcKey_sender = serialization.load_pem_public_key(pubkey_sender)
        prvKey_sender = serialization.load_pem_private_key(prvkey_sender,password=None)
      object_receiver = self.userRepository.GetKeys(tenant[0])
      if object_receiver is not None:
        pubkey_receiver = object_receiver[2]
        pbcKey_receiver = serialization.load_pem_public_key(pubkey_receiver)

        return pbcKey_sender, pbcKey_receiver, prvKey_sender
  

    