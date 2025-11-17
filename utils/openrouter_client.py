"""
OpenRouter API Client for SmartResume AI
Handles interactions with OpenRouter API (alternative to Gemini)
"""

import os
import requests
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class OpenRouterClient:
    """Client for interacting with OpenRouter API"""
    
    def __init__(self):
        """Initialize the OpenRouter API client"""
        self.api_key = os.getenv("OPENROUTER_API_KEY")
        self.site_url = os.getenv("OPENROUTER_SITE_URL", "http://localhost:8503")
        self.site_name = os.getenv("OPENROUTER_SITE_NAME", "SmartResume AI")
        
        if not self.api_key:
            raise ValueError("OPENROUTER_API_KEY not found in environment variables")
        
        self.api_url = "https://openrouter.ai/api/v1/chat/completions"
        
        # Default to free model
        self.model = "google/gemma-3-27b-it:free"
        
        # Generation configuration
        self.generation_config = {
            "temperature": 0.7,
            "top_p": 0.95,
            "max_tokens": 1024,
        }
    
    def generate_content(self, prompt):
        """
        Generate content using OpenRouter API
        
        Args:
            prompt (str): The prompt to send to the API
            
        Returns:
            str: Generated content or error message
        """
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
                "HTTP-Referer": self.site_url,
                "X-Title": self.site_name,
            }
            
            data = {
                "model": self.model,
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                **self.generation_config
            }
            
            response = requests.post(
                url=self.api_url,
                headers=headers,
                data=json.dumps(data),
                timeout=30
            )
            
            # Check if request was successful
            if response.status_code == 200:
                result = response.json()
                
                # Extract the generated text
                if "choices" in result and len(result["choices"]) > 0:
                    content = result["choices"][0]["message"]["content"]
                    return content.strip()
                else:
                    return "Error: No content generated"
            
            elif response.status_code == 429:
                return "Rate limit exceeded. Please wait a moment and try again."
            
            elif response.status_code == 401:
                return "Invalid API key. Please check your configuration."
            
            else:
                error_data = response.json() if response.content else {}
                error_msg = error_data.get("error", {}).get("message", "Unknown error")
                return f"An error occurred: {error_msg}"
                
        except requests.exceptions.Timeout:
            return "Request timed out. Please try again."
        
        except requests.exceptions.ConnectionError:
            return "Connection error. Please check your internet connection."
        
        except Exception as e:
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
            
            # Check if result is an error
            if not result.startswith("Rate limit") and \
               not result.startswith("Invalid") and \
               not result.startswith("An error") and \
               not result.startswith("Error:") and \
               not result.startswith("Request timed") and \
               not result.startswith("Connection error"):
                return result
            
            # Retry with exponential backoff
            if attempt < max_retries:
                import time
                time.sleep(2 ** attempt)
        
        return result
