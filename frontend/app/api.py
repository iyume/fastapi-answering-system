import os
import httpx
from typing import Any, Dict, Optional, Union


host_url = 'http://127.0.0.1:8000'


async def get(uri: str, **params) -> Union[Dict[Any, Any], str, None]:
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(uri, params=params)
    except:
        return None
    return response.json()

async def post(uri: str, **params) -> Union[Dict[Any, Any], str, None]:
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(uri, data=params)
    except:
        return None
    return response.json()


class API():
    def __init__(self, version) -> None:
        self.api_uri = os.path.join(
            host_url, 'api', version
        )
        self.question_uri = os.path.join(self.api_uri, 'question/')
        self.answer_uri = os.path.join(self.api_uri, 'answer/')

    async def get_question_by_subject(
        self,
        subject: str,
        random: Optional[bool] = True
    ):
        if random:
            result = await get(
                self.question_uri,
                subject = subject,
                random = random
            )
        else:
            result = None
        return result

    async def get_answer(self, id: str):
        result = await get(
            self.answer_uri,
            id = id
        )
        return result

apifunc = API(version='v1')


class AUTH():
    def __init__(self, endpoint: str) -> None:
        self.auth_uri = os.path.join(
            host_url, endpoint
        )

    async def authenticate(self, name: str, password: str):
        content = await post(
            self.auth_uri,
            name = name,
            passowrd = password
        )
        if isinstance(content, str):
            return content
        token = getattr(content, 'access-token', None)
        return token

authfunc = AUTH(endpoint='auth/')
