# DiffLens AI Server

<div align="center">

![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.120.0-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-0.3.x-1C3C3C?style=for-the-badge&logo=langchain&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-pgvector-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)

**LLM 기반 지능형 패널 검색 및 분석 AI 서버**

[Architecture](#architecture) · [API Endpoints](#api-endpoints) · [Getting Started](#getting-started) · [Deployment](#deployment)

</div>

---

## Overview

DiffLens AI Server는 LLM(Large Language Model)을 활용한 지능형 패널 검색 및 분석 서비스입니다. 메인 서버([be-main](https://github.com/SW-DiffLens/be-main))와 연동하여 자연어 쿼리 파싱, 시맨틱 검색, 개인화 추천, 집단 비교 분석 기능을 제공합니다.

### 주요 기능

| 기능                    | 설명                                                   |
| ----------------------- | ------------------------------------------------------ |
| 🗣️ **자연어 쿼리 파싱** | LLM을 활용한 자연어 → 구조화된 필터 자동 변환          |
| 🔍 **하이브리드 검색**  | 필터 기반 검색 + 벡터 유사도 검색 조합                 |
| 📊 **지능형 차트 추천** | 데이터 특성에 맞는 최적의 시각화 차트 자동 선택        |
| 🎯 **개인화 추천**      | 업종/회원 검색 이력 기반 맞춤형 패널 추천              |
| ⚖️ **집단 비교 분석** | 두 코호트 간 통계적 차이 분석 및 AI 인사이트 생성      |
| 📝 **프로필 생성**      | 패널 메타데이터 기반 자연어 프로필 및 해시태그 자동 생성 |

---

## Architecture

### System Architecture
<img src="https://private-user-images.githubusercontent.com/158552165/520499397-1549a73c-79fa-4c2f-9219-5c0901411178.png?jwt=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3NjQ1MTczMTEsIm5iZiI6MTc2NDUxNzAxMSwicGF0aCI6Ii8xNTg1NTIxNjUvNTIwNDk5Mzk3LTE1NDlhNzNjLTc5ZmEtNGMyZi05MjE5LTVjMDkwMTQxMTE3OC5wbmc_WC1BbXotQWxnb3JpdGhtPUFXUzQtSE1BQy1TSEEyNTYmWC1BbXotQ3JlZGVudGlhbD1BS0lBVkNPRFlMU0E1M1BRSzRaQSUyRjIwMjUxMTMwJTJGdXMtZWFzdC0xJTJGczMlMkZhd3M0X3JlcXVlc3QmWC1BbXotRGF0ZT0yMDI1MTEzMFQxNTM2NTFaJlgtQW16LUV4cGlyZXM9MzAwJlgtQW16LVNpZ25hdHVyZT01NGU0NDYxODlhZGYyMzk0OTVhNDUwODBlNjAzOTg0ZDEwZWRmODMwMmRhOTZiZDkwZmRmMmYxNzZhYWIwZjQ5JlgtQW16LVNpZ25lZEhlYWRlcnM9aG9zdCJ9.T-glm0nPzE03LhF7GjeLQU72zftqxflp55m0Jd_Gjhc">

### Project Structure

```
be-sub/
├── app/
│   ├── __init__.py
│   └── main.py                      # AI 서브모듈 로더
│
├── ai/                              # AI 서브모듈 (git submodule)
│   ├── main.py                      # FastAPI 앱 엔트리포인트
│   │
│   ├── src/
│   │   ├── api/                     # API Layer
│   │   │   ├── routes/              # FastAPI 라우터
│   │   │   │   ├── search.py        # 검색 API
│   │   │   │   ├── recommendations.py  # 추천 API
│   │   │   │   └── comparison.py    # 비교 분석 API
│   │   │   └── schemas/             # Request/Response DTO
│   │   │       ├── search.py
│   │   │       ├── recommendation.py
│   │   │       └── comparison.py
│   │   │
│   │   ├── services/                # Business Logic Layer
│   │   │   ├── search_service.py    # 검색 비즈니스 로직
│   │   │   ├── recommendation_service.py  # 추천 로직
│   │   │   └── comparison_service.py     # 비교 분석 로직
│   │   │
│   │   ├── repositories/            # Data Access Layer
│   │   │   ├── panel_repository.py  # 패널 데이터 접근
│   │   │   ├── search_history_repository.py  # 검색 이력
│   │   │   └── library_repository.py  # 라이브러리 데이터
│   │   │
│   │   ├── llm/                     # LLM Integration Layer
│   │   │   ├── client.py            # LLM 클라이언트 팩토리
│   │   │   ├── query_parser.py      # 자연어 쿼리 파싱
│   │   │   ├── chart_decider.py     # 차트 추천 로직
│   │   │   ├── insight_generator.py # 인사이트 생성
│   │   │   ├── embeddings.py        # 임베딩 서비스
│   │   │   └── profile_generator.py # 프로필/해시태그 생성
│   │   │
│   │   ├── domain/                  # Domain Models
│   │   │   ├── enums.py             # 열거형 정의
│   │   │   ├── models.py            # 도메인 모델
│   │   │   └── schemas.py           # LLM 출력 스키마
│   │   │
│   │   ├── core/                    # Core Utilities
│   │   │   ├── config.py            # 환경 설정
│   │   │   ├── database.py          # DB 커넥션 풀
│   │   │   └── exceptions.py        # 커스텀 예외
│   │   │
│   │   └── utils/                   # Utilities
│   │       └── constants.py         # 상수 정의
│   │
│   └── prompts/                     # LLM Prompt Templates
│       ├── parse_query.md           # 쿼리 파싱 프롬프트
│       ├── decide_main_chart.md     # 차트 결정 프롬프트
│       ├── analyze_cohort_insights.md  # 코호트 인사이트 프롬프트
│       ├── extract_patterns.md      # 패턴 추출 프롬프트
│       ├── generate_personalized_recommendations.md  # 추천 프롬프트
│       ├── generate_profile.md      # 프로필 생성 프롬프트
│       └── generate_hashtags.md     # 해시태그 생성 프롬프트
│
├── Dockerfile                       # Docker 이미지 빌드
├── docker-compose.yml               # 컨테이너 구성
├── requirements.txt                 # Python 의존성
├── start.sh                         # 서버 시작 스크립트
└── README.md                        # 프로젝트 문서
```

---

## Tech Stack

| Category      | Technology                         |
| ------------- | ---------------------------------- |
| **Language**  | Python 3.11                        |
| **Framework** | FastAPI 0.120.0                    |
| **LLM**       | Anthropic Claude (Haiku, Sonnet)   |
| **Embedding** | Upstage Embedding API              |
| **LLM Framework** | LangChain 0.3.x                |
| **Database**  | PostgreSQL + pgvector              |
| **ORM**       | SQLAlchemy 2.0 + asyncpg (async)   |
| **Container** | Docker                             |
| **Cloud**     | AWS ECR                            |

### LLM Models

| Model              | Usage                              | Provider  |
| ------------------ | ---------------------------------- | --------- |
| `claude-3-5-haiku` | 쿼리 파싱, 프로필/해시태그 생성    | Anthropic |
| `claude-sonnet-4-5` | 인사이트 생성, 복잡한 분석         | Anthropic |
| `embedding-query`  | 시맨틱 검색용 벡터 임베딩          | Upstage   |

---

## API Endpoints

### 🔍 Search API (`/api/search`)

| Method | Endpoint                                       | Description                |
| ------ | ---------------------------------------------- | -------------------------- |
| `POST` | `/api/search/`                                 | 자연어/필터 기반 패널 검색 |
| `POST` | `/api/search/search-result/{search_id}/refine` | 검색 결과 필터 추가        |
| `GET`  | `/api/search/search-result/{search_id}/info`   | 검색 결과 상세 조회        |
| `GET`  | `/api/search/available-filters`                | 사용 가능한 필터 목록      |

---

### 🎯 Recommendations API (`/api/quick-search`)

| Method | Endpoint                                      | Description              |
| ------ | --------------------------------------------- | ------------------------ |
| `POST` | `/api/quick-search/recommendations`           | 업종 기반 패널 추천      |
| `POST` | `/api/quick-search/recommendations/by-member` | 회원 검색 이력 기반 추천 |
| `GET`  | `/api/quick-search/health`                    | 추천 서비스 상태 확인    |

---

### ⚖️ Comparison API (`/api/cohort-comparison`)

| Method | Endpoint                         | Description             |
| ------ | -------------------------------- | ----------------------- |
| `POST` | `/api/cohort-comparison/compare` | 두 코호트 비교 분석     |
| `GET`  | `/api/cohort-comparison/metrics` | 비교 가능한 메트릭 목록 |

---

## LLM Pipeline

### Query Parsing Flow

```
┌──────────────┐      ┌──────────────┐      ┌──────────────────────┐
│  User Query  │ ──▶  │ QueryParser  │ ──▶  │  Structured Filters  │
│  "30대 여성" │      │    (LLM)     │      │ {age: "30대",        │
└──────────────┘      └──────────────┘      │  gender: "여성"}     │
                                            └──────────────────────┘
```

### Search Flow

```
┌─────────┐     ┌─────────────┐     ┌───────────────┐     ┌──────────┐
│  Query  │ ──▶ │ QueryParser │ ──▶ │ SearchService │ ──▶ │  Result  │
└─────────┘     └─────────────┘     └───────┬───────┘     └──────────┘
                                            │
                      ┌─────────────────────┼─────────────────────┐
                      ▼                     ▼                     ▼
               ┌────────────┐       ┌────────────┐       ┌────────────┐
               │   Filter   │       │   Vector   │       │   Chart    │
               │   Search   │       │   Search   │       │  Decider   │
               │   (SQL)    │       │ (Embedding)│       │   (LLM)    │
               └────────────┘       └────────────┘       └────────────┘
```

---

## Getting Started

### Prerequisites

- **Python 3.11+**
- **Docker** & **Docker Compose**
- **PostgreSQL 14+** with pgvector extension
- **AWS CLI** (ECR 배포 시)

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

### Installation & Running

```bash
# 1. 저장소 클론 (서브모듈 포함)
git clone --recurse-submodules https://github.com/SW-DiffLens/be-sub.git
cd be-sub

# 2. 서브모듈 초기화 (이미 클론한 경우)
git submodule init
git submodule update

# 3. 가상환경 생성 및 활성화
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 4. 의존성 설치
pip install -r requirements.txt
pip install -r ai/requirements.txt

# 5. 환경 변수 설정
cp .env.example .env
# .env 파일 수정

# 6. 개발 서버 실행
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### API Documentation

서버 실행 후 아래 URL에서 API 문서를 확인할 수 있습니다:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## Deployment

### Docker Build & Run

```bash
# 1. Docker 이미지 빌드
docker build -t difflens-ai .

# 2. 컨테이너 실행
docker run -p 8000:8000 --env-file .env difflens-ai

# 3. docker-compose 사용
docker-compose up -d
```

### AWS ECR Deployment

```bash
# 1. ECR 로그인
aws ecr get-login-password --region ap-northeast-2 | \
  docker login --username AWS --password-stdin <your-ecr-uri>

# 2. 멀티 아키텍처 빌드 (ARM64 → AMD64)
docker buildx build --platform linux/amd64 -t difflens-ai .

# 3. 이미지 태그 및 푸시
docker tag difflens-ai:latest <your-ecr-uri>:latest
docker push <your-ecr-uri>:latest
```

---

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

---

## Related Repositories

| Repository                                          | Description                           |
| --------------------------------------------------- | ------------------------------------- |
| [be-main](https://github.com/SW-DiffLens/be-main)   | 메인 서버 (Spring Boot, JWT 인증)     |
| [fe](https://github.com/SW-DiffLens/fe)             | 프론트엔드 (React, TypeScript, Vite)  |

---

## License

This project is proprietary software. All rights reserved.

---

<div align="center">

**DiffLens** - Data-driven Panel Analysis Platform

</div>
