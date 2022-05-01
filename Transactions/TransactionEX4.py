import Transactions
from Transactions.SignatureEX4 import *

class Tx:
  inputs = None
  outputs =None
  sigs = None

  def __init__(self):
      self.inputs = []
      self.outputs = []
      self.sigs = []

  def add_input(self, from_addr, amount):
    #for i in self.inputs:
      if self.inputs is not None:
        self.inputs.append([from_addr, amount])


  def add_output(self, to_addr, amount):
    if self.outputs is not None:
      self.outputs.append([to_addr, amount])

  def sign(self, private):
    sigList = self.bytesTostr()
    self.sigs.append(sign(sigList, private))
   
  # def sign(self, private):
  #       allLists = self.concateLists()
  #       self.sigs.append(sign(allLists, private))

  # def concateLists(self):
  #       result = [*self.inputs, *self.outputs]
  #       return result
  
  def bytesTostr(self):
    add_to_list = [*self.inputs, *self.outputs]
    return add_to_list

    # #if self.sigs is not None:
    #   #self.sigs = []
    # self.sigs.append(private)
    # for i in range(len(self.inputs)):
    #   if self.inputs is not None:
    #     msg_to_be_signed = str(self.inputs[i]).encode()
    #     byte_msg = bytes(msg_to_be_signed)
    # for i in range(len(self.sigs)):
    #     sign(byte_msg, self.sigs[i])
        

    
    # for i in range(len(self.outputs)):
    #   if self.outputs is not None:
    #     msg_to_be_signed = str(self.outputs[i]).encode()
    #     byte_msg = bytes(msg_to_be_signed)
    #     self.sigs = sign(byte_msg, private)
    



      

