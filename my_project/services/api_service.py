from typing import List, Dict, Any
from services.concurrent_service import ConcurrentRequestService

class APIService:
    def __init__(self):
        self.concurrent_service = ConcurrentRequestService()
    
    def send_concurrent_requests(self, user_prompt: str = '', style: str = '文艺', system_prompt: str = '') -> List[Dict[str, Any]]:
        return self.concurrent_service.execute(
            user_prompt=user_prompt,
            style=style,
            system_prompt=system_prompt
        )
