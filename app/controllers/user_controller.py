from app.models.user_model import RegisterUser,validateUser

def createNewUser(email,name,surname,password,country,city):
  return RegisterUser(email,name,surname,password,country,city)