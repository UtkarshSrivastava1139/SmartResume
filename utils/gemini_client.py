"""
Gemini API Client for SmartResume AI
Handles all interactions with Google's Gemini API
"""

import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class GeminiClient:
    """Client for interacting with Google Gemini API"""
    
    def __init__(self):
        """Initialize the Gemini API client"""
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
        
        genai.configure(api_key=api_key)
        try:
            self.model = genai.GenerativeModel('gemini-2.5-flash')
        except:
            self.model = genai.GenerativeModel('gemini-pro')
        
        # Generation configuration
        self.generation_config = {
            "temperature": 0.7,
            "top_p": 0.95,
            "top_k": 40,
            "max_output_tokens": 1024,
        }
    
    def generate_content(self, prompt):
        """
        Generate content using Gemini API
        
        Args:
            prompt (str): The prompt to send to the API
            
        Returns:
            str: Generated content or error message
        """
        try:
            response = self.model.generate_content(
                prompt,
                generation_config=self.generation_config
            )
            return response.text.strip()
        except Exception as e:
            error_msg = str(e).lower()
            if "quota" in error_msg or "rate" in error_msg:
                return "Rate limit exceeded. Please wait a moment and try again."
            elif "api key" in error_msg:
                return "Invalid API key. Please check your configuration."
            else:
                return f"An error occurred: {str(e)}"
    
    def generate_with_retry(self, prompt, max_retries=2):
        """
        Generate content with retry logic
        
        Args:
            prompt (str): The prompt to send
            max_retries (int): Maximum number of retries
            
        Returns:
            str: Generated content or error message
        """
        for attempt in range(max_retries + 1):
            result = self.generate_content(prompt)
            if not result.startswith("Rate limit") and not result.startswith("Invalid") and not result.startswith("An error"):
                return result
            if attempt < max_retries:
                import time
                time.sleep(2 ** attempt)  # Exponential backoff
        return result
