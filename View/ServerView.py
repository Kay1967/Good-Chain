from Service.LoginService import *
from Repository.UserRepository import *
from Service.SignUpService import *
from Service.BlockService import *
from threading import Thread
from Service.ServerService import *

class ServerView:

  def __init__(self, loginService, signUpService, blockService, serverService, clientService):          
    self.loginService = loginService
    self.signUpService = signUpService
    self.blockService = blockService
    self.serverService = serverService
    self.clientService = clientService
    
  def GetMenu(self):
    recTransaction = Thread(target=self.serverService.recTransactions)
    recUser = Thread(target=self.serverService.recUser)
    recBlock = Thread(target=self.serverService.recBlockchain)
    recVerification = Thread(target=self.serverService.recBlockVerification)
    recTransaction.start()
    print("server is on...")
    recUser.start()
    recBlock.start()
    recVerification.start()

    #return