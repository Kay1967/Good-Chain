#from Enum.Permission import Permission
import os
from Service.LoginService import *
from Service.SignUpService import *
from Service.BlockService import *
from Service.ServerService import *
from View.LoginView import LoginView
from View.ServerView import *
from Repository.UserRepository import *
from Domain.User import *
from threading import Thread


class MainView:
  def __init__(self, tenant, loginService, userService, signUpService, blockService, userRepository, serverService, clientService, loginView):
    self.loginService = loginService
    self.userService = userService
    self.signUpService = signUpService
    self.blockService = blockService
    self.tenant = tenant
    self.userRepository = userRepository
    self.serverService = serverService
    self.clientService = clientService
    self.loginView = loginView

  def GetMenu(self):
    print(f"================================")
    check_block_valid = self.userRepository.GetAllFromTempBlock()
    recheck = []
    for check in check_block_valid:
      rehashed = User.hash_transaction(self, check)
      recheck.append(rehashed)  
    b = False
    hashed_before = self.userRepository.GetAllHashForBlock()
    for i in range(len(hashed_before)): 
      if hashed_before[i][1] == recheck[i]:
        b = True
      else:
        b = False
        os.system('color')
        print(f"Block number {hashed_before[i][0]} is", colored('tempered!', 'yellow'))
        time.sleep(0.2)
    print(f"================================")
    confirming_users = self.userRepository.GetAllUsers()
    list_confirmed = []
    exist_block = self.userRepository.GetAllFromTempBlock()
    if len(exist_block) > 0:
      for i in range(len(confirming_users)):
        list_confirmed.append(confirming_users[i][3])
      username=self.tenant
      if sum(list_confirmed) == 0: 
        print(f"{username[0]}, blocks are waiting for confirmation, if you have not confirmed one.")
      if sum(list_confirmed) == 1:
        print(f"{username[0]}, blocks are waiting for confirmation, if you have not confirmed one.")
      if sum(list_confirmed) == 2:
        print(f"{username[0]}, blocks are waiting for confirmation, if you have not confirmed one.")
    else:
      print("There is no block mined yet to be confirmed.")
    
      #recTransaction = Thread(target=self.serverService.recTransactions)
      # recUser = Thread(target=self.serverService.recUser)
      # recBlock = Thread(target=self.serverService.recBlockchain)
      # recVerification = Thread(target=self.serverService.recBlockVerification)
      #recTransaction.start()
      #print("server is on...")
      # recUser.start()
      # recBlock.start()
      # recVerification.start()
      #return 

    view = []
    
    view.append([len(view) + 1, 'Transfer Coins', self.userService.TransferCoins])
    view.append([len(view) + 1, 'Check the Balance', self.userService.CheckBalance])
    view.append([len(view)+1, 'Explore the Chain', self.userService.ExploreChain])
    view.append([len(view)+1, 'Check the Pool', self.userService.CheckPool])
    view.append([len(view) + 1, 'Cancel a Transaction', self.userService.CancelTransaction])
    view.append([len(view) + 1, 'Mine a Block', self.userService.MineBlock])
    view.append([len(view) + 1, 'Confirm a Block', self.userService.ConfirmBlock])
    view.append([0, 'Log out', self.loginView.GetMenu]) 

    return view

    

    