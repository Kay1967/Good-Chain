from Domain.User import User

from Repository.UserRepository import UserRepository

from Service.SignUpService import *
from Service.UserService import *
from Service.BlockService import *

from Service.LoginService import *

class ServiceCollection:
    def __init__(self, dbContext):
        self.dbContext = dbContext

    # In between solution for loading services and repositories to define tenant
    def ConfigureLoginDependencies(self):
        
        
        self.UserRepository = UserRepository(self.dbContext)
        self.UserService = UserService(self.dbContext.loggedin, self.UserRepository)
        self.LoginService = LoginService(self.UserRepository, self.UserService)
        
        self.SignUpService = SignUpService(self.UserRepository)
        self.BlockService = BlocklService(self.UserRepository)
        

    # Called when user is logged in, to reload other services when tenant (user) is defined
    def ConfigureServicesOnLogin(self):
        if not self.LoginService.loggedin:
            return
        self.AddRepositories()
        self.AddServices()

    def AddRepositories(self):
    
        self.UserRepository = UserRepository(self.dbContext, self.LoginService.tenant)
    
        return

    def AddServices(self):
          self.UserService = UserService(self.LoginService.tenant, self.UserRepository)
          self.SignUpService = SignUpService(self.UserRepository)
          self.BlockService = BlocklService(self.UserRepository)
          
          return