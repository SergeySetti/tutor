import logging
import os

from dotenv import load_dotenv
from google.adk.sessions.database_session_service import DatabaseSessionService
from injector import Module, provider, singleton, Injector
from pymongo import MongoClient
from telegram import Bot

from infrastructure.curriculum_repository import CurriculumRepository
from infrastructure.db_config import MongoDBConfig
from infrastructure.settings import Settings

load_dotenv()


class AppModule(Module):
    def __init__(self):
        self._session_service = None

    def configure(self, binder):
        binder.bind(Bot, to=Bot(token=os.getenv("TELEGRAM_BOT_TOKEN")), scope=singleton)
        binder.bind(DatabaseSessionService, to=DatabaseSessionService(db_url=f'sqlite+aiosqlite:///{os.getenv("DB_PATH")}'), scope=singleton)
        binder.bind(CurriculumRepository, to=CurriculumRepository, scope=singleton)
        binder.bind(Settings, to=Settings(
            config={
                'telegram_bot_token': os.getenv("TELEGRAM_BOT_TOKEN"),
                'app_name' : 'tutor_bot',
                'mongodb_database' : 'tutor_bot_db',
            }
        ), scope=singleton)


    @provider
    @singleton
    def provide_logger(self) -> logging.Logger:
        global_logger = logging.getLogger("global")
        if not global_logger.handlers:
            global_logger.setLevel(logging.DEBUG)

            # Add timestamp to logs
            formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)

            # Rotate logs every day and keep 7 days of logs
            file_handler = logging.FileHandler("app.log")
            file_handler.setFormatter(formatter)

            global_logger.addHandler(file_handler)
            global_logger.addHandler(console_handler)
        return global_logger

    @provider
    @singleton
    def provide_mongodb_client(self) -> MongoClient:
        return MongoClient(os.getenv("MONGODB_URI"))

    @provider
    @singleton
    def provide_mongodb_config(self) -> MongoDBConfig:
        return MongoDBConfig(
            uri=os.getenv("MONGODB_URI"),
            database=os.getenv("MONGODB_DATABASE"),
        )


injector = Injector([AppModule()])
print("Injector initialized with AppModule.")
injector._cache = {}
