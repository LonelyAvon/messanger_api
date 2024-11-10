import asyncio
from functools import wraps
import json
import aiohttp
from aiohttp import BasicAuth
from app.settings import settings
# from app.common.logger import logger




def handle_response_errors(retries=10, initial_delay=0.2):
        """
        a decorator for getting request results 
        or calling exceptions when receiving erroneous status codes
        if response has correct status code, returns payload as json,
        othervise intercepts any errors and throws them further to the calling code
        
        exception handling can be extended further as needed.
        
        in the current implementation, 
        it processes only 429 code - exceeding the request limit. 
        upon receiving this code, it makes several attempts to send a request 
        with an exponentially increasing pause between attempts

        Args:
            retries:
                number of attemps to send request
            initial_delay:
                delay in seconds for the first pause in attemps
        
        TODO: need to decompose error handling here 
        """
        def decorator(func):
            @wraps(func)
            async def wrapper(*args, **kwargs):
                for attempt in range(retries):
                    try:
                        url, status, data = await func(*args, **kwargs)
                        # correct respnse
                        if status < 400:
                            # logger.info(f"url {url} fetched")
                            return data
                        
                        # response is not correct, error handling
                        # logger.warning(f"url: {url} {status} data: {data}")
                        # too many requests
                        if status == 429:
                            delay = initial_delay * (2 ** (attempt + 1))
                            await asyncio.sleep(delay)
                            continue
                            
                        elif status in (412, 404):
                            return data
                        
                        else:
                            raise Exception(f"HTTP error {status} for URL {url}")    
                    
                    except asyncio.exceptions.TimeoutError:
                        delay = initial_delay * (2 ** (attempt + 1))
                        await asyncio.sleep(delay)
                        # logger.warning(f"TimeoutError occurred for attempt {attempt + 1}, retrying...")
                        continue

                    except Exception as e: # not response errors handling here11
                        # logger.warning(e)
                        raise e
                raise Exception("Max retries exceeded")
            return wrapper
        return decorator



class AsyncHttpClient:
    def __init__(self, base_url=None):
        self.base_url = base_url
        self.headers = {'Content-Type': 'application/json'}
        self.session = None

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.session.close()

    @handle_response_errors(10, 0.2)    
    async def _request(self, method: str, path: str, **kwargs):
        url = f"{self.base_url}{path}"
        async with self.session.request(method, url, headers=self.headers, **kwargs) as response:
            return url, response.status, await response.json()

    async def get(self, path: str, params: dict = None):
        return await self._request('GET', path, params=params)

    async def post(self, path: str, data: dict = None):
        return await self._request('POST', path, data=json.dumps(data))

    async def put(self, path: str, data: dict = None):
        return await self._request('PUT', path, data=json.dumps(data))

    async def delete(self, path: str, params: dict = None):
        return await self._request('DELETE', path, params=params)
    
    

        
async def get_client():
    async with AsyncHttpClient("https://api.currentsapi.services/v1") as client:
        yield client


