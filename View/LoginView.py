from Service.LoginService import *
from Repository.UserRepository import *
from Service.SignUpService import *
from Service.BlockService import *

class LoginView:

  def __init__(self, loginService, signUpService, blockService):          
    self.loginService = loginService
    self.signUpService = signUpService
    self.blockService = blockService
    
  def GetMenu(self):
    return [[1, 'login', self.loginService.login ], 
            [2, 'Explore the blockchain', self.blockService.Block], 
            [3, 'Sign up', self.signUpService.SignUp],
            [4, 'Exit', self.loginService.close]]

    
    
