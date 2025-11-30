# DiffLens FastAPI Server

AI 서브모듈을 통합하여 패널 검색 API를 제공하는 FastAPI 서버

## Overview

이 레포지토리는 [Panel Search AI](./ai) 서브모듈을 Docker 컨테이너로 패키징하고 배포하기 위한 래퍼 서버입니다. AI 서브모듈의 FastAPI 앱을 로드하여 자연어 기반 패널 검색, 개인화 추천, 코호트 비교 분석 기능을 제공합니다.

### 주요 기능

- **자연어 패널 검색**: LLM을 활용한 자연어 쿼리 → 구조화된 필터 변환
- **하이브리드 검색**: 필터 검색 + 벡터 유사도 검색 조합
- **개인화 추천**: 업종/회원 이력 기반 맞춤형 패널 추천
- **코호트 비교 분석**: 두 코호트 간 통계적 차이 분석 및 인사이트 생성
- **지능형 차트 추천**: 데이터 특성에 맞는 최적의 시각화 차트 자동 선택

## Architecture

```
be-sub/
├── app/
│   ├── __init__.py
│   └── main.py              # AI 서브모듈 로더
├── ai/                      # AI 서브모듈 (git submodule)
│   ├── main.py              # FastAPI 앱 엔트리포인트
│   ├── src/                 # AI 비즈니스 로직
│   │   ├── api/             # API 라우터
│   │   ├── services/        # 비즈니스 서비스
│   │   ├── repositories/    # 데이터 접근 계층
│   │   ├── llm/             # LLM 통합 모듈
│   │   ├── domain/          # 도메인 모델
│   │   └── core/            # 핵심 유틸리티
│   └── prompts/             # LLM 프롬프트 템플릿
├── Dockerfile               # Docker 이미지 빌드
├── docker-compose.yml       # 컨테이너 구성
├── requirements.txt         # Python 의존성
└── start.sh                 # 서버 시작 스크립트
```

## Tech Stack

| Category  | Technology                       |
| --------- | -------------------------------- |
| Framework | FastAPI 0.120.0                  |
| Runtime   | Python 3.11                      |
| LLM       | Anthropic Claude (Haiku, Sonnet) |
| Embedding | Upstage Embedding API            |
| Database  | PostgreSQL + pgvector            |
| Container | Docker                           |
| Cloud     | AWS ECR                          |

## API Endpoints

### Search API (`/api/search`)

| Method | Endpoint                                       | Description                |
| ------ | ---------------------------------------------- | -------------------------- |
| POST   | `/api/search/`                                 | 자연어/필터 기반 패널 검색 |
| POST   | `/api/search/search-result/{search_id}/refine` | 검색 결과 필터 추가        |
| GET    | `/api/search/search-result/{search_id}/info`   | 검색 결과 상세 조회        |
| GET    | `/api/search/available-filters`                | 사용 가능한 필터 목록      |

### Recommendations API (`/api/quick-search`)

| Method | Endpoint                                      | Description              |
| ------ | --------------------------------------------- | ------------------------ |
| POST   | `/api/quick-search/recommendations`           | 업종 기반 패널 추천      |
| POST   | `/api/quick-search/recommendations/by-member` | 회원 검색 이력 기반 추천 |
| GET    | `/api/quick-search/health`                    | 추천 서비스 상태 확인    |

### Comparison API (`/api/cohort-comparison`)

| Method | Endpoint                         | Description             |
| ------ | -------------------------------- | ----------------------- |
| POST   | `/api/cohort-comparison/compare` | 두 코호트 비교 분석     |
| GET    | `/api/cohort-comparison/metrics` | 비교 가능한 메트릭 목록 |

## Installation

### Prerequisites

- Python 3.11+
- Docker & Docker Compose
- PostgreSQL 14+ with pgvector extension
- AWS CLI (ECR 배포 시)

### Setup

```bash
# 저장소 클론 (서브모듈 포함)
git clone --recurse-submodules https://github.com/SW-DiffLens/be-sub.git
cd be-sub

# 서브모듈 초기화 (이미 클론한 경우)
git submodule init
git submodule update

# 가상환경 생성 및 활성화
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 의존성 설치
pip install -r requirements.txt
pip install -r ai/requirements.txt

# 환경 변수 설정
cp .env.example .env
# .env 파일 수정
```

### Environment Variables

```env
# LLM API Keys
ANTHROPIC_API_KEY=sk-ant-api03-xxx
UPSTAGE_API_KEY=up_xxx

# Database (PostgreSQL + pgvector)
DATABASE_URL=localhost
DATABASE_USERNAME=postgres
DATABASE_PASSWORD=your_password
DATABASE_NAME=panel_search
DB_PORT=5432
```

## Usage

### 로컬 개발

```bash
# 개발 모드 실행
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 또는
python -m uvicorn app.main:app --reload
```

### Docker 실행

```bash
# 이미지 빌드
docker build -t difflens-fastapi .

# 컨테이너 실행
docker run -p 8000:8000 --env-file .env difflens-fastapi

# docker-compose 사용
docker-compose up -d
```

### API 문서

서버 실행 후 아래 URL에서 API 문서 확인:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Deployment

### AWS ECR 배포

```bash
# 1. AWS ECR 로그인
aws ecr get-login-password --region ap-northeast-2 | \
  docker login --username AWS --password-stdin <your-ecr-uri>

# 2. Docker 이미지 빌드 (ARM64 환경에서 AMD64 빌드 시)
docker buildx build --platform linux/amd64 -t difflens-fastapi .

# 3. 이미지 태그
docker tag difflens-fastapi:latest <your-ecr-uri>:latest

# 4. ECR 푸시
docker push <your-ecr-uri>:latest
```

## Submodule Management

### 서브모듈 업데이트

```bash
# 서브모듈 최신화
git submodule update --remote

# 변경사항 커밋
git add ai
git commit -m "chore: AI 서브모듈 업데이트"
git push
```

### 서브모듈 초기화 (새로 클론 시)

```bash
git submodule init
git submodule update
```

## Project Structure

```
.
├── app/
│   ├── __init__.py          # 패키지 초기화
│   └── main.py              # FastAPI 앱 로더
├── ai/                      # AI 서브모듈 (git submodule)
├── Dockerfile               # Docker 빌드 설정
├── docker-compose.yml       # Docker Compose 설정
├── requirements.txt         # 메인 의존성
├── start.sh                 # 컨테이너 시작 스크립트
└── README.md                # 프로젝트 문서
```

## License

This project is proprietary software. All rights reserved.
