from Domain.User import User

from Repository.UserRepository import UserRepository

from Service.SignUpService import *
from Service.UserService import *
from Service.BlockService import *

from Service.LoginService import *
from Service.ServerService import *
from Service.ClientService import *
from View.LoginView import LoginView

class ServiceCollection:
    def __init__(self, dbContext):
        self.dbContext = dbContext
        

    # In between solution for loading services and repositories to define tenant
    def ConfigureLoginDependencies(self):
        
        
        self.UserRepository = UserRepository(self.dbContext)
        self.UserService = UserService(self.dbContext.loggedin, self.UserRepository)
        self.SignUpService = SignUpService(self.UserRepository)
        self.ServerService = ServerService(self.UserService, self.SignUpService, self.UserRepository)
        self.ClientService = ClientService()
        self.LoginService = LoginService(self.UserRepository, self.UserService, self.ServerService, self.ClientService)
        self.BlockService = BlocklService(self.UserRepository)
        #self.User = User(self.dbContext.loggedin, self.UserRepository, self.UserService, self.SignUpService, self.LoginService)
        self.LoginView = LoginView(self.LoginService, self.SignUpService, self.BlockService, self.ServerService)
        
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
          self.ServerService = ServerService(self.UserService, self.SignUpService, self.UserRepository)
          self.User = User(self.LoginService.tenant, self.UserRepository, self.UserService, self.SignUpService, self.LoginService)
        
          
          return
    
    
    