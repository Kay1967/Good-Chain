from msilib.schema import Error
from sqlite3 import SQLITE_TRANSACTION
from flask import g
from datetime import datetime as dt
#from matplotlib import get_backend
import Domain
from Domain.User import *
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
      raise ValueError("Login failed", True, LoginView.GetMenu(self))
      
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
  
  def CreateUser(self, init_user):
    try:
      Values = (init_user[0], init_user[1], init_user[2], init_user[3], init_user[4], init_user[5])
      sql_statement = '''INSERT INTO users (username, password, initialbalance, confirmation_status, date, time) VALUES (?,?,?,?,?,?)'''
      self.dbContext.executeAndCommit(sql_statement, Values)
      return True
    except Exception as e:
      print(e)
      return False
  
  def CreateTempBlock(self, temp_block): 
    try:
      Values = (temp_block[0], temp_block[1], temp_block[2], temp_block[3], temp_block[4], temp_block[5], temp_block[6], temp_block[7])
      sql_statement = '''INSERT INTO TempBlock (username, nonce, previous_hash, data, current_hash, duration, date, time) VALUES (?,?,?,?,?,?,?,?)'''
      self.dbContext.executeAndCommit(sql_statement, Values)
      return True
    except Exception as e:
      print(e)
      return False

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

  def CreateBlockChain(self, addBlock):
    try:
      Values = (addBlock[0], addBlock[1], addBlock[2], addBlock[3], addBlock[4], addBlock[5])
      sql_statement = '''INSERT INTO BlockChain (nonce, previous_hash, data, current_hash, date, time) VALUES (?,?,?,?,?,?)'''
      self.dbContext.executeAndCommit(sql_statement, Values)
      return True
    except Exception as e:
      print(e)
      return False
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
  
  
  def CreateUsersBalance(self, user_balance):
    try:
      Values = (user_balance[0], user_balance[1], user_balance[2], user_balance[3], user_balance[4], user_balance[5], user_balance[6])
      sql_statement = '''INSERT INTO UsersBalance (username, initialbalance, amount_sent, amount_received, fee_paid, fee_gained, mined_reward) VALUES (?,?,?,?,?,?,?)'''
      self.dbContext.executeAndCommit(sql_statement, Values)
      return True
    except Exception as e:
      print(e)
      return False
      
  def GetLastUserBalance(self, username):
    queryParameters = (username,)
    sql_statement = '''SELECT * from UsersBalance WHERE LOWER(username)=LOWER(?)'''
    get_balance =  self.dbContext.executeAndFetchOne(sql_statement, queryParameters)
    userRecord = get_balance
    return userRecord

  def SaveKeys(self, keys_init):
    try:
      Values = (keys_init[0], keys_init[1], keys_init[2], keys_init[3], keys_init[4], keys_init[5])
      sql_statement = '''INSERT INTO SaveKeys (username, password, public_key, private_key, date, time) VALUES (?,?,?,?,?,?)'''
      self.dbContext.executeAndCommit(sql_statement, Values)
      return True
    except Exception as e:
      print(e)
      return False
  
  def CreateTransactionPool(self, tx_to_db):
   try:
      Values = (tx_to_db[0], tx_to_db[1], tx_to_db[2], tx_to_db[3], tx_to_db[4], tx_to_db[5], tx_to_db[6])
      sql_statement = '''INSERT INTO TransactionPool (Sender_username, Receiver_username, Tx_value, Tx_fee, sig, date, time) VALUES (?,?,?,?,?,?,?)'''
      self.dbContext.executeAndCommit(sql_statement, Values)
      return True
   except Exception as e:
      print(e)
      return False
  
  def GetLastFromPool(self):
    queryParameters = None
    sql_statement = '''SELECT * from TransactionPool ORDER BY Tx_No DESC LIMIT 1'''
    #sql_statement = '''SELECT Sender_username, Receiver_username, Tx_value, Tx_fee, sig, date, time FROM TransactionPool WHERE Tx_value != 0 ORDER BY Tx_No DESC LIMIT 1'''
    get_transaction =  self.dbContext.executeAndFetchOne(sql_statement, queryParameters)
    userRecord = get_transaction
    return userRecord
  
  def GetLastFromPoolId(self, Tx_Id):
    queryParameters = (Tx_Id,)
    sql_statement = '''SELECT Sender_username, Receiver_username, Tx_value, Tx_fee, sig, date, time FROM TransactionPool WHERE Tx_No = ?'''
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

  def UpdateUserBalance(self, values_to_update):
    status = values_to_update[0]
    amount = values_to_update[1]
    username = values_to_update[2]
    if status == 'amount_sent':
      Values = (amount, username)
      sql_statement = '''UPDATE UsersBalance SET amount_sent=? WHERE username=?'''
      try: 
        self.dbContext.executeAndCommit(sql_statement, Values)
        return True
      except Exception as e:
        print(e)
        return False
    if status == 'amount_received':
      Values = (amount, username)
      sql_statement = '''UPDATE UsersBalance SET amount_received=? WHERE username=?'''
      try: 
        self.dbContext.executeAndCommit(sql_statement, Values)
        return True
      except Exception as e:
        print(e)
        return False
    if status == 'fee_paid':
      Values = (amount, username)
      sql_statement = '''UPDATE UsersBalance SET fee_paid=? WHERE username=?'''
      try: 
        self.dbContext.executeAndCommit(sql_statement, Values)
        return True
      except Exception as e:
        print(e)
        return False
    if status == 'fee_gained':
      Values = (amount, username)
      sql_statement = '''UPDATE UsersBalance SET fee_gained=? WHERE username=?'''
      try: 
        self.dbContext.executeAndCommit(sql_statement, Values)
        return True
      except Exception as e:
        print(e)
        return False
    if status == 'mined_reward':
      Values = (amount, username)
      sql_statement = '''UPDATE UsersBalance SET mined_reward=? WHERE username=?'''
      try: 
        self.dbContext.executeAndCommit(sql_statement, Values)
        return True
      except Exception as e:
        print(e)
        return False

  def DeleteTransaction(self, transaction_number):
    try: 
      Tx_No = transaction_number 
      Values = (Tx_No,)
      sql_statement = '''DELETE FROM TransactionPool WHERE Tx_No =?'''
      self.dbContext.executeAndCommit(sql_statement, Values)
      
      sql_statement = '''DELETE FROM HashForSecurity WHERE Tx_No =?'''
      self.dbContext.executeAndCommit(sql_statement, Values)
      return True
    except Exception as e:
      print(e)
      return False
      
  def DeleteConfirmedTransactions(self, transaction_number):
    try: 
      Tx_No = transaction_number 
      Values = (Tx_No,)
      sql_statement = '''DELETE FROM HashForSecurity WHERE Tx_No =?'''
      self.dbContext.executeAndCommit(sql_statement, Values)
    
      sql_statement = '''DELETE FROM TransactionPool WHERE Tx_No =?'''
      self.dbContext.executeAndCommit(sql_statement, Values)
      return True
    except Exception as e:
      print(e)
      return False 

  def UpdateConfirmationStatus(self, confirmation):
    username = confirmation[1]
    confirmation_status = confirmation[0]
    Values = (confirmation_status, username)
    sql_statement = '''UPDATE users SET confirmation_status=? WHERE username=?'''
    try: 
      self.dbContext.executeAndCommit(sql_statement, Values)
      return True
    except Exception as e:
      print(e)
      return False
  
  def CreateHashForSecurity(self, hashed_tx):
    try:
      Values = (hashed_tx[0], hashed_tx[1])
      sql_statement = '''INSERT INTO HashForSecurity (hashed_transactions, transaction_status) VALUES (?, ?)'''
      self.dbContext.executeAndCommit(sql_statement, Values)
      return True
    except Exception as e:
      print(e)
      return False

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

  def UpdateHashForSecurity(self, txNumber):
    Tx_No = txNumber[1]
    transaction_status = txNumber[0]
    Values = (transaction_status, Tx_No)
    sql_statement = '''UPDATE HashForSecurity SET transaction_status=? WHERE Tx_No=?'''
    try: 
      self.dbContext.executeAndCommit(sql_statement, Values)
      return True
    except Exception as e:
      print(e)
      return False

  def CreateHashForBlock(self, hashed_blocks):
    try:  
      Values = (hashed_blocks,)
      sql_statement = '''INSERT INTO HashForBlock (hashed_blocks) VALUES (?)''' 
      self.dbContext.executeAndCommit(sql_statement, Values)
      return True
    except Exception as e:
      print(e)
      return False

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
    try:
      Values = (hashed_blocks,)
      sql_statement = '''INSERT INTO HashForChain (hashed_chain) VALUES (?)'''
      self.dbContext.executeAndCommit(sql_statement, Values)
      return True
    except Exception as e:
      print(e)
      return False

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
    try: 
      Values = (Id_No,)
      sql_statement = '''DELETE FROM TempBlock WHERE Id_No=?'''
      self.dbContext.executeAndCommit(sql_statement, Values)
    
      Value = (Id_No,)
      sql_statement = '''DELETE FROM HashForBlock WHERE Tx_No=?'''
      self.dbContext.executeAndCommit(sql_statement, Value)
      return True
    except Exception as e:
      print(e)
      return False

  def DeleteUserName(self, user_Id):
    try: 
      Values = (user_Id,)
      sql_statement = '''DELETE FROM users WHERE user_Id =?'''
      self.dbContext.executeAndCommit(sql_statement, Values)
      return True
    except Exception as e:
      print(e)
      return False
  
  def DeleteUsersBalance(self, balance_Id):
    try: 
      Values = (balance_Id,)
      sql_statement = '''DELETE FROM UsersBalance WHERE balance_Id =?'''
      self.dbContext.executeAndCommit(sql_statement, Values)
      return True
    except Exception as e:
      print(e)
      return False
  
  def DeleteKeys(self, key_Id):
    try: 
      Values = (key_Id,)
      sql_statement = '''DELETE FROM SaveKeys WHERE key_Id =?'''
      self.dbContext.executeAndCommit(sql_statement, Values)
      return True
    except Exception as e:
      print(e)
      return False
    