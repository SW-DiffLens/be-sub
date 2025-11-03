FROM python:3.11-slim

WORKDIR /app

# psycopg2 빌드를 위한 시스템 패키지 설치
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# FastAPI 레포 전체 복사 (서브모듈 포함)
COPY . .

# AI 레포 requirements 설치
RUN pip install --no-cache-dir -r ./ai/requirements.txt

# Python 경로 설정 (app 모듈과 ai 모듈 모두 포함)
ENV PYTHONPATH="/app:/app/ai"

# AI 모듈 루트 경로 설정 (프롬프트 파일 경로 해결)
ENV AI_MODULE_ROOT="/app/ai"

EXPOSE 8000

# 시작 스크립트 실행 권한 부여
RUN chmod +x /app/start.sh

# 시작 스크립트를 사용하여 실행 (환경변수와 디버깅 정보 포함)
CMD ["/app/start.sh"]
