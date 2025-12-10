
from plugins.ads.Ads import Ads



class Debug:


    def __init__(self, user_id=None, **kwargs):
        super().__init__(**kwargs)

        self.ads = Ads()

        self.test()


    def test(self):
        self.ads.get_data()


Debug()