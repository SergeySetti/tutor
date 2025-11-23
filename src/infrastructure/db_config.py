class MongoDBConfig:
    def __init__(self, uri: str, database: str) -> None:
        self.URI = uri
        self.DATABASE = database
