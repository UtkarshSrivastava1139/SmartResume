"""
Unified AI Client for SmartResume AI
Automatically selects between Gemini and OpenRouter based on available API keys
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class AIClient:
    """Unified client that uses Gemini or OpenRouter based on configuration"""
    
    def __init__(self):
        """Initialize the AI client with available providers"""
        self.client = None
        self.provider = None
        
        # Try Gemini first
        gemini_key = os.getenv("GEMINI_API_KEY")
        openrouter_key = os.getenv("OPENROUTER_API_KEY")
        
        if gemini_key:
            try:
                from utils.gemini_client import GeminiClient
                self.client = GeminiClient()
                self.provider = "Gemini"
                return
            except Exception as e:
                print(f"Failed to initialize Gemini: {e}")
        
        # Fallback to OpenRouter
        if openrouter_key:
            try:
                from utils.openrouter_client import OpenRouterClient
                self.client = OpenRouterClient()
                self.provider = "OpenRouter"
                return
            except Exception as e:
                print(f"Failed to initialize OpenRouter: {e}")
        
        # No API keys available
        raise ValueError("No AI API keys found. Please configure GEMINI_API_KEY or OPENROUTER_API_KEY in .env file")
    
    def generate_content(self, prompt):
        """
        Generate content using available AI provider
        
        Args:
            prompt (str): The prompt to send to the API
            
        Returns:
            str: Generated content or error message
        """
        if not self.client:
            return "No AI provider configured. Please add API keys to .env file."
        
        return self.client.generate_content(prompt)
    
    def generate_with_retry(self, prompt, max_retries=2):
        """
        Generate content with retry logic
        
        Args:
            prompt (str): The prompt to send
            max_retries (int): Maximum number of retries
            
        Returns:
            str: Generated content or error message
        """
        if not self.client:
            return "No AI provider configured. Please add API keys to .env file."
        
        return self.client.generate_with_retry(prompt, max_retries)
    
    def get_provider_name(self):
        """Get the name of the active AI provider"""
        return self.provider if self.provider else "None"
