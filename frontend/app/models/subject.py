class Subjects():
    subjects = [
        {
            'alias': 'fb',
            'name_en': 'fund_basis',
            'name_zh': '基金基础',
            'area_endpoint': 'tiku_area_fb',
            'paper_endpoint': 'tiku_paper_fb'
        },
        {
            'alias': 'fr',
            'name_en': 'fund_regulations',
            'name_zh': '基金法规',
            'area_endpoint': 'tiku_area_fr',
            'paper_endpoint': 'tiku_paper_fb'
        },
        {
            'alias': 'sr',
            'name_en': 'security_regulations',
            'name_zh': '证券法规',
            'area_endpoint': 'tiku_area_sr',
            'paper_endpoint': 'tiku_paper_sr'
        }
    ]

    @property
    def aliases(self):
        return [i['alias'] for i in self.subjects]

subjects = Subjects()
