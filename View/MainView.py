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
    self.tenant = tenant

  def GetMenu(self):
    view = []
    
    view.append([len(view) + 1, 'Transfer Coins', self.userService.TransferCoins])
    view.append([len(view) + 1, 'Check the Balance', self.userService.CheckBalance])
    view.append([len(view)+1, 'Explore the Chain', self.userService.ExploreChain])
    view.append([len(view)+1, 'Check the Pool', self.userService.CheckPool])
    view.append([len(view) + 1, 'Cancel a Transaction', self.userService.CancelTransaction])
    view.append([len(view) + 1, 'Mine a Block', self.userService.MineBlock])
    view.append([len(view) + 1, 'Confirm a Block', self.userService.ConfirmBlock])
    view.append([0, 'Log out', self.loginService.close]) 

    return view