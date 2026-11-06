import random

class home_todo:
    def __init__(self, name):
        self.name = name

    def random_todo(self):

        i = ['Помыться', 'Пожукить', 'Побибиматься']
        x = random.choice(i)
        return(x)

    def format(self):
        text = self.random_todo()
        return text