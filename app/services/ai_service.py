import aiohttp
import json
from typing import Dict, Any

class AIService:
    def __init__(self):
        self.azure_endpoint = "https://gpt-candidate-test.openai.azure.com/"
        self.api_key = "4jcVWz6srd4Y7INprd7cpXGvodoPprnYd3cO3vC920sRWrXSCbvKJQQJ99AKACYeBjFXJ3w3AAABACOGBqy1"
        self.assistant_id = "asst_7y4JlZnzk3Agv6zvFTCEhj1Q"
        self.headers = {
            "api-key": self.api_key,
            "Content-Type": "application/json"
        }

    async def process_request(self, user_input: str, room_context: Dict[str, Any]) -> str:
        """Process user request with context-aware AI"""
        try:
            async with aiohttp.ClientSession() as session:
                payload = {
                    "messages": [
                        {
                            "role": "system",
                            "content": "You are a smart hotel room assistant helping guests with room controls and information."
                        },
                        {
                            "role": "user",
                            "content": f"Room Context: {json.dumps(room_context)}\nUser Request: {user_input}"
                        }
                    ],
                    "assistant_id": self.assistant_id
                }

                async with session.post(
                    f"{self.azure_endpoint}/v1/chat/completions",
                    headers=self.headers,
                    json=payload
                ) as response:
                    result = await response.json()
                    return result['choices'][0]['message']['content']
                    
        except Exception as e:
            return f"Error processing request: {str(e)}" 