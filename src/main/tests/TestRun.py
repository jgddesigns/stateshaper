from main.core import MorphicSemanticEngine


class TestRun:

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


        self.engine = None



    def start(self, data):
        self.engine = MorphicSemanticEngine(
            data["input"],
            data["vocab"],
            data["constants"],
            data["mod"]
        )