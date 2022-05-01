from sqlite3 import SQLITE_TRANSACTION
from flask import g
from datetime import datetime as dt
import Domain
from Domain.User import User
from Record.UserRecord import UserRecord
import hashlib
from hashlib import sha256
import Transactions
from Transactions.Asym import *
#from Helper.EncryptionHelper import EncryptionHelper
hash_func = lambda x: sha256(x.encode('utf-8')).hexdigest()
class UserRepository:

  def __init__ (self, db, tenant = None):
    self.dbContext = db
    #self.loggingRepository = loggingRepository

    tenantIsDefined = isinstance(tenant, User)
    if tenantIsDefined:
      self.tenant = tenant

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
      # if len(userRecords)==0:
      #   print('There is no component named %s'%userRecord)
      # else:
      #   print('Component %s found with rowids %s'%(userRecord,','.join(map(str, next(zip(*userRecords))))))
    return allUsers 

  # Generic for updating password for all users
  def GetKeys(self, username):
    queryParameters = (username,)
    sql_statement = '''SELECT * from SaveKeys WHERE LOWER(username)=LOWER(?)'''
    get_keys =  self.dbContext.executeAndFetchOne(sql_statement, queryParameters)
    userRecord = get_keys
    return userRecord
  
  def CreateUser(self, username, password, initialbalance):
    hashed_password = hash_func(str(password))
    Values = (username, hashed_password, initialbalance)
    sql_statement = '''INSERT INTO users (username, password, initialbalance) VALUES (?,?,?)'''
    self.dbContext.executeAndCommit(sql_statement, Values)
    #except Exception as error: self.loggingRepository.CreateLog(self.tenant.username, f"{self.CreateUser.__name__}", f"DatabaseException {error}", 1)
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
  
  
  def CreateUsersBalance(self, username, initialbalance, amount_sent, amount_received, fee_paid, fee_gained):
    # today =  dt.now()
    # date = today.strftime("%d-%m-%Y")
    # time = today.strftime("%H:%M:%S")
    
    Values = (username, initialbalance, amount_sent, amount_received, fee_paid, fee_gained)
    sql_statement = '''INSERT INTO UsersBalance (username, initialbalance, amount_sent, amount_received, fee_paid, fee_gained) VALUES (?,?,?,?,?,?)'''
    self.dbContext.executeAndCommit(sql_statement, Values)

  def SaveKeys(self, username, password, publickey, privatekey):
    #hashed_password = hash_func(str(password))
   # hashed_publicKey = hash_func(str(publickey))
    #hashed_privateKey = hash_func(str(privatekey))
    Values = (username, password, publickey, privatekey)
    sql_statement = '''INSERT INTO SaveKeys (username, password, public_key, private_key) VALUES (?,?,?,?)'''
    self.dbContext.executeAndCommit(sql_statement, Values)
  
  def CreateTransactionPool(self, Sender_username, Receiver_username, Tx_value, Tx_fee):
    # today =  dt.now()
    # date = today.strftime("%d-%m-%Y")
    # time = today.strftime("%H:%M:%S")
    status = "pending"

    Values = (Sender_username, Receiver_username, Tx_value, Tx_fee, status)
    sql_statement = '''INSERT INTO TransactionPool (Sender_username, Receiver_username, Tx_value, Tx_fee, status) VALUES (?,?,?,?,?)'''
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
      # if self.tenantIsDefined:
      #     self.CreateLog(self.tenant.username, f"{self.GetAllLogs.__name__}", f"DatabaseException {error}", 1); return
      #else:
      raise ValueError ("Cannot get balance of the user!")

    if userEncrypted is None and login is False:
      raise ValueError("User not found", True)
    if userEncrypted is None and login is True:
      raise ValueError("Login failed", True)

    userRecord = userEncrypted
    return userRecord

  def DeleteTransactie(self, username):
    #encryptedValues = EncryptionHelper.GetEncryptedTuple((username,))
    sql_statement = '''DELETE FROM users WHERE username =?'''
    try: self.dbContext.executeAndCommit(sql_statement)
    except:
       raise ValueError ("Cannot delete the row you required!")
  def UpdateTransactionStatus(self, username):
    status = "validated"
    Values = (status, username)
    sql_statement = '''UPDATE TransactionPool SET status=? WHERE sender_username=?'''
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