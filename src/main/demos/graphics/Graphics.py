class Graphics:


    def __init__(self, **kwargs):

        self.shapes = ["square","triangle","hexagon","diamond","trapezoid"]

        self.colors = ["red","blue","green","yellow","orange","purple","pink","cyan","lime","teal","emerald","indigo"]

        self.color_length = 6
        self.x_max = 5
        self.y_max = 5
        self.grid_size = self.x_max * self.y_max
        self.shape_count = 0



    def get_shapes(self, token):
        shapes = [] 

        while len(shapes) < (token % (self.grid_size-1)) + 1:
            shapes.append(self.draw_shape(token * (len(shapes) + 1)))

        return shapes


    def draw_shape(self, token):
        shape = self.get_shape(token)
        color = self.get_color(token)
        size = self.get_size(token)
        pos = self.get_pos(token)
        return {"shape": shape, "color": color, "size": size, "pos": pos}


    def get_shape(self, token):
        return self.shapes[token % len(self.shapes)]
    

    def get_color(self, token): 
        return token % len(self.colors)
        # letters = ["a", "b", "c", "d", "e", "f"]
        # color = ""

        # while len(color) < self.color_length:
        #     color = color + (letters[token % len(letters)] if (token * len(color)) % 3 == 0 else str((token * len(color) * 3) % 10))
        #     token = (token + len(color)) * token * len(color)
        #     token = self.cut(token, 4)

        # return "#" + str(color)


    def get_size(self, token):
        height = self.cut(token * self.cut(token, 2), 2) if token % 2 != 0 else self.cut((token * 1.75) * self.cut(token, 2), 2) % 24
        width = self.cut(token * self.cut(token, 2), 2) if token % 2 != 0 else self.cut((token * 1.25) * self.cut(token, 2), 2) % 24
        return {"width": width if width % 2 == 0 else width + 1 , "height": (height % 24) if width % 2 == 0 else width + 1}


    def get_pos(self, token):
        x = round((self.cut(token, 2) * 1.25)) % self.x_max
        y = round((self.cut(token, 2) * 1.5)) % self.y_max
        return {"x": x, "y": y}


    def cut(self, number, slice, forward=True):
        if forward == True:
            return int(str(number)[:slice])
        return int(str(number)[slice:])