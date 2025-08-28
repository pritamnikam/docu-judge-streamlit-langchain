import pytest
from unittest.mock import AsyncMock, MagicMock, patch
import os
import sys

# Add the parent directory to the path so we can import our modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from llm_service import LLMService
from config import LLMProvider

# Test data
TEST_GOLDEN_STANDARD = """# Test Standard
- Item 1
- Item 2
"""

TEST_DOCUMENT = """# Test Document
- Item 1
- Item 2
- Item 3
"""

# Mock responses
MOCK_RESPONSE = """
VERDICT: Pass
CONFIDENCE: 0.9
EXPLANATION: The document meets all the requirements.
"""

# Fixtures
@pytest.fixture
def mock_openai_response():
    mock = AsyncMock()
    mock.content = MOCK_RESPONSE
    return mock

@pytest.fixture
def mock_llm(mock_openai_response):
    mock = AsyncMock()
    mock.ainvoke.return_value = mock_openai_response
    return mock

# Tests
class TestLLMService:
    @pytest.mark.asyncio
    async def test_evaluate_document_success(self, mock_llm):
        # Arrange
        with patch('langchain_openai.ChatOpenAI', return_value=mock_llm):
            service = LLMService()
            
            # Act
            result = await service.evaluate_document(TEST_GOLDEN_STANDARD, TEST_DOCUMENT)
            
            # Assert
            assert result["success"] is True
            assert result["verdict"] == "Pass"
            assert result["confidence"] == 0.9
            assert "meets all the requirements" in result["explanation"]
    
    @pytest.mark.asyncio
    async def test_evaluate_document_error_handling(self, mock_llm):
        # Arrange
        mock_llm.ainvoke.side_effect = Exception("API Error")
        
        with patch('langchain_openai.ChatOpenAI', return_value=mock_llm):
            service = LLMService()
            
            # Act
            result = await service.evaluate_document(TEST_GOLDEN_STANDARD, "")
            
            # Assert
            assert result["success"] is False
            assert result["verdict"] == "Error"
            assert "API Error" in result["error"]
    
    @pytest.mark.parametrize("provider,model_name", [
        (LLMProvider.OPENAI, "gpt-4"),
        (LLMProvider.OPENAI, "gpt-3.5-turbo"),
        (LLMProvider.GROQ, "mixtral-8x7b-32768"),
        (LLMProvider.GROQ, "llama2-70b-4096"),
    ])
    def test_llm_initialization(self, provider, model_name):
        # Arrange
        with patch('langchain_openai.ChatOpenAI') as mock_openai, \
             patch('langchain_groq.ChatGroq') as mock_groq:
            
            # Act
            with patch('config.config.llm_provider', provider), \
                 patch('config.config.llm_model', model_name):
                
                service = LLMService()
                
                # Assert
                if provider == LLMProvider.OPENAI:
                    mock_openai.assert_called_once()
                    assert mock_groq.call_count == 0
                else:
                    mock_groq.assert_called_once()
                    assert mock_openai.call_count == 0
    
    @pytest.mark.parametrize("response_text,expected_verdict,expected_confidence", [
        ("VERDICT: Pass\nCONFIDENCE: 0.9\nEXPLANATION: Good", "Pass", 0.9),
        ("VERDICT: Fail\nCONFIDENCE: 0.1\nEXPLANATION: Bad", "Fail", 0.1),
        ("INVALID FORMAT", "", 0.0),  # Test with invalid format
    ])
    @pytest.mark.asyncio
    async def test_response_parsing(self, response_text, expected_verdict, expected_confidence):
        # Arrange
        mock_llm = AsyncMock()
        mock_response = MagicMock()
        mock_response.content = response_text
        mock_llm.ainvoke.return_value = mock_response
        
        with patch('langchain_openai.ChatOpenAI', return_value=mock_llm):
            service = LLMService()
            
            # Act
            result = await service.evaluate_document("", "")
            
            # Assert
            assert result["verdict"] == expected_verdict
            assert result["confidence"] == expected_confidence
