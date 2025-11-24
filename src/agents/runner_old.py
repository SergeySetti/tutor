from logging import Logger
from typing import Optional

from google.adk import Runner
from google.adk.sessions import Session
from google.adk.sessions.database_session_service import DatabaseSessionService
from google.genai import types
from telegram import Update

from agents.telegram_agent.agent import root_agent
from container import injector
from infrastructure.settings import Settings

session_service = injector.get(DatabaseSessionService)
settings = injector.get(Settings)


async def call_agent_async(
        message: str,
        agent_instance,
        update,
        logger: Logger,
        settings: Settings,
        session_service: DatabaseSessionService,
):
    app_name = settings.get('app_name')

    runner = Runner(
        agent=agent_instance,
        app_name=app_name,
        session_service=session_service
    )

    state = {
        "chat_id": update.effective_chat.id,
        "user_id": update.effective_user.id,
        "first_name": update.effective_user.first_name,
        "last_name": update.effective_user.last_name or "",
        "username": update.effective_user.username or "",
        "message_id": update.message.message_id,
        "message_text": update.message.text or "",
    }

    user_id = str(state.get("user_id"))
    session_id = f"{state.get('chat_id')}-{user_id}-{update.message.date.date()}"

    stored_session: Session | None = await runner.session_service.get_session(
        app_name=runner.app_name,
        user_id=user_id,
        session_id=session_id
    )

    if stored_session:
        logger.info(f"Resuming session {session_id} for user {user_id}.")
    else:
        logger.info(f"Creating new session {session_id} for user {user_id}.")
        stored_session = await runner.session_service.create_session(
            app_name=runner.app_name,
            user_id=user_id,
            session_id=session_id,
            state=state
        )

    content = types.Content(parts=[
        types.Part(text=message)
    ])

    final_response_text = "Agent did not produce a final response."  # Default

    async for event in runner.run_async(user_id=user_id, session_id=session_id, new_message=content):
        logger.info(f"Event with content: {event.content}")
        if event.is_final_response():
            if event.content and event.content.parts:
                final_response_text = event.content.parts[0].text
            elif event.actions and event.actions.escalate:  # Handle potential errors/escalations
                logger.error(f"Agent escalated: {event.error_message or 'No specific message.'}")
            break

    return final_response_text


async def reply_to_mention(message: str, update: Update, logger) -> Optional[str]:
    logger.info(f"Message to agent: {update.message.text}")

    result = await call_agent_async(
        message,
        root_agent,
        update,
        logger,
        settings,
        session_service
    )

    return result.replace("—", "-").strip() if result else None
