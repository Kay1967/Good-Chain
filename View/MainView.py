#from Enum.Permission import Permission

from Service.LoginService import LoginService
from Service.SignUpService import *
from Service.BlockService import *
from View.LoginView import LoginView


class MainView:
  def __init__(self, tenant, loginService, userService, signUpService, blockService):
    self.loginService = loginService
    self.userService = userService
    self.signUpService = signUpService
    self.blockService = blockService
    #self.clientService = clientService
    #self.sysAdminService = sysAdminService
    #self.logService = logService
    #self.backupService = backupService
    self.tenant = tenant

  def GetMenu(self):
    view = []
    #for permission in Permission:
      #if Permission.ViewClient == permission and self.tenant.HasPermission(permission):
    #view.append([len(view)+1, 'View all clients', self.clientService.GetAllClients])
    #view.append([len(view)+1, 'Search client', self.clientService.ViewAndGetClientInfo])
      #if Permission.CreateClient == permission and self.tenant.HasPermission(permission):
    #view.append([len(view)+1, 'Sign up', self.SignUpService.SignUp])
      #if Permission.UpdateClientInfo == permission and self.tenant.HasPermission(permission):
    #view.append([len(view)+1, 'Update client', self.clientService.UpdateClientInfo])
      #if Permission.ManageClient == permission and self.tenant.HasPermission(permission):
    #view.append([len(view)+1, 'Delete client', self.clientService.DeleteClientRecord])
      
      #if Permission.ViewAllUsers == permission and self.tenant.HasPermission(permission):
    #view.append([len(view)+1, 'View all users', self.userService.GetAllUsers])
      
      #if Permission.ManageAdvisor == permission and self.tenant.HasPermission(permission):
  
    view.append([len(view) + 1, 'Transfer Coins', self.userService.TransferCoins])
    view.append([len(view) + 1, 'Check the Balance', self.userService.CheckBalance])
    view.append([len(view)+1, 'Explore the Chain', self.userService.ExploreChain])
      #if Permission.UpdateAdvisorPassword == permission and self.tenant.HasPermission(permission):
    view.append([len(view)+1, 'Check the Pool', self.userService.CheckPool])

      #if Permission.ManageSysAdmin == permission and self.tenant.HasPermission(permission):
    view.append([len(view) + 1, 'Cancel a Transaction', self.userService.CancelTransaction])
    view.append([len(view) + 1, 'Mine a Block', self.userService.MineBlock])
    #view.append([len(view)+1, 'Delete admin', self.sysAdminService.DeleteSysAdmin])
      #if Permission.UpdateSysAdminPassword == permission and self.tenant.HasPermission(permission):
    #view.append([len(view)+1, 'Update password for admin', self.sysAdminService.UpdatePasswordForSysAdmin])

      #if Permission.ManageBackup == permission and self.tenant.HasPermission(permission):
    #view.append([len(view)+1, 'Create backup', self.backupService.CreateBackup])

      #if Permission.ManageLog ==  permission and self.tenant.HasPermission(permission):
    #view.append([len(view)+1, 'View all Logs', self.logService.ViewAllLogs])
    # userLogAggregate = self.logService.GetUserLogAggregate()
    # if userLogAggregate.countUnseenSuspiciousActivity > 0:
    #print(f"\n!!!! {userLogAggregate.countUnseenSuspiciousActivity} suspicous activities logged after your last login ({userLogAggregate.userLastLogin})\n") 


    view.append([0, 'Log out', self.loginService.close]) #self.loginService.close

    return view