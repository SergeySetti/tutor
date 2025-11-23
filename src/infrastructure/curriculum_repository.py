import datetime
from typing import Dict

import pytz
from injector import inject
from pymongo import MongoClient, ASCENDING

from domain.models.corriculum_state import CurriculumState
from infrastructure.db_config import MongoDBConfig


class CurriculumRepository:
    @inject
    def __init__(self, db_config: MongoDBConfig) -> None:
        self.client = MongoClient(db_config.URI)
        self.db = self.client[db_config.DATABASE]
        self.collection = self.db["curriculums"]

        # Ensure compound index on chat_id and date for better query performance
        try:
            self.collection.create_index([("user_name", ASCENDING)])
        except Exception:
            print("Index for InteractionRepository already exists")

    def insert_update_curriculum_state(self, user_name: str, state: CurriculumState) -> None:
        """Insert or update the curriculum state for a user."""
        self.collection.update_one(
            {"user_name": user_name},
            {"$set": {"state": state.model_dump_json(), "updated_at": datetime.datetime.now(pytz.utc)}},
            upsert=True
        )

    def get_curriculum_state(self, user_name: str) -> Dict | None:
        """Retrieve the curriculum state for a user."""
        document = self.collection.find_one({"user_name": user_name})
        if document:
            return CurriculumState.from_json(document.get("state"))
        return None
