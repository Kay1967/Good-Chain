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

  def GetMenuDb(self):
    return    [[1, 'show all clients', self.loginService.show_all_clients], [2, 'show all users', self.loginService.show_all_users], \
            [3, 'add new client', self.loginService.add_new_client], [4, 'add new user', self.loginService.add_new_user], \
            [5, 'make a user "admin"', self.loginService.make_a_user_admin], \
            [6, 'delete a client', self.loginService.delete_client], [7, 'delete a user', self.loginService.delete_user], \
            [8, 'change password', self.loginService.change_password], [0, 'logout', self.loginService.logout]]
    
    # [ [1, 'show all clients', self.userRepository.show_all_clients], [2, 'show all users', self.userRepository.show_all_users], \
    #         [3, 'add new client', self.userRepository.add_new_client], [4, 'add new user', self.userRepository.add_new_user], \
    #         [5, 'make a user "admin"', self.userRepository.make_a_user_admin], \
    #         [6, 'delete a client', self.userRepository.delete_client], [7, 'delete a user', self.userRepository.delete_user], \
    #         [8, 'change password', self.userRepository.change_password], [0, 'logout', self.userRepository.logout]] 
    
    
