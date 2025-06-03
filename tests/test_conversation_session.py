
import pytest
from unittest import TestCase, mock
from dotenv import load_dotenv

from src.conversation_session import (
    ConversationSession,
    defaultModelConfig,
)

load_dotenv()

class TestConversationSession(TestCase):
    def setUp(self):
        return super().setUp()
    
    def tearDown(self):
        return super().tearDown()
    
    def test_ceate_conversation(self):
        modelConfig = {**defaultModelConfig}
        modelConfig["chatter_type"] = "ServerAzureOpenAI"
        
        with mock.patch("src.conversation_session.AzureGptConversation") as mockAzureGptConversation:
            mockAzureGptConversation.return_value = mock.MagicMock()
            mockAzureGptConversation.return_value.query.return_value = ("Hello, how can I help you?", {}, None)
            mockAzureGptConversation.return_value.find_rag_agent.return_value = (None, None)
            session = ConversationSession(
                "abcdefg",
                modelConfig
            )
            self.assertIsNot(session, None)
            self.assertEqual(session.sessionData.sessionId, "abcdefg")
            self.assertIsNot(session.chatter, None)
         
            res = session.chat(
                messages=[
                    {"role": "user", "content": "Hi"}
                ],
                modelConfig=modelConfig,
            )
            self.assertIsNot(res, None)
    
    def test_create_conversation_server(self):
        modelConfig = {**defaultModelConfig}
        modelConfig["chatter_type"] = "ServerAzureOpenAI"
        with mock.patch("src.conversation_session.AzureGptConversation") as mockAzureGptConversation:
            mockAzureGptConversation.return_value = mock.MagicMock()
            mockAzureGptConversation.return_value.query.return_value = ("Hello, how can I help you?", {}, None)
            mockAzureGptConversation.return_value.find_rag_agent.return_value = (None, None)
            session = ConversationSession(
                "abcdefg",
                modelConfig
            )
            self.assertIsNot(session, None)
            self.assertEqual(session.sessionData.sessionId, "abcdefg")
            self.assertIsNot(session.chatter, None)
            session = ConversationSession(
                "abcdefg",
                modelConfig
            )
            res = session.chat(
                messages=[
                    {"role": "user", "content": "Hi"}
                ],
                modelConfig=modelConfig,
            )
            self.assertIsNot(res, None)

