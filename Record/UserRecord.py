#from Domain.SuperAdmin import SuperAdmin
#from Helper.EncryptionHelper import EncryptionHelper
#from Domain.Advisor import Advisor
#from Domain.SysAdmin import SysAdmin

class UserRecord:
    def __init__(self, username, password, initial_balance):
       # userTuple = EncryptionHelper.GetDecryptedTuple(encryptedUserTuple)

        self.username = username
        self.password= password
        
        self.initial_balance = initial_balance

    # def ToUserDomain(self):
    #     isAdmin = self.admin == "1"
    #     isSuperAdmin = self.username == "superadmin" 
    #     if isSuperAdmin:
    #         return SuperAdmin(self.username, self.password, self.fullname, isAdmin, self.last_login)
    #     if isAdmin:
    #         return SysAdmin(self.username, self.password, self.fullname, isAdmin, self.last_login)
    #     return Advisor(self.username, self.password, self.fullname, isAdmin, self.last_login)
    