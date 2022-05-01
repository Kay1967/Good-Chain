from Domain.UserLogAggregate import Log
from Helper.EncryptionHelper import EncryptionHelper


class PermissionRecord:

    def __init__(self, encryptedPermissionTuple):
        logTuple = EncryptionHelper.GetDecryptedTuple(encryptedPermissionTuple)
        self.permissionEnum = logTuple[0] 
        self.advisor = logTuple[1]
        self.sysadmin = logTuple[2]
        self.superadmin = logTuple[3]
