from typing import Any, Dict, List

class Subjects():
    subjects = [
        {
            'alias': 'fb',
            'name_en': 'fund_basis',
            'name_zh': '基金基础',
            'question_count': 622
        },
        {
            'alias': 'fr',
            'name_en': 'fund_regulations',
            'name_zh': '基金法规',
            'question_count': 284
        },
        {
            'alias': 'sr',
            'name_en': 'security_regulations',
            'name_zh': '证券法规',
            'question_count': 160
        }
    ]

    def get_item(self, subject: str) -> Dict[str, Any]:
        if subject not in self.aliases:
            raise ValueError(f'no subject named "{subject}"')
        return [i for i in self.subjects if i['alias'] == subject][0]

    @property
    def items(self) -> list[dict]:
        return self.subjects

    @property
    def aliases(self) -> List[str]:
        return [str(i['alias']) for i in self.subjects]

subjects = Subjects()
