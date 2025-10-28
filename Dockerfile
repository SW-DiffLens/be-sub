FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# FastAPI 레포 전체 복사 (서브모듈 포함)
COPY . .

# AI 레포 requirements 설치
RUN pip install --no-cache-dir -r ./ai/requirements.txt

# Python 경로에 ai 폴더 포함
ENV PYTHONPATH="${PYTHONPATH}:/app/ai"

EXPOSE 8000

# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
