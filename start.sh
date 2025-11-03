#!/bin/bash
set -e

# 환경변수 설정
export PYTHONPATH="/app:/app/ai"
export AI_MODULE_ROOT="/app/ai"

# uvicorn 실행
exec python -m uvicorn app.main:app --host 0.0.0.0 --port 8000

