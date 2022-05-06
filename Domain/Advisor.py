from Domain.User import User


class Advisor(User):
  def __init__(self, username, password, initialbalance):
    
    super().__init__(username, password, initialbalance)
  