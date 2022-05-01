import os
from Component.UserInterface import *
import Transactions
from Transactions.Signature import *
from Transactions.BlockChain import *
import tabulate
from tabulate import tabulate
from termcolor import colored

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
    Block.mine(leading_zeros)
    nonce = Block.nonce
    previous_hash = Block.previousBlock
    
    current_hash = Block.CurrentHash
    list_data_str = '-'.join([str(elem) for elem in data])
    print(list_data_str)
    # check_blocks = self.userRepository.GetAllBlocks()
    # if len(check_blocks) == 1:
    self.userRepository.CreateBlockChain(nonce, previous_hash, list_data_str, current_hash)
      # else:
      #   list_data = []
      #   for i in range(1, len(check_blocks), 1):
      #     hash_data = hash_func(check_blocks[i][3])
      #     list_data.append(hash_data)
      #   hash_new_data = hash_func(data)
      
      #   for dt in list_data:
      #     if dt == hash_new_data:
      #      print(f"Transaction number {check_blocks[i][0]} is already in the block")
      #     if dt != hash_new_data:
      #      self.userRepository.CreateBlockChain(nonce, previous_hash, data, current_hash)

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
