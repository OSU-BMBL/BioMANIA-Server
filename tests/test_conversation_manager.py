
from unittest import mock
import pytest

from src.conversation_manager import (
    get_conversation, 
    has_conversation,
    initialize_conversation, 
    remove_conversation,
)
from src.conversation_session import defaultModelConfig
from src.llm_auth import _parse_api_key

def test_parse_api_key():
    res = _parse_api_key("Bearer balahbalah")
    assert res == "balahbalah"


def test_get_conversation():
    modelConfig = {
        **defaultModelConfig,
        "chatter_type": "ServerOpenAI",
    }
    with mock.patch("src.conversation_session.GptConversation") as mockGptConversation:
        conversation = get_conversation(
            sessionId="balahbalah", modelConfig=modelConfig,
        )
    assert conversation is not None
    assert conversation.sessionData.sessionId == "balahbalah"
    assert conversation.chatter is not None
    assert has_conversation("balahbalah") 

def test_remove_conversation():
    sessionId = "test"
    assert not has_conversation(sessionId)
    initialize_conversation(
        sessionId=sessionId,
        modelConfig={
            "model": "gpt-3.5-turbo",
            "temperature": 0.7,
            "max_tokens": 2000,
            "presence_penalty": 0,
            "frequency_penalty": 0,
            "sendMemory": True,
            "historyMessageCount": 4,
            "compressMessageLengthThreshold": 2000,
        }
    )
    assert has_conversation(sessionId)
    remove_conversation(sessionId)
    assert not has_conversation(sessionId)


