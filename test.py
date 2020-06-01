import enum

class Menu(enum.Enum):
    Scelta1 = 1
    Scelta2 = 2
    Scelta3 = 3
    Scelta4 = 4

class SwitchTest:
    def __init__(self):
        self.switch = {
            Menu.Scelta1.value: self.f1,
            Menu.Scelta2.value: self.f2, 
            Menu.Scelta3.value: self.f3,
            Menu.Scelta4.value: self.f4
        }

    def run(self, scelta):
        t = self.switch.get(int(scelta), None)
        if t:
            t()

    def f1(self):
        print("function 1")
    
    def f2(self):
        print("function 2")

    def f3(self):
        print("function 3")

    def f4(self):
        print("function 4")

def test():
    stest = SwitchTest()
    stest.run(1)
    stest.run(2)
    stest.run(5)
    stest.run(4)

test()