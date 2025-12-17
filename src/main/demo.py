
from demos.markov.Markov import Markov



class Demo:


    def __init__(self, user_id=None, **kwargs):
        super().__init__(**kwargs)

        self.markov = Markov()

        self.start()


    def start(self):
        self.markov.run("standard")


Demo()