class Settings:
    def __init__(self, config: dict):
        self.config = config

    def get(self, key: str, default=None):
        return self.config.get(key, default)
