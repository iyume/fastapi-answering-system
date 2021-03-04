import os
from typing import Any, Optional
import httpx

from fastapi import HTTPException

from app import schema
from app.config import logger


host_url = 'http://127.0.0.1:8000'


def error_handlers(status_code) -> None:
    if status_code == 403:
        raise HTTPException(
            status_code=403, detail='403 Forbidden')
    if status_code == 400:
        raise HTTPException(
            status_code=400, detail='Bad request caused by inner api request')


async def get(uri: str, **params) -> Any:
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(uri, params=params)
    except:
        raise HTTPException(
            status_code=500, detail='500 Server error')
    error_handlers(response.status_code)
    return response.json()

async def post_with_params(uri: str, **params) -> Any:
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(uri, params=params)
    except:
        raise HTTPException(
            status_code=500, detail='500 Server error')
    error_handlers(response.status_code)
    return response.json()

async def post_with_json(uri: str, **params) -> Any:
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(uri, json=params)
    except:
        raise HTTPException(
            status_code=500, detail='500 Server error')
    error_handlers(response.status_code)
    return response.json()


# collection of resource will tail with slash
# single endpoint end to be empty
class API():
    def __init__(self, version) -> None:
        self.api_uri = os.path.join(host_url, 'api', version)
        self.question_uri = os.path.join(self.api_uri, 'question', '')
        self.answer_uri = os.path.join(self.api_uri, 'answer', '')

    async def get_question_by_subject(
        self, subject: str, random: bool = True) -> dict:
        result = await get(
            self.question_uri,
            subject = subject,
            random = random
        )
        if not result:
            raise HTTPException(status_code=500)
        return result

    async def get_answer(self, id: str) -> dict:
        result = await get(
            self.answer_uri,
            id = id
        )
        if not result:
            raise HTTPException(status_code=400, detail='incorrect question id')
        return result


class AUTH():
    def __init__(self, endpoint: str) -> None:
        self.auth_uri = os.path.join(host_url, endpoint)
        self.auth_access_token_uri = os.path.join(self.auth_uri, 'access-token')
        self.auth_retrieve_payload_uri = os.path.join(self.auth_uri, 'retrieve-payload')
        self.auth_register_uri = os.path.join(self.auth_uri, 'register')

    async def authenticate(self, name: str, password: str) -> schema.JWT:
        content = await post_with_json(
            self.auth_access_token_uri,
            name = name,
            password = password
        )

        if isinstance(content, str):
            raise HTTPException(status_code=403, detail='Validate user error')
        token = content.get('access-token', None)
        if not token:
            raise HTTPException(status_code=403, detail='')
        tokenmodel = schema.JWT(access_token=token)
        return tokenmodel

    async def retrieve_payload(self, jwt: str) -> dict:
        content = await post_with_json(
            self.auth_retrieve_payload_uri,
            jwt = jwt
        )
        if isinstance(content, str):
            raise HTTPException(status_code=500, detail=content)
        return content

    async def register(self, name: str, email: str, password: str) -> schema.JWT:
        content = await post_with_json(
            self.auth_register_uri,
            name = name,
            email = email,
            password = password
        )

        if isinstance(content, str):
            raise HTTPException(status_code=400, detail=content)
        token = await self.authenticate(name, password)
        return token


apifunc = API(version='v1')
authfunc = AUTH(endpoint='auth')
