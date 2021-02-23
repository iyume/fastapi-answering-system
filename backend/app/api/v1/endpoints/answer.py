from fastapi import APIRouter

from app.db.database import database

router = APIRouter(prefix='/answer')

@router.get('/')
async def get_answer_by_id(subject: str = 'fb', id: str = None):
    if not id:
        return {'result': 'Get with question id'}

    subject2table = {'fb': '基金基础', 'fr': '基金法规', 'sr': '证券法规'}
    if subject in subject2table:
        query = f"SELECT id,问题,A,B,C,D,答案 FROM {subject2table[subject]} WHERE id = '{id}'"
    else:
        return {'result': 'Not supperted subject'}

    if result := await database.fetch_one(query):
        id, question, option_a, option_b, option_c, option_d, answer = result
        return {'id': id,
                'q': question,
                'a': option_a,
                'b': option_b,
                'c': option_c,
                'd': option_d,
                'answer': answer.upper()}
    else:
        return {'result': 'None'}
