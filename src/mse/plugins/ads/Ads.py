

class Ads:




    def __init__(self, user_id=None, **kwargs):
        super().__init__(**kwargs)

        self.user_id = user_id

        self.data_format = {
            "input": [],
            "rules": "rating",
            "length": 10
        }

        if user_id:
            print("\nFetching user based on entered user ID.")
            self.get_user()
        else:
            print("\nCreating new user.")
            self.create_user()


    ## get user seed from database.
    def get_user(self):

        ## for demo use mock seed. 
        self.current_seed = {
            "user_id": "1234",
            "state": [
                3404,
                832,
                2194,
                6734,
                105
            ],
            "vocab": [],
            "mod": 9973,
            "constants": {
                "a": 3,
                "b": 5,
                "c": 7,
                "d": 11
            }
        }


    def create_user(self):
        self.user_id = "1235"
        self.create_data()


    def create_seed(self):
        self.current_seed = {
            "user_id": self.user_id,
            "state": [
                3404,
                832,
                2194,
                6734,
                105
            ],
            "vocab": [],
            "mod": 9973,
            "constants": {
                "a": 3,
                "b": 5,
                "c": 7,
                "d": 11
            }
        }


    # build a list of the ads to be shown. contains actual url. for demo, some images will be included in this directory.
    def get_ads(self):
        pass


    def create_data(self):
        pass