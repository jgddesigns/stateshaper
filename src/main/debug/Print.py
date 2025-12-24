



class Print:

    def __init__(self, debug=True, **kwargs):
        super().__init__(**kwargs)

        self.debug = debug


    def p(self, txt, condition=None):
        if not condition:
            print(str(txt)) 
        else:
            print(str(txt)) if self.debug == True else None
        

    def s(self, spaces, condition=None):
        space = ""

        while len(space) < spaces * 2:
            space = space + "\n"

        if not condition:
            print(space)
        else: 
            print(space) if self.debug == True else None