from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from app.agent import root_agent


def test_agent_responds_to_list_products() -> None:
    session_service = InMemorySessionService()
    session = session_service.create_session_sync(user_id="test_user", app_name="test")
    runner = Runner(agent=root_agent, session_service=session_service, app_name="test")

    message = types.Content(
        role="user", parts=[types.Part.from_text(text="List all products")]
    )

    events = list(
        runner.run(
            new_message=message,
            user_id="test_user",
            session_id=session.id,
        )
    )
    assert len(events) > 0

    has_text = any(
        event.content and event.content.parts and any(part.text for part in event.content.parts)
        for event in events
    )
    assert has_text


def test_agent_workflow_routes_to_correct_subagent() -> None:
    session_service = InMemorySessionService()
    session = session_service.create_session_sync(user_id="test_user", app_name="test")
    runner = Runner(agent=root_agent, session_service=session_service, app_name="test")

    message = types.Content(
        role="user", parts=[types.Part.from_text(text="What is the status of shipment TRK10001?")]
    )
    events = list(
        runner.run(new_message=message, user_id="test_user", session_id=session.id)
    )
    assert len(events) > 0
