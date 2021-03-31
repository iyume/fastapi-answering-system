from typing import Any
import asyncio
from datetime import datetime

from app.api import userfunc, apifunc

async def read_exams(username: str) -> Any:
    myexams = await userfunc.read_exams(username)
    myexams = sorted(myexams, key=lambda k:k['start_time'], reverse=True)
    processing_exam_entry_coroutines = []
    processing_exam_entry_index = []
    for exam in myexams:
        if exam['exam_status'] == 1:
            processing_exam_entry_coroutines.append(
                apifunc.exam_paper_get_first_not_picked(
                    username,
                    exam['exam_tag']
                )
            )
            processing_exam_entry_index.append(myexams.index(exam))
        start_time = datetime.fromisoformat(exam['start_time'])
        end_time = datetime.fromisoformat(exam['end_time'])
        exam['start_time'] = exam['start_time'].replace('T', ' ')
        exam['end_time'] = exam['end_time'].replace('T', ' ')
        if timenow := datetime.now():
            if start_time < timenow < end_time:
                exam['opening_status'] = '进行中'
            elif timenow > end_time:
                exam['opening_status'] = '已结束'
            else:
                exam['opening_status'] = '未开始'
    processing_exam_entry_coroutines_results = await asyncio.gather(
        *processing_exam_entry_coroutines
    )
    for i, e in zip(
        processing_exam_entry_index,
        processing_exam_entry_coroutines_results
    ):
        # TODO strict zip in python3.10
        myexams[i]['exam_entry_num'] = e.get('question_order', 1) if e else 1
    return myexams

