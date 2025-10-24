FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# FastAPI 레포 전체 복사 (서브모듈 포함)
COPY . .

# 만약 AI 레포가 setup.py가 있다면 로컬 설치 가능
# RUN pip install -e ./ai

# Python 경로에 ai 폴더 포함 (환경변수로 PYTHONPATH 설정)
ENV PYTHONPATH="${PYTHONPATH}:/app/ai"

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
