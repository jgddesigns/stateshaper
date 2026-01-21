import os
print(os.environ["PATH"])

import json
from example_data.format_data.FormatData import FormatData
from stateshaper import RunEngine
from tools.tiny_state.TinyState import TinyState


class Demo:


    def __init__(self, user_id=None, **kwargs):
        super().__init__(**kwargs)


        self.connector = None

        # self.run_test()
        self.run_test("random")


    def format_test(self):
        self.format_data = FormatData(self.get_file("random"))
        self.format_data.compound_example()
        data = self.format_data.get_data()

        self.run_test(data)



    def run_test(self, test="compound"):
        if isinstance(test, str) == True:
            file = self.get_file(test)

            with open(file, "r") as f:
                self.data = json.loads(f.read())
                f.close()
        else: 
            self.data = test

        self.engine = RunEngine(self.data, token_count=50, initial_state=1)
        self.engine.start_engine()
        self.engine.run_engine()


    def get_file(self, test):
        return f"example_data/{test}.json"



Demo()