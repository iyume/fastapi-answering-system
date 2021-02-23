import httpx

api_url = 'http://127.0.0.1:8000/api/v1/'

async def question_random(subject: str):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f'{api_url}question/?subject={subject}')
    except:
        return None
    json = response.json()
    if (*json,) == ('id', 'q', 'a', 'b', 'c', 'd'):
        return json
    else:
        return None

async def get_answer(subject: str, id: str):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f'{api_url}answer/?subject={subject}&id={id}')
    except:
        return None
    json = response.json()
    if (*json,) == ('id', 'q', 'a', 'b', 'c', 'd', 'answer'):
        return json
    else:
        return None
