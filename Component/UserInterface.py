from math import trunc
import time
import os
import sys
#from startup import ServiceCollection

from View.LoginView import *
from sqlite3.dbapi2 import OperationalError
from Service.LoginService import *
from Service.SignUpService import *
from Service.BlockService import *
from Service.ServerService import *
from threading import Thread


from termcolor import colored
import sqlite3

class UserInterfaceComponent:

  default_menu = [[1, 'option 1', None], [2, 'option 2', None], [3, 'option 2', None], [0, 'Exit', None]]

  def __init__(self, view, closeOnAction, menuheading='Not logged in'):
      #self.view = view
      if view is None:
          menueitems = self.default_menu
      else:
          menueitems = view.GetMenu()

      self.menuheading = menuheading
      self.menuitems = menueitems
      self.menuoptions = [option[0] for option in self.menuitems]
      self.menufunctions = [option[2] for option in self.menuitems]
      
      self.closeOnAction = closeOnAction
      print(self.menuheading)
      self.menu_display()

  def menu_display(self):
      #print('\n_________________________________\n') 
      for option in self.menuitems:
          print('[' + str(option[0]) + ']' + ' ' + option[1])
          time.sleep(0.1)
          #print('\n_________________________________\n')   
              
  def default_no_menuitems(self):
      print('Menu items are not defined')

  def run(self):
      
      try:
          option = int(input('Choose a number from the menu: '))
          print()
      except:
          option = -1
          print()

      while option != self.menuoptions[-1]:
          if option in self.menuoptions:
              if self.menuitems == self.default_menu:
                  self.default_no_menuitems()
              else:
                  try:
                      func_return = self.menuitems[self.menuoptions.index(option)][2]()
                      #print(func_return)
                      if self.closeOnAction:
                          return
                      if func_return == 0:
                          option = 0
                          continue
                  except Exception as e:
                      print(e)
          else:
              print('invalid option')

          print()
          self.menu_display()
          try:
              option = int(input('Choose a number from the menu: '))
              print()
                
          except:
              option = -1
              print()
      
        
        
        