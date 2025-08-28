import os
from typing import Dict, Any, Optional
from dotenv import load_dotenv
from enum import Enum

# Load environment variables
load_dotenv()

class LLMProvider(str, Enum):
    OPENAI = "openai"
    GROQ = "groq"

class Config:
    def __init__(self):
        self.llm_provider = os.getenv("LLM_PROVIDER", "openai").lower()
        self.llm_model = os.getenv("LLM_MODEL", "gpt-4")
        self.temperature = float(os.getenv("LLM_TEMPERATURE", 0.3))
        self.max_tokens = int(os.getenv("MAX_TOKENS", 2000))
        
        # Provider-specific API keys
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.groq_api_key = os.getenv("GROQ_API_KEY")
        
        self._validate()
    
    def _validate(self):
        """Validate the configuration."""
        if self.llm_provider not in [p.value for p in LLMProvider]:
            raise ValueError(f"Unsupported LLM provider: {self.llm_provider}")
        
        if self.llm_provider == LLMProvider.OPENAI and not self.openai_api_key:
            raise ValueError("OpenAI API key is required when using OpenAI provider")
            
        if self.llm_provider == LLMProvider.GROQ and not self.groq_api_key:
            raise ValueError("Groq API key is required when using Groq provider")
        
        if not 0.0 <= self.temperature <= 1.0:
            raise ValueError("Temperature must be between 0.0 and 1.0")
        
        if self.max_tokens <= 0:
            raise ValueError("Max tokens must be greater than 0")
    
    def get_llm_config(self) -> Dict[str, Any]:
        """Get the configuration for the selected LLM provider."""
        base_config = {
            "model": self.llm_model,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
        }
        
        if self.llm_provider == LLMProvider.OPENAI:
            return {
                **base_config,
                "api_key": self.openai_api_key,
            }
        elif self.llm_provider == LLMProvider.GROQ:
            return {
                **base_config,
                "api_key": self.groq_api_key,
            }
        
        raise ValueError(f"Unsupported LLM provider: {self.llm_provider}")

# Global config instance
config = Config()
