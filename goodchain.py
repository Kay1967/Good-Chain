from Service.LoginService import LoginService
from startup import ServiceCollection
from Component.UserInterface import UserInterfaceComponent
from DbContext.database import * 
from View.MainView import MainView
from View.LoginView import LoginView
from View.ServerView import *
from Domain.User import *
import sqlite3
from termcolor import colored
import time


Heading = '''
Public Menu
----------------------------------                           
| Menu for sign up in Goodchain  |
----------------------------------
'''
def CreateMainMenuHeader(tenantName, tenantTypeName):
    nameAndSpaces =  tenantName + "" * (19 - len(tenantName))
    userTypeAndSpaces = tenantTypeName + "" * (19 - len(tenantTypeName))
    
    return '''
----------------------------------
| Username : {0}             |
| welcome to gooChain node       |
----------------------------------
'''.format(nameAndSpaces, userTypeAndSpaces)


# GLobal Variables
# --------------------------------------------------------------------
max_input_try = 3
chain_db_name = 'goodchain.db'
users_tb_name = 'users'
#---------------------------------------------------------------------
dbContext = db(chain_db_name, users_tb_name)
serviceCollection = ServiceCollection(dbContext)
serviceCollection.ConfigureLoginDependencies()
#-----------------------------------------------------------------------

# View calls Service, and Service calls Repository and Repository reflects always the data layer (database)

if __name__ == "__main__":
    loginService = LoginService(serviceCollection.UserRepository, serviceCollection.UserService, serviceCollection.ServerService, serviceCollection.ClientService)
    
    loginService.GenesisBlock()
    loginService.checks()
    loginService.serverOn()
    
    #serverView = ServerView(serviceCollection.LoginService, serviceCollection.SignUpService, serviceCollection.BlockService, serviceCollection.ServerService, serviceCollection.ClientService)
    loginView = LoginView(serviceCollection.LoginService, serviceCollection.SignUpService, serviceCollection.BlockService, serviceCollection.ServerService) #serviceCollection.User
    
    loginInterface = UserInterfaceComponent(loginView, True, Heading)
    #serverInterface = UserInterfaceComponent(serverView, True, None)
    loginInterface.run()
    #serverInterface.run()
    #loginService.serverView()
    if serviceCollection.LoginService.loggedin:
        serviceCollection.ConfigureServicesOnLogin()
        mainView = MainView(serviceCollection.LoginService.tenant, 
                            serviceCollection.LoginService,
                            serviceCollection.UserService,
                            serviceCollection.SignUpService,
                            serviceCollection.BlockService,
                            serviceCollection.UserRepository,
                            serviceCollection.ServerService,
                            serviceCollection.ClientService,
                            serviceCollection.LoginView) 
                    
        mainHeading = CreateMainMenuHeader(serviceCollection.LoginService.tenant[1], type(serviceCollection.LoginService.tenant).__name__)
     
        mainInterface = UserInterfaceComponent(mainView, False, mainHeading)
        
        mainInterface.run()
        
        dbContext.conn.close()
        
        
    