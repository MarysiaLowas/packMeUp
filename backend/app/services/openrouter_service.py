import aiohttp
import logging
import time
import os
import asyncio
from typing import Optional, Dict, Any, Callable
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Create console handler if it doesn't exist
if not logger.handlers:
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

class OpenRouterService:
    """Service class for interacting with the OpenRouter API.

    This class handles building and sending requests, as well as parsing responses and error handling.
    """

    def __init__(self, api_key: str, api_endpoint: str) -> None:
        """
        Initialize the service with API key and endpoint.
        """
        if not isinstance(api_key, str) or not api_key.strip():
            raise ValueError("API key must be a non-empty string")
        if not isinstance(api_endpoint, str) or not api_endpoint.strip():
            raise ValueError("API endpoint must be a non-empty string")
        self._api_key: str = api_key
        self._api_endpoint: str = api_endpoint
        self._system_message: str = ""
        self._user_message: str = ""
        self._response_format: Dict[str, Any] = {}
        self._model_name: str = ""
        self._model_parameters: Dict[str, Any] = {}
        
        # Retry configuration
        self._max_retries: int = 3
        self._backoff_factor: float = 1.0

    @classmethod
    def from_env(cls) -> 'OpenRouterService':
        """
        Create an instance of OpenRouterService using environment variables.
        Expects OPENROUTER_API_KEY and OPENROUTER_API_ENDPOINT to be set.
        """
        api_key = os.environ.get("OPENROUTER_API_KEY")
        api_endpoint = os.environ.get("OPENROUTER_API_ENDPOINT")
        if not api_key or not api_endpoint:
            raise ValueError("Environment variables OPENROUTER_API_KEY and OPENROUTER_API_ENDPOINT must be set")
        return cls(api_key, api_endpoint)

    # Public Methods
    def set_system_message(self, message: str) -> None:
        """Set the system message after validating it's a string."""
        if not isinstance(message, str):
            raise ValueError("System message must be a string")
        self._system_message = message

    def set_user_message(self, message: str) -> None:
        """Set the user message after validating it's a string."""
        if not isinstance(message, str):
            raise ValueError("User message must be a string")
        self._user_message = message

    def set_response_format(self, fmt: Dict[str, Any]) -> None:
        """Set the response format schema after validating it's a dictionary."""
        if not isinstance(fmt, dict):
            raise ValueError("Response format must be a dictionary")
        self._response_format = fmt

    def set_model_name(self, name: str) -> None:
        """Set the model name after validating it's a string."""
        if not isinstance(name, str):
            raise ValueError("Model name must be a string")
        self._model_name = name

    def set_model_parameters(self, params: Dict[str, Any]) -> None:
        """Set model parameters after validating they're provided as a dictionary."""
        if not isinstance(params, dict):
            raise ValueError("Model parameters must be a dictionary")
        self._model_parameters = params

    async def send_request(self) -> Any:
        """
        Send the request to the OpenRouter API asynchronously.
        """
        headers = {
            "Authorization": f"Bearer {self._api_key}",
            "Content-Type": "application/json"
        }
        payload = self._build_request_payload()
        logger.debug(f"Sending request to OpenRouter with payload: {payload}")
        
        timeout = aiohttp.ClientTimeout(
            total=90,  # Total timeout
            connect=10,  # Connection timeout
            sock_read=60  # Socket read timeout
        )
        
        for attempt in range(self._max_retries):
            try:
                async with aiohttp.ClientSession(timeout=timeout) as session:
                    async with session.post(
                        self._api_endpoint,
                        headers=headers,
                        json=payload
                    ) as response:
                        if response.status != 200:
                            text = await response.text()
                            logger.error(f"API call failed with status {response.status}: {text}")
                            raise Exception(f"API call failed with status code {response.status}: {text}")
                        
                        try:
                            data = await response.json()
                            logger.debug(f"Received response from OpenRouter: {data}")
                            return data
                        except asyncio.TimeoutError as e:
                            logger.error(f"Timeout while reading response: {e}")
                            raise Exception("OpenRouter API timeout while reading response")
                        except Exception as e:
                            logger.error(f"Error parsing response: {e}")
                            raise Exception(f"Error parsing OpenRouter response: {str(e)}")
                        
            except asyncio.TimeoutError as e:
                logger.error(f"Timeout during attempt {attempt + 1}: {e}")
                if attempt == self._max_retries - 1:
                    raise Exception("OpenRouter API timeout after all retries")
                wait = self._backoff_factor * (2 ** attempt)
                logger.info(f"Retrying in {wait} seconds...")
                await asyncio.sleep(wait)  # Use asyncio.sleep instead of time.sleep
                
            except Exception as e:
                logger.error(f"Attempt {attempt + 1} failed: {str(e)}", exc_info=True)
                if not self._should_retry(e) or attempt == self._max_retries - 1:
                    raise Exception(f"OpenRouter API error: {str(e)}")
                    
                wait = self._backoff_factor * (2 ** attempt)
                logger.info(f"Retrying in {wait} seconds...")
                await asyncio.sleep(wait)  # Use asyncio.sleep instead of time.sleep

    # Private Methods
    def _build_request_payload(self) -> Dict[str, Any]:
        """
        Build the payload for the API request.
        """
        messages = []
        if self._system_message:
            messages.append({
                "role": "system",
                "content": self._system_message
            })
        messages.append({
            "role": "user",
            "content": self._user_message
        })
        
        return {
            "model": self._model_name,
            "messages": messages,
            "response_format": self._response_format,
            **self._model_parameters
        }

    def _should_retry(self, error: Exception) -> bool:
        """
        Determine if the request should be retried based on the error.
        """
        if isinstance(error, (aiohttp.ClientError, aiohttp.ServerTimeoutError)):
            return True
        message = str(error)
        if "API call failed with status code" in message:
            try:
                code = int(message.split("status code")[1].split(":")[0].strip())
                return code >= 500
            except:
                pass
        return False 