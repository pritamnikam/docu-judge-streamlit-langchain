from typing import Dict, Any, List, Optional
from langchain.schema import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
from config import config, LLMProvider
import os

class LLMService:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(LLMService, cls).__new__(cls)
            cls._instance.llm = None
            cls._instance.current_config = {
                "provider": config.llm_provider,
                "model": config.llm_model,
                "temperature": config.temperature,
                "max_tokens": config.max_tokens,
                "api_key": os.getenv("OPENAI_API_KEY") if config.llm_provider == LLMProvider.OPENAI else os.getenv("GROQ_API_KEY")
            }
        return cls._instance
    
    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.llm = self._initialize_llm()
            self.initialized = True
    
    def update_config(self, provider: str, model: str, temperature: float, max_tokens: int, api_key: str):
        """Update the LLM configuration and reinitialize if needed."""
        new_config = {
            "provider": provider,
            "model": model,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "api_key": api_key
        }
        
        # Only reinitialize if config has changed
        if new_config != self.current_config:
            self.current_config = new_config
            self.llm = self._initialize_llm()
    
    def _initialize_llm(self):
        """Initialize the LLM based on the current config."""
        provider = self.current_config["provider"]
        model = self.current_config["model"]
        temperature = self.current_config["temperature"]
        max_tokens = self.current_config["max_tokens"]
        api_key = self.current_config["api_key"]
        
        if not api_key:
            raise ValueError(f"API key not configured for provider: {provider}")
        
        if provider == LLMProvider.OPENAI:
            return ChatOpenAI(
                model_name=model,
                temperature=temperature,
                max_tokens=max_tokens,
                api_key=api_key
            )
        elif provider == LLMProvider.GROQ:
            return ChatGroq(
                model_name=model,
                temperature=temperature,
                max_tokens=max_tokens,
                groq_api_key=api_key
            )
        else:
            raise ValueError(f"Unsupported LLM provider: {provider}")
    
    async def evaluate_document(self, golden_standard: str, document: str) -> Dict[str, Any]:
        """
        Evaluate a document against the golden standard using the configured LLM.
        
        Args:
            golden_standard: The golden standard content
            document: The document content to evaluate
            
        Returns:
            Dict containing the evaluation results
        """
        system_prompt = """You are a judge and your task is to evaluate documents based on the provided golden standard.
        Analyze the content thoroughly and provide a verdict with confidence score.
        """
        
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=f"""
            GOLDEN STANDARD:
            {golden_standard}
            
            DOCUMENT TO EVALUATE:
            {document}
            
            Please provide:
            1. A verdict (Pass/Fail) based on the document's alignment with the golden standard
            2. A confidence score between 0 and 1 (1 being most confident)
            3. A brief explanation for your verdict
            
            Format your response as:
            VERDICT: [Pass/Fail]
            CONFIDENCE: [0-1]
            EXPLANATION: [Your explanation]
            """)
        ]
        
        try:
            response = await self.llm.ainvoke(messages)
            
            # Parse the response
            result = {
                "verdict": "",
                "confidence": 0.0,
                "explanation": "",
                "success": True,
                "error": None
            }
            
            for line in response.content.split('\n'):
                line = line.strip()
                if line.startswith("VERDICT:"):
                    result["verdict"] = line.split(":", 1)[1].strip()
                elif line.startswith("CONFIDENCE:"):
                    try:
                        result["confidence"] = float(line.split(":", 1)[1].strip())
                    except (ValueError, IndexError):
                        result["confidence"] = 0.0
                elif line.startswith("EXPLANATION:"):
                    result["explanation"] = line.split(":", 1)[1].strip()
            
            return result
            
        except Exception as e:
            return {
                "verdict": "Error",
                "confidence": 0.0,
                "explanation": str(e),
                "success": False,
                "error": str(e)
            }

# Global instance
llm_service = LLMService()
