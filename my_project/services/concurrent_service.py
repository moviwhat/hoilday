import asyncio
import aiohttp
import json
from typing import List, Dict, Any
from config import Config

class ConcurrentRequestService:
    def __init__(self):
        self.max_concurrent = Config.MAX_CONCURRENT_REQUESTS
        self.api_base_url = Config.API_BASE_URL
        self.timeout = Config.API_TIMEOUT
        self.data_config_path = Config.DATA_CONFIG_PATH
    
    def load_data_config(self) -> List[Dict[str, Any]]:
        try:
            with open(self.data_config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
                return config.get('data', [])
        except Exception as e:
            print(f"加载配置文件失败: {e}")
            return []
    
    async def send_single_request(self, session: aiohttp.ClientSession, data_item: Dict[str, Any]) -> Dict[str, Any]:
        try:
            async with session.post(
                f"{self.api_base_url}/process",
                json=data_item,
                timeout=aiohttp.ClientTimeout(total=self.timeout)
            ) as response:
                result = await response.json()
                return {
                    'data_id': data_item.get('id'),
                    'success': response.status == 200,
                    'status': response.status,
                    'result': result
                }
        except asyncio.TimeoutError:
            return {
                'data_id': data_item.get('id'),
                'success': False,
                'error': '请求超时'
            }
        except Exception as e:
            return {
                'data_id': data_item.get('id'),
                'success': False,
                'error': str(e)
            }
    
    async def process_with_semaphore(self, session: aiohttp.ClientSession, semaphore: asyncio.Semaphore, data_item: Dict[str, Any]) -> Dict[str, Any]:
        async with semaphore:
            return await self.send_single_request(session, data_item)
    
    async def send_concurrent_requests(self) -> List[Dict[str, Any]]:
        data_items = self.load_data_config()
        
        if not data_items:
            return []
        
        semaphore = asyncio.Semaphore(self.max_concurrent)
        
        async with aiohttp.ClientSession() as session:
            tasks = [
                self.process_with_semaphore(session, semaphore, item)
                for item in data_items
            ]
            
            results = await asyncio.gather(*tasks)
            
            return list(results)
    
    def execute(self) -> List[Dict[str, Any]]:
        return asyncio.run(self.send_concurrent_requests())
