import os
from re import L
import httpx
from typing import Any, Dict, Optional, Union

from app.schema.token import Token


host_url = 'http://127.0.0.1:8000'


async def get(uri: str, **params) -> Union[Dict[Any, Any], str, None]:
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(uri, params=params)
    except:
        return None
    return response.json()

async def post_with_params(uri: str, **params) -> Union[Dict[Any, Any], str, None]:
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(uri, params=params)
    except:
        return None
    return response.json()

async def post_with_json(uri: str, **params) -> Union[Dict[Any, Any], str, None]:
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(uri, json=params)
    except:
        return None
    return response.json()


# collection of resource will tail with slash
# single endpoint end to be empty
class API():
    def __init__(self, version) -> None:
        self.api_uri = os.path.join(host_url, 'api', version)
        self.question_uri = os.path.join(self.api_uri, 'question', '')
        self.answer_uri = os.path.join(self.api_uri, 'answer', '')

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


class AUTH():
    def __init__(self, endpoint: str) -> None:
        self.auth_uri = os.path.join(host_url, endpoint)
        self.auth_access_token_uri = os.path.join(self.auth_uri, 'access-token')
        self.auth_retrieve_user_uri = os.path.join(self.auth_uri, 'retrieve-user')
        self.auth_register_uri = os.path.join(self.auth_uri, 'register')

    async def authenticate(self, name: str, password: str):
        # content = await post_with_params(
        #     self.auth_access_token_uri,
        #     name = name,
        #     passowrd = password
        # )
        async with httpx.AsyncClient() as client:
            content = await client.post(
                self.auth_access_token_uri,
                params={'name': name, 'password': password}
            )
        content = content.json()

        if isinstance(content, str):
            return content
        if token := content.get('access-token', None):
            tokenmodel = Token(access_token=token)
            return tokenmodel
        return 'invalid name or password'

    async def get_user_by_jwt(self, jwt: str):
        content = await post_with_json(
            self.auth_retrieve_user_uri
        )

    async def register(self, name: str, email: str, password: str):
        content = await post_with_json(
            self.auth_register_uri,
            name = name,
            email = email,
            password = password
        )
        # async with httpx.AsyncClient() as client:
        #     content = await client.post(
        #         self.auth_register_uri,
        #         data={'name': name, 'email': email, 'password': password}
        #     )
        # content = content.json()

        if isinstance(content, str):
            return content
        if token := await self.authenticate(name, password):
            return Token(token=token)
        return 'invalid name or email or password'


apifunc = API(version='v1')
authfunc = AUTH(endpoint='auth')
