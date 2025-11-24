from datetime import datetime
from logging import Logger
from typing import Optional

from google.adk import Runner
from google.adk.events import Event, EventActions
from google.adk.sessions import Session
from google.adk.sessions.database_session_service import DatabaseSessionService
from google.genai.types import Content, Part
from telegram import Update

from agents.telegram_agent.agent import root_agent
from container import injector
from domain.models.corriculum_state import CurriculumState
from infrastructure.curriculum_repository import CurriculumRepository
from infrastructure.settings import Settings

session_service = injector.get(DatabaseSessionService)
settings = injector.get(Settings)
curriculum_repository: CurriculumRepository = injector.get(CurriculumRepository)


async def init_session(app_name: str, user_id: str, session_id: str, user_name) -> Session:
    session = await session_service.get_session(
        app_name=app_name,
        user_id=user_id,
        session_id=session_id,
    )
    if session:
        print(f"Session already exists: App='{app_name}', User='{user_id}', Session='{session_id}'")
        return session

    initial_curriculum = curriculum_repository.get_curriculum_state(user_id)
    if not initial_curriculum:
        initial_curriculum = CurriculumState.get_initial_curriculum_from_json()
        curriculum_repository.insert_update_curriculum_state(user_id, initial_curriculum)

    session = await session_service.create_session(
        app_name=app_name,
        user_id=user_id,
        session_id=session_id,
        state={
            "user_name": user_name,
            "current_curriculum": initial_curriculum.model_dump_json()
        }  # Initial state
    )
    print(f"Session created: App='{app_name}', User='{user_id}', Session='{session_id}'")
    return session


app_name, session_id = "agents", "session1"


async def call_agent_async(
        message: str,
        update,
        logger: Logger,
):
    user_id = str(update.effective_user.id)

    session = await init_session(app_name, user_id, session_id, user_name=update.effective_user.username or "")

    runner = Runner(
        agent=root_agent,
        app_name=app_name,
        session_service=session_service
    )

    final_response_text = "..."

    user_message = Content(parts=[Part(text=message)])
    for event in runner.run(user_id=user_id, session_id=session_id, new_message=user_message):
        # Logging each event
        logger.info(f"Tool call event: {event}")
        if event.is_final_response():
            final_response_text = event.content.parts[0].text
            print(event.content.parts)

    updated_session = await session_service.get_session(app_name=app_name, user_id=user_id, session_id=session_id)
    return final_response_text


async def reply_to_mention(message: str, update: Update, logger) -> Optional[str]:
    logger.info(f"Message to agent: {update.message.text}")

    result = await call_agent_async(
        message,
        update,
        logger
    )

    return result.replace("—", "-").strip() if result else None
