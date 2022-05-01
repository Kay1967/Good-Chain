# from datetime import datetime as dt
# from Domain.User import User
# #from Helper.EncryptionHelper import EncryptionHelper
# #from Record.LogRecord import LogRecord

# class LoggingRepository:
#     def __init__ (self, db, tenant = None):
#         self.dbContext = db

#         self.tenantIsDefined = isinstance(tenant, User)
#         if self.tenantIsDefined:
#             self.tenant = tenant

#     def GetAllLogs(self):
#         sql_statement = f"SELECT * FROM logging ORDER BY date DESC, time"
#         try: logRecords = self.dbContext.executeAndFetchAll(sql_statement, None)
#         except Exception as error: self.CreateLog(self.tenant.username, f"{self.GetAllLogs.__name__}", f"DatabaseException {error}", 1); return

#         allLogs = []
#         for logRecord in logRecords:
#             #logRecord = LogRecord(logRecord)
#             allLogs.append(logRecord.ToLogDomain())

#         return allLogs 

#     def CreateLog(self, username, description_of_activity, additional_info, suspicious):
#         today =  dt.now()
#         date = today.strftime("%d-%m-%Y")
#         time = today.strftime("%H:%M:%S")
        
#         #encryptedValues = EncryptionHelper.GetEncryptedTuple((username, date, time, description_of_activity, additional_info, suspicious))
#         sql_statement = '''INSERT INTO logging (username, date, time, description_of_activity, additional_info, supicious) VALUES (?,?,?,?,?,?)'''
#         self.dbContext.executeAndCommit(sql_statement)