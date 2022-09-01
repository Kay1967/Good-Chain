from Service.LoginService import *
from Repository.UserRepository import *
from Service.SignUpService import *
from Service.BlockService import *
from threading import Thread
from Service.ServerService import *
import Domain
from Domain.User import *

class LoginView:

  def __init__(self, loginService, signUpService, blockService, serverService): #user         
    self.loginService = loginService
    self.signUpService = signUpService
    self.blockService = blockService
    self.serverService = serverService
    #self.user = user
    
    
  def GetMenu(self):
    #recTransaction = Thread(target=self.user.recTransactions)
    # recUser = Thread(target=self.serverService.recUser)
    # recBlock = Thread(target=self.serverService.recBlockchain)
    # recVerification = Thread(target=self.serverService.recBlockVerification)
    #recTransaction.start()
    #print("server is on...")
    # recUser.start()
    # recBlock.start()
    # recVerification.start()
    return [[1, 'login', self.loginService.login ], 
            [2, 'Explore the blockchain', self.blockService.Block], 
            [3, 'Sign up', self.signUpService.SignUp],
            [4, 'Exit', self.loginService.close]]
            

    
    
