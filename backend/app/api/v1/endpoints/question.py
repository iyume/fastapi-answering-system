from fastapi import APIRouter

from app.db.database import database

router = APIRouter(prefix='/question')

@router.get('/')
async def get_question(subject: str='fb'):
    subject2table = {'fb': '基金基础', 'fr': '基金法规', 'sr': '证券法规'}
    if subject in subject2table:
        query = f"SELECT id,问题,A,B,C,D FROM {subject2table[subject]} ORDER BY RANDOM() LIMIT 0,1"
    else:
        return {'result': 'Not supperted subject'}

    if result := await database.fetch_one(query):
        id, question, option_a, option_b, option_c, option_d = result
        return {'id': id,
                'q': question,
                'a': option_a,
                'b': option_b,
                'c': option_c,
                'd': option_d}
    else:
        return {'result': 'None'}
