from sqlite3 import SQLITE_TRANSACTION
from flask import g
from datetime import datetime as dt
import Domain
from Domain.User import *
#
import hashlib
from hashlib import sha256
import Transactions
from Transactions.Asym import *

hash_func = lambda x: sha256(x.encode('utf-8')).hexdigest()
class UserRepository:

  def __init__ (self, db, tenant = None):
    self.dbContext = db
    
  def GetUser(self, username, login = False):
    queryParameters = (username,)
    sql_statement = '''SELECT * from users WHERE LOWER(username)=LOWER(?)'''
    try: userEncrypted = self.dbContext.executeAndFetchOne(sql_statement, queryParameters)
    except:
      raise ValueError ("Cannot get user!")

    if userEncrypted is None and login is False:
      raise ValueError("User not found", True)
    if userEncrypted is None and login is True:
      raise ValueError("Login failed", True)

    userRecord = userEncrypted
    return userRecord

  def GetAllUsers(self):
    sql_statement = f"SELECT * FROM users"
    try: userRecords = self.dbContext.executeAndFetchAll(sql_statement, None)
    except:
      raise ValueError ("no user was found")

    allUsers = []
    for userRecord in userRecords:
      allUsers.append(userRecord)
      
    return allUsers 

  def GetKeys(self, username):
    queryParameters = (username,)
    sql_statement = '''SELECT * from SaveKeys WHERE LOWER(username)=LOWER(?)'''
    get_keys =  self.dbContext.executeAndFetchOne(sql_statement, queryParameters)
    userRecord = get_keys
    return userRecord
  
  def CreateUser(self, username, password, initialbalance, confirmation_status):
    hashed_password = hash_func(str(password))
    Values = (username, hashed_password, initialbalance, confirmation_status)
    sql_statement = '''INSERT INTO users (username, password, initialbalance, confirmation_status) VALUES (?,?,?,?)'''
    self.dbContext.executeAndCommit(sql_statement, Values)
  
  def CreateTempBlock(self, username, nonce, previous_hash, data, current_hash, duration):
    today =  dt.now()
    date = today.strftime("%d-%m-%Y")
    time = today.strftime("%H:%M:%S")
    Values = (username, nonce, previous_hash, data, current_hash, duration, date, time)
    sql_statement = '''INSERT INTO TempBlock (username, nonce, previous_hash, data, current_hash, duration, date, time) VALUES (?,?,?,?,?,?,?,?)'''
    self.dbContext.executeAndCommit(sql_statement, Values)

  def GetAllFromTempBlock(self):
    allUsers = []
    sql_statement = '''SELECT * from TempBlock'''
    try: 
      userRecords = self.dbContext.executeAndFetchAll(sql_statement, None)
      if userRecords is None:
        allUsers = None
        return allUsers
    except:
      raise ValueError ("nothing found")

    for userRecord in userRecords:
      allUsers.append(userRecord)
    return allUsers 

  def GetLastTempBlock(self):
    queryParameters = None
    sql_statement = '''SELECT * from TempBlock ORDER BY Id_No DESC LIMIT 1'''
    get_transaction =  self.dbContext.executeAndFetchOne(sql_statement, queryParameters)
    userRecord = get_transaction
    return userRecord  

  def CreateBlockChain(self, nonce, previous_hash, data, current_hash):
    today =  dt.now()
    date = today.strftime("%d-%m-%Y")
    time = today.strftime("%H:%M:%S")
    Values = (nonce, previous_hash, data, current_hash, date, time)
    sql_statement = '''INSERT INTO BlockChain (nonce, previous_hash, data, current_hash, date, time) VALUES (?,?,?,?,?,?)'''
    self.dbContext.executeAndCommit(sql_statement, Values)
  
  def GetAllBlocks(self):
    sql_statement = f"SELECT * FROM BlockChain"
    try: userRecords = self.dbContext.executeAndFetchAll(sql_statement, None)
    except:
      raise ValueError ("no block was found")

    allUsers = []
    for userRecord in userRecords:
      allUsers.append(userRecord)
    return allUsers 
  
  def GetLastBlock(self):
    queryParameters = None
    sql_statement = '''SELECT * from BlockChain ORDER BY Blc_No DESC LIMIT 1'''
    get_transaction =  self.dbContext.executeAndFetchOne(sql_statement, queryParameters)
    userRecord = get_transaction
    return userRecord
  
  
  def CreateUsersBalance(self, username, initialbalance, amount_sent, amount_received, fee_paid, fee_gained, mined_reward):
    
    Values = (username, initialbalance, amount_sent, amount_received, fee_paid, fee_gained, mined_reward)
    sql_statement = '''INSERT INTO UsersBalance (username, initialbalance, amount_sent, amount_received, fee_paid, fee_gained, mined_reward) VALUES (?,?,?,?,?,?,?)'''
    self.dbContext.executeAndCommit(sql_statement, Values)

  def SaveKeys(self, username, password, publickey, privatekey):

    Values = (username, password, publickey, privatekey)
    sql_statement = '''INSERT INTO SaveKeys (username, password, public_key, private_key) VALUES (?,?,?,?)'''
    self.dbContext.executeAndCommit(sql_statement, Values)
  
  def CreateTransactionPool(self, Sender_username, Receiver_username, Tx_value, Tx_fee):
    today =  dt.now()
    date = today.strftime("%d-%m-%Y")
    time = today.strftime("%H:%M:%S")
   
    Values = (Sender_username, Receiver_username, Tx_value, Tx_fee, date, time)
    sql_statement = '''INSERT INTO TransactionPool (Sender_username, Receiver_username, Tx_value, Tx_fee, date, time) VALUES (?,?,?,?,?,?)'''
    self.dbContext.executeAndCommit(sql_statement, Values)
  
  def GetLastFromPool(self):
    queryParameters = None
    sql_statement = '''SELECT * from TransactionPool ORDER BY Tx_No DESC LIMIT 1'''
    get_transaction =  self.dbContext.executeAndFetchOne(sql_statement, queryParameters)
    userRecord = get_transaction
    return userRecord

  def GetFromPool(self):
    allUsers = []
    sql_statement = '''SELECT * from TransactionPool'''
    try: 
      userRecords = self.dbContext.executeAndFetchAll(sql_statement, None)
      if userRecords is None:
        allUsers = None
        return allUsers
    except:
      raise ValueError ("nothing found")

    for userRecord in userRecords:
      allUsers.append(userRecord)
    return allUsers 
  
  def GetBalance(self):
    allUsers = []
    sql_statement = '''SELECT * from UsersBalance'''
    try: 
      userRecords = self.dbContext.executeAndFetchAll(sql_statement, None)
      if userRecords is None:
        allUsers = None
        return allUsers
    except:
      raise ValueError ("nothing found")

    for userRecord in userRecords:
      allUsers.append(userRecord)
    return allUsers 

  def GetUserBalance(self, username, login = False):
    queryParameters = (username,)
    sql_statement = '''SELECT * from UsersBalance WHERE LOWER(username)=LOWER(?)'''
    try: userEncrypted = self.dbContext.executeAndFetchOne(sql_statement, queryParameters)
    except: 
      raise ValueError ("Cannot get balance of the user!")

    if userEncrypted is None and login is False:
      raise ValueError("User not found", True)
    if userEncrypted is None and login is True:
      raise ValueError("Login failed", True)

    userRecord = userEncrypted
    return userRecord

  def UpdateUserBalance(self, status, amount,username):
    if status == 'amount_sent':
      Values = (amount,username)
      sql_statement = '''UPDATE UsersBalance SET amount_sent=? WHERE username=?'''
      try: self.dbContext.executeAndCommit(sql_statement, Values)
      except:
        raise ValueError ("Cannot update the column!")
    if status == 'amount_received':
      Values = (amount, username)
      sql_statement = '''UPDATE UsersBalance SET amount_received=? WHERE username=?'''
      try: self.dbContext.executeAndCommit(sql_statement, Values)
      except:
        raise ValueError ("Cannot update the column!")
    if status == 'fee_paid':
      Values = (amount, username)
      sql_statement = '''UPDATE UsersBalance SET fee_paid=? WHERE username=?'''
      try: self.dbContext.executeAndCommit(sql_statement, Values)
      except:
        raise ValueError ("Cannot update the column!")
    if status == 'fee_gained':
      Values = (amount, username)
      sql_statement = '''UPDATE UsersBalance SET fee_gained=? WHERE username=?'''
      try: self.dbContext.executeAndCommit(sql_statement, Values)
      except:
        raise ValueError ("Cannot update the column!")
    if status == 'mined_reward':
      Values = (amount, username)
      sql_statement = '''UPDATE UsersBalance SET mined_reward=? WHERE username=?'''
      try: self.dbContext.executeAndCommit(sql_statement, Values)
      except:
        raise ValueError ("Cannot update the column!")

  def DeleteTransaction(self, transaction_number):
    Values = (transaction_number,)
    sql_statement = '''DELETE FROM TransactionPool WHERE Tx_No =?'''
    try: self.dbContext.executeAndCommit(sql_statement, Values)
    except:
       raise ValueError ("Cannot delete the row you required!")
    
    sql_statement = '''DELETE FROM HashForSecurity WHERE Tx_No =?'''
    try: self.dbContext.executeAndCommit(sql_statement, Values)
    except:
       raise ValueError ("Cannot delete the row you required!")
       
  def UpdateConfirmationStatus(self, confirmation_status, username):
    Values = (confirmation_status, username)
    sql_statement = '''UPDATE users SET confirmation_status=? WHERE username=?'''
    try: self.dbContext.executeAndCommit(sql_statement, Values)
    except:
      raise ValueError ("Cannot update the column!")
  
  def CreateHashForSecurity(self, hashed_transactions):
    Values = (hashed_transactions,)
    sql_statement = '''INSERT INTO HashForSecurity (hashed_transactions) VALUES (?)'''
    try:
      self.dbContext.executeAndCommit(sql_statement, Values)
    except:
      raise ValueError("no such a table")

  def GetAllHashForSecurity(self):
    allUsers = []
    sql_statement = '''SELECT * from HashForSecurity'''
    try: 
      userRecords = self.dbContext.executeAndFetchAll(sql_statement, None)
      if userRecords is None:
        allUsers = None
        return allUsers
    except:
      raise ValueError ("nothing found")

    for userRecord in userRecords:
      allUsers.append(userRecord)
    return allUsers 

  def CreateHashForBlock(self, hashed_blocks):
    Values = (hashed_blocks,)
    sql_statement = '''INSERT INTO HashForBlock (hashed_blocks) VALUES (?)'''
    try:
      self.dbContext.executeAndCommit(sql_statement, Values)
    except:
      raise ValueError("no such a table")

  def GetAllHashForBlock(self):
    allUsers = []
    sql_statement = '''SELECT * from HashForBlock'''
    try: 
      userRecords = self.dbContext.executeAndFetchAll(sql_statement, None)
      if userRecords is None:
        allUsers = None
        return allUsers
    except:
      raise ValueError ("nothing found")

    for userRecord in userRecords:
      allUsers.append(userRecord)
    return allUsers 

  def CreateHashForChain(self, hashed_blocks):
    Values = (hashed_blocks,)
    sql_statement = '''INSERT INTO HashForChain (hashed_chain) VALUES (?)'''
    try:
      self.dbContext.executeAndCommit(sql_statement, Values)
    except:
      raise ValueError("no such a table")

  def GetAllHashForChain(self):
    allUsers = []
    sql_statement = '''SELECT * from HashForChain'''
    try: 
      userRecords = self.dbContext.executeAndFetchAll(sql_statement, None)
      if userRecords is None:
        allUsers = None
        return allUsers
    except:
      raise ValueError ("nothing found")

    for userRecord in userRecords:
      allUsers.append(userRecord)
    return allUsers 
  
  def DeleteTempBlock(self, Id_No):
    Values = (Id_No,)
    sql_statement = '''DELETE FROM TempBlock WHERE Id_No=?'''
    try: self.dbContext.executeAndCommit(sql_statement, Values)
    except:
       raise ValueError ("Cannot delete the table you required!")
    Value = (Id_No,)
    sql_statement = '''DELETE FROM HashForBlock WHERE Tx_No=?'''
    try: self.dbContext.executeAndCommit(sql_statement, Value)
    except:
       raise ValueError ("Cannot delete the table you required!")