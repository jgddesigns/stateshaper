
from demos.ads.Ads import Ads



class Demo:


    def __init__(self, user_id=None, **kwargs):
        super().__init__(**kwargs)

        self.ads = Ads()

        self.test()


    def test(self):
        self.ads.get_data()


Demo()