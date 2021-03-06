import os
from typing import Any

import httpx

from fastapi import HTTPException

from app import schema


host_url = 'http://127.0.0.1:8000'
timeout = 8


def error_handlers(status_code: int) -> None:
    if status_code == 403:
        raise HTTPException(
            status_code=403, detail='Forbidden')
    if status_code == 400:
        raise HTTPException(
            status_code=400, detail='Bad request')
    if status_code == 422:
        raise HTTPException(
            status_code=422, detail='Validation error')
    if status_code != 200:
        raise HTTPException(status_code=status_code)


async def get(uri: str, **params: Any) -> Any:
    try:
        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.get(uri, params=params)
    except:
        raise HTTPException(
            status_code=500, detail='500 Server error')
    error_handlers(response.status_code)
    return response.json()

async def post_with_params(uri: str, **params: Any) -> Any:
    try:
        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.post(uri, params=params)
    except:
        raise HTTPException(
            status_code=500, detail='500 Server error')
    error_handlers(response.status_code)
    return response.json()

async def post_with_json(uri: str, **params: Any) -> Any:
    try:
        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.post(uri, json=params)
    except:
        raise HTTPException(
            status_code=500, detail='500 Server error')
    error_handlers(response.status_code)
    return response.json()


# collection of resource will tail with slash
# single endpoint end to be empty
class API():
    def __init__(self, version: str) -> None:
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
        self.auth_retrieve_detail_uri = os.path.join(self.auth_uri, 'retrieve-detail')
        self.auth_register_uri = os.path.join(self.auth_uri, 'register')

    async def access_token(self, name: str, password: str) -> schema.JWT:
        content = await post_with_json(
            self.auth_access_token_uri,
            name = name,
            password = password
        )
        if isinstance(content, str):
            raise HTTPException(status_code=403, detail='Validate user error')
        token = content.get('access_token', None)
        if not token:
            raise HTTPException(status_code=403, detail='')
        tokenmodel = schema.JWT(access_token=token)
        return tokenmodel

    async def retrieve_payload(self, jwt: str) -> dict:
        return await post_with_params(
            self.auth_retrieve_payload_uri,
            jwt = jwt
        )

    async def retrieve_detail(self, jwt: str) -> dict:
        return await post_with_params(
            self.auth_retrieve_detail_uri,
            jwt = jwt
        )

    async def register(self, name: str, email: str, password: str) -> schema.JWT:
        content = await post_with_json(
            self.auth_register_uri,
            name = name,
            email = email,
            password = password
        )
        if isinstance(content, str):
            raise HTTPException(status_code=400, detail=content)
        token = await self.access_token(name, password)
        return token


apifunc = API(version='v1')
authfunc = AUTH(endpoint='auth')
