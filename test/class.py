class Test(object):
    Tos = None
    rene = "carte"
    
    def __init__(self, x):
        self.x = x
    def __call__(self, y):
        return self.x + y
    def tos(self):
        print(self.x)

class Dog(type):
    def bark(x):
        print("Woof")
        
class Cat():

    color = "white"
    feet = 4

class Cat(
  object
):
  def __init__():
    print("Hello")