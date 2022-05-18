import os
from Component.UserInterface import *
import Transactions
from Transactions.Signature import *
from Transactions.BlockChain import *
import tabulate
from tabulate import tabulate
from termcolor import colored
from Domain.User import *

hash_func = lambda x: sha256(x.encode('utf-8')).hexdigest()

class BlocklService:  
  loggedin = False

  def __init__(self, userRepository):
    #self.tenant = tenant
    self.userRepository = userRepository
    #self.userService = userService
  def Block(self):
    all_blocks = self.userRepository.GetAllBlocks()
    if len(all_blocks) == 0:
      leading_zeros = 2
      data = "Genesis"
      Gn = CBlock(data, None)
      Gn.mine(leading_zeros)
      nonce = Gn.nonce
      previous_hash = Gn.previousHash
      data = Gn.data
      current_hash = Gn.currentHash
      self.userRepository.CreateBlockChain(nonce, previous_hash, data, current_hash)
      block_in_chain = self.userRepository.GetLastBlock()
      check_blockchain = User.hash_transaction(self, block_in_chain)
      self.userRepository.CreateHashForChain(check_blockchain)
    
    #if all_blocks[0][0] == 1 and all_blocks[0][3] == "Genesis":
    all_blocks = self.userRepository.GetAllBlocks()
    for i in range(len(all_blocks)):
      print(f"BlcNo: {all_blocks[i][0]} \n"
            f"Nonce: {all_blocks[i][1]} \n"+
            f"Previous_hash: {all_blocks[i][2]} \n"+
            f"data: {all_blocks[i][3]} \n"+
            f"Current_hash: {all_blocks[i][4]} \n"+
            f"Date: {all_blocks[i][5]} \n"+
            f"Time: {all_blocks[i][6]} \n"+
            f"=========================== \n")
  
  def chainblock(self, transaction):
    leading_zeros = 2
    data = transaction#transaction_list.inputs[1]
    last_block = self.userRepository.GetLastBlock()
    
    previous_block = last_block[4]
    Block = CBlock(data, previous_block)
    #start = time.time()
    Block.mine(leading_zeros)
    #time.sleep(5)
    #end = time.time()
    #duration = end - start
    nonce = Block.nonce
    previous_hash = Block.previousBlock
    time_taken = Block.duration
    #time_taken = duration
    #print("It took ", time_taken, "seconds to mine this block.")
    current_hash = Block.currentHash
    list_data_str = ' - '.join([str(elem) for elem in data])
    #print(list_data_str)
    return nonce, previous_hash, list_data_str, current_hash, time_taken
    

    all_blocks = self.userRepository.GetAllBlocks()
    for i in range(len(all_blocks)):
       print(f"BlcNo: {all_blocks[i][0]} \n"
            f"Nonce: {all_blocks[i][1]} \n"+
            f"Previous_hash: {all_blocks[i][2]} \n"+
            f"data: {all_blocks[i][3]} \n"+
            f"Current_hash: {all_blocks[i][4]} \n"+
            f"Date: {all_blocks[i][5]} \n"+
            f"Time: {all_blocks[i][6]} \n")
    
    print("you got here")
