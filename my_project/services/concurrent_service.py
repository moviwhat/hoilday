import asyncio
import aiohttp
import json
import time
from typing import List, Dict, Any
from config import Config

class ConcurrentRequestService:
    def __init__(self):
        self.max_concurrent = Config.MAX_CONCURRENT_REQUESTS
        self.api_base_url = Config.API_BASE_URL
        self.timeout = Config.API_TIMEOUT
        self.data_config_path = Config.DATA_CONFIG_PATH
        
        self.start_time = None
        self.completed_count = 0
        self.total_count = 0
        self.request_times = []
        self.lock = asyncio.Lock()
    
    def load_data_config(self) -> List[Dict[str, Any]]:
        try:
            with open(self.data_config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
                return config.get('data', [])
        except Exception as e:
            print(f"加载配置文件失败: {e}")
            return []
    
    async def print_progress(self):
        elapsed_time = time.time() - self.start_time
        avg_time = elapsed_time / self.completed_count if self.completed_count > 0 else 0
        remaining = self.total_count - self.completed_count
        
        print(f"=" * 50)
        print(f"总请求数: {self.total_count}")
        print(f"已完成: {self.completed_count}")
        print(f"剩余: {remaining}")
        print(f"平均每个请求耗时: {avg_time:.2f}秒")
        print(f"总耗时: {elapsed_time:.2f}秒")
        print(f"=" * 50)
    
    async def send_single_request(self, session: aiohttp.ClientSession, data_item: Dict[str, Any]) -> Dict[str, Any]:
        request_start_time = time.time()
        
        try:
            async with session.post(
                f"{self.api_base_url}/process",
                json=data_item,
                timeout=aiohttp.ClientTimeout(total=self.timeout)
            ) as response:
                result = await response.json()
                request_time = time.time() - request_start_time
                
                async with self.lock:
                    self.completed_count += 1
                    self.request_times.append(request_time)
                    await self.print_progress()
                
                return {
                    'data_id': data_item.get('id'),
                    'success': response.status == 200,
                    'status': response.status,
                    'result': {
                        'text': data_item.get('text', ''),
                        'photos': data_item.get('photos', []),
                        'generated_text': result.get('generated_text', '')
                    },
                    'request_time': request_time
                }
        except asyncio.TimeoutError:
            request_time = time.time() - request_start_time
            
            async with self.lock:
                self.completed_count += 1
                await self.print_progress()
            
            return {
                'data_id': data_item.get('id'),
                'success': False,
                'error': '请求超时',
                'request_time': request_time,
                'result': {
                    'text': data_item.get('text', ''),
                    'photos': data_item.get('photos', [])
                }
            }
        except Exception as e:
            request_time = time.time() - request_start_time
            
            async with self.lock:
                self.completed_count += 1
                await self.print_progress()
            
            return {
                'data_id': data_item.get('id'),
                'success': False,
                'error': str(e),
                'request_time': request_time,
                'result': {
                    'text': data_item.get('text', ''),
                    'photos': data_item.get('photos', [])
                }
            }
    
    async def process_with_semaphore(self, session: aiohttp.ClientSession, semaphore: asyncio.Semaphore, data_item: Dict[str, Any]) -> Dict[str, Any]:
        async with semaphore:
            return await self.send_single_request(session, data_item)
    
    async def send_concurrent_requests(self) -> List[Dict[str, Any]]:
        data_items = self.load_data_config()
        
        if not data_items:
            return []
        
        self.total_count = len(data_items)
        self.completed_count = 0
        self.request_times = []
        self.start_time = time.time()
        
        print(f"开始并发请求，总请求数: {self.total_count}, 最大并发数: {self.max_concurrent}")
        
        semaphore = asyncio.Semaphore(self.max_concurrent)
        
        async with aiohttp.ClientSession() as session:
            tasks = [
                self.process_with_semaphore(session, semaphore, item)
                for item in data_items
            ]
            
            results = await asyncio.gather(*tasks)
            
            total_time = time.time() - self.start_time
            avg_time = sum(self.request_times) / len(self.request_times) if self.request_times else 0
            
            print(f"\n所有请求已完成!")
            print(f"=" * 50)
            print(f"总请求数: {self.total_count}")
            print(f"总耗时: {total_time:.2f}秒")
            print(f"平均每个请求耗时: {avg_time:.2f}秒")
            print(f"=" * 50)
            
            return list(results)
    
    def execute(self) -> List[Dict[str, Any]]:
        return asyncio.run(self.send_concurrent_requests())
