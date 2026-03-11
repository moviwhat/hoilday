from typing import List, Dict, Any
from services.concurrent_service import ConcurrentRequestService

class APIService:
    def __init__(self):
        self.concurrent_service = ConcurrentRequestService()
    
    def send_concurrent_requests(self) -> List[Dict[str, Any]]:
        return self.concurrent_service.execute()
