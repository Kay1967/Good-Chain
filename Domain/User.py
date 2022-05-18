import os
import string
import random
from termcolor import colored
import time
from sys import hash_info
import Repository
from  Repository.UserRepository import *
from datetime import datetime as dt
import hashlib
from hashlib import sha256
from Service.BlockService import *

hash_func = lambda x: sha256(x.encode('utf-8')).hexdigest()

class User:
    
    def __init__(self, username, userRepository):
      self.username = username
      self.userRepository = userRepository


    def CheckReceiver(self, username):
      self.username = username
      receiver_name = self.userRepository.GetAllUsers()
      for receiver in receiver_name:

        if receiver[0] == username:
          
          return receiver[0]

      else:
        raise ValueError(f"This user has not signed up yet.")
          

    def hash_transaction(self, transaction):
      hash_info = hash_func(str(transaction))
      return hash_info
