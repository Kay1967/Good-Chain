import time
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
import hashlib
from hashlib import sha256



hash_func = lambda x: sha256(x.encode('utf-8')).hexdigest()
class CBlock:
  previousHash = None
  currentHash = None
  previousBlock = None
  data = None
  nonce = 0
  duration = 0
  def __init__(self, data, previousBlock):
      self.data = data
      self.previousBlock = previousBlock
      self.CurrentHash = hash_func(str(data))
      self.nonce = 1
      self.duration = 0
      if previousBlock is not None:
        self.previousHash = self.previousBlock

  def mine(self, leading_zeros):
    leading_str = '0' * leading_zeros
    if self.previousBlock is not None:
        self.previousHash = self.previousBlock #.currentHash
    
    #start = time.time()
    for Nonce in range(1000000):
      #start = time.time()
      self.nonce = Nonce
      block_to_be_mined = str(self.data) + str(Nonce)
      if self.previousBlock != None:
          block_to_be_mined += str(self.previousHash)
      block_to_be_mined = hash_func(block_to_be_mined)
      if block_to_be_mined.startswith(leading_str):
        self.currentHash = block_to_be_mined
        # print(f"it is the nounce: {self.nonce}")
        # end = time.time()
        # self.duration = end - start
        #time.sleep(5)
        #print(f"It took {self.duration} to mine this block")
        #return
    # end = time.time()
    # self.duration = end - start
    # print(f"It took {self.duration} to mine this block")
    return
  def is_valid_hash(self):
    currentBlock = self
    check = True
    while currentBlock is not None:
      coming_block = str(currentBlock.data) #+ str(currentBlock.nonce)
      if currentBlock.previousBlock is not None:
        coming_block += str(currentBlock.previousHash)
      newHash = hash_func(coming_block)
      if newHash != currentBlock.CurrentHash:
        check = False
      else:
        check = True
      currentBlock = currentBlock.previousBlock
    return check
