from .demos.ads.Ads import Ads
from .classes.connector.Connector import Connector
from .core import Stateshaper




class RunEngine:

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.plugin = Ads()
        self.connector = Connector(self.plugin.get_data())

        self.engine = None

        self.seed = None
        self.compressed_seed = None
        self.run_engine()


    def run_engine(self):
        self.seed = self.connector.start_connect()
        self.compressed_seed = self.compress_seed()
        self.engine = Stateshaper(
            self.seed["state"],
            self.seed["vocab"],
            self.seed["constants"],
            self.seed["mod"]
        )

        self.tokens = self.engine.generate_tokens(self.connector.token_count)
        
        print("\n\nTokens successfully generated from vocab.\n")