import sqlite3
#from Helper.EncryptionHelper import EncryptionHelper
from datetime import datetime as dt
from datetime import timedelta

# Database
# --------------------------------------------------------------------
class db:
    def __init__(self, db_name, users_table_name):
        self.db_name = db_name
        #self.client_table_name = client_table_name
        self.users_table_name = users_table_name
        
        self.loggedin = 0
        self.loggedin_user = None
       # self.admin_is_loggedin = 0
        
        self.reset()

    def reset(self):
        self.conn = sqlite3.connect(self.db_name) 
        self.cur = self.conn.cursor()

        # create user table if it does not exist
        tb_create = "CREATE TABLE users (username TEXT, password BLOB, initialbalance INTEGER)"
        try:
            self.cur.execute(tb_create)
            # add sample records to the db manually
            lastLogin = dt.now() - timedelta(days=15)
            date = lastLogin.strftime("%d-%m-%Y")
            self.cur.execute('''INSERT INTO users (username, password, initialbalance) VALUES (?, ?, ?)''')
            #self.cur.execute('''INSERT INTO users (username, password, fullname, admin, last_login) VALUES (?, ?, ?, ?, ?)''', EncryptionHelper.GetEncryptedTuple(('ivy_russel', 'ivy@R123' , 'Ivy Russel', 0, date)))
            #self.cur.execute('''INSERT INTO users (username, password, fullname, admin, last_login) VALUES (?, ?, ?, ?, ?)''', EncryptionHelper.GetEncryptedTuple(('superadmin', 'Admin!23' , 'Super Admin', 1, date)))
            self.conn.commit()
        except: 
            None
      
        #create keys table
        tb_create = "CREATE TABLE SaveKeys (username TEXT, password BLOB, public_key BLOB, private_key BLOB)"
        try:
            self.cur.execute(tb_create)
            # add sample records to the db manually
            lastLogin = dt.now() - timedelta(days=15)
            date = lastLogin.strftime("%d-%m-%Y")
            self.cur.execute('''INSERT INTO SaveKeys (username, password, public_key, private_key) VALUES (?, ?, ?, ?)''')
            #self.cur.execute('''INSERT INTO users (username, password, fullname, admin, last_login) VALUES (?, ?, ?, ?, ?)''', EncryptionHelper.GetEncryptedTuple(('ivy_russel', 'ivy@R123' , 'Ivy Russel', 0, date)))
            #self.cur.execute('''INSERT INTO users (username, password, fullname, admin, last_login) VALUES (?, ?, ?, ?, ?)''', EncryptionHelper.GetEncryptedTuple(('superadmin', 'Admin!23' , 'Super Admin', 1, date)))
            self.conn.commit()
        except: 
            None

        # create transaction table    
        tb_create = "CREATE TABLE TransactionPool (Tx_No INTEGER PRIMARY KEY AUTOINCREMENT, Sender_username TEXT, Receiver_username TEXT, Tx_value REAL, Tx_fee REAL, status TEXT)"
        try:
            self.cur.execute(tb_create)
            # add sample records to the db manually
            lastLogin = dt.now() - timedelta(days=15)
            date = lastLogin.strftime("%d-%m-%Y")
            self.cur.execute('''INSERT INTO TransactionPool (Sender_username, Receiver_username, Tx_value, Tx_fee, status) VALUES (?, ?, ?, ?, ?)''')
            #self.cur.execute('''INSERT INTO users (username, password, fullname, admin, last_login) VALUES (?, ?, ?, ?, ?)''', EncryptionHelper.GetEncryptedTuple(('ivy_russel', 'ivy@R123' , 'Ivy Russel', 0, date)))
            #self.cur.execute('''INSERT INTO users (username, password, fullname, admin, last_login) VALUES (?, ?, ?, ?, ?)''', EncryptionHelper.GetEncryptedTuple(('superadmin', 'Admin!23' , 'Super Admin', 1, date)))
            self.conn.commit()
        except: 
            None
         # create blockchain   
        tb_create = "CREATE TABLE BlockChain (Blc_No INTEGER PRIMARY KEY AUTOINCREMENT, nonce TEXT, previous_hash TEXT, data TEXT, current_hash TEXT, date TEXT, time TEXT)"
        try:
            self.cur.execute(tb_create)
            # add sample records to the db manually
            today =  dt.now()
            date = today.strftime("%d-%m-%Y")
            time = today.strftime("%H:%M:%S")
            self.cur.execute('''INSERT INTO BlockChain (nonce, previous_hash, data, current_hash, date, time) VALUES (?, ?, ?, ?, ?, ?)''')
            #self.cur.execute('''INSERT INTO users (username, password, fullname, admin, last_login) VALUES (?, ?, ?, ?, ?)''', EncryptionHelper.GetEncryptedTuple(('ivy_russel', 'ivy@R123' , 'Ivy Russel', 0, date)))
            #self.cur.execute('''INSERT INTO users (username, password, fullname, admin, last_login) VALUES (?, ?, ?, ?, ?)''', EncryptionHelper.GetEncryptedTuple(('superadmin', 'Admin!23' , 'Super Admin', 1, date)))
            self.conn.commit()
        except: 
            None
        #create wallet
        tb_create = "CREATE TABLE UsersBalance (username, initialbalance, amount_sent, amount_received, fee_paid, fee_gained)"
        try:
            self.cur.execute(tb_create)
            # add sample records to the db manually
            lastLogin = dt.now() - timedelta(days=15)
            date = lastLogin.strftime("%d-%m-%Y")
            self.cur.execute('''INSERT INTO UsersBalance (username, initialbalance, amount_sent, amount_received, fee_paid, fee_gained) VALUES (?, ?, ?, ?, ?, ?)''')
            #self.cur.execute('''INSERT INTO users (username, password, fullname, admin, last_login) VALUES (?, ?, ?, ?, ?)''', EncryptionHelper.GetEncryptedTuple(('ivy_russel', 'ivy@R123' , 'Ivy Russel', 0, date)))
            #self.cur.execute('''INSERT INTO users (username, password, fullname, admin, last_login) VALUES (?, ?, ?, ?, ?)''', EncryptionHelper.GetEncryptedTuple(('superadmin', 'Admin!23' , 'Super Admin', 1, date)))
            self.conn.commit()
        except: 
            None
        # this is used for validation of the pool
        tb_create = "CREATE TABLE HashForSecurity (Tx_No INTEGER PRIMARY KEY AUTOINCREMENT, hashed_transactions TEXT)"
        try:
            self.cur.execute(tb_create)
           
            self.cur.execute('''INSERT INTO HashForSecurity (hashed_transactions) VALUES (?)''')
            #self.cur.execute('''INSERT INTO users (username, password, fullname, admin, last_login) VALUES (?, ?, ?, ?, ?)''', EncryptionHelper.GetEncryptedTuple(('ivy_russel', 'ivy@R123' , 'Ivy Russel', 0, date)))
            #self.cur.execute('''INSERT INTO users (username, password, fullname, admin, last_login) VALUES (?, ?, ?, ?, ?)''', EncryptionHelper.GetEncryptedTuple(('superadmin', 'Admin!23' , 'Super Admin', 1, date)))
            self.conn.commit()
        except: 
            None
    
    def executeAndCommit(self, sql_statement, queryParameters):
        try:
            if queryParameters is not None:
                self.cur.execute(sql_statement, queryParameters)
            else:
                self.cur.execute(sql_statement)
            self.conn.commit()
        except Exception as exception: 
            print("something went wrong")
            raise Exception(exception, False)   
        pass

    def executeAndFetchAll(self, sql_statement, queryParameters):
        try:
            if queryParameters is not None:
                self.cur.execute(sql_statement, queryParameters)
            else:
                self.cur.execute(sql_statement)
            records = self.cur.fetchall()
            return records
        except Exception as exception: 
            print("something went wrong")
            raise Exception(exception, False)     

    def executeAndFetchOne(self, sql_statement, queryParameters):
        try:
            if queryParameters is not None:
                self.cur.execute(sql_statement, queryParameters)
            else:
                self.cur.execute(sql_statement)
            record = self.cur.fetchone()
            return record
        except Exception as exception: 
            print("something went wrong")
            raise Exception(exception, False)      

    def not_implemented(self, func):
        print(func.__name__ + ' method is Not implemented')
    
def escape_sql_meta(sql_query):
    pass



