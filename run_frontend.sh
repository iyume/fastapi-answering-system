#!/bin/bash
source ~/.virtualenvs/fastapi/bin/activate
cd frontend && uvicorn app.main:app --host=0.0.0.0 --port=9090
