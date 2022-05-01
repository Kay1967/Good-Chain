from Transactions.Signature import *

class Tx:

  inputs = None
  outputs =None
  sigs = None
  reqd = None
  
  def __init__(self):
    self.inputs = []
    self.outputs = []
    self.sigs = []
    self.reqd = []
  
  def add_input(self, from_addr, amount):
    self.inputs.append((from_addr, amount))
    self.sum_inputs = 0
    for i in range (len(self.inputs)):
      self.sum_inputs += self.inputs[i][1]
    self.positive_values_in = 0 
    for i in range(len(self.inputs)):
      if self.inputs[i][1] > 0:
        self.positive_values_in = self.inputs[i][1]
      
  def add_output(self, to_addr, amount):
    self.outputs.append((to_addr, amount))
    self.sum_outputs = 0
    for i in range (len(self.outputs)):
      self.sum_outputs += self.outputs[i][1]
    self.positive_values_out = 0 
    for i in range(len(self.outputs)):
      if self.outputs[i][1] > 0:
        self.positive_values_out = self.outputs[i][1]
    
  def add_reqd(self, public):
    self.reqd.append(public)
  
  def sign(self, private):
    sigValues = self.variadic_arity()
    self.sigs.append(sign(sigValues, private))        

  def is_valid(self):
              
    if(len(self.inputs) > len(self.outputs)):
      return False
    
    if (len(self.reqd) > 0):     
          if (self.sum_inputs >= self.sum_outputs):
            if (self.positive_values_in > 0 and self.positive_values_out > 0):   
              for i in range(len(self.sigs)):
                  verf_value = self.variadic_arity()
                  if(i == 0):
                    validity2 = verify(verf_value, self.sigs[i], self.inputs[i][0])
                  if (i == 1):
                    validity1 = verify(verf_value, self.sigs[i], self.reqd[0])
                
                    if (validity1 == validity2):
                      return True

    else:
      if (self.sum_inputs >= self.sum_outputs):
        if (self.positive_values_in > 0 and self.positive_values_out > 0):
          for i in range(len(self.sigs)):
            verf_value = self.variadic_arity()
            
            validity = verify(verf_value, self.sigs[i], self.inputs[i][0])
            return validity
              
  def variadic_arity(self):
    self.asterisk_values= (*self.inputs, *self.outputs)
    return self.asterisk_values