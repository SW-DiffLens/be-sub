# DiffLens AI Server
https://github.com/user-attachments/assets/8916618c-9827-4a0d-8cb9-5339a6f3f6e3

DiffLens AI Server는 LLM 기반 지능형 패널 검색 및 분석 서비스입니다.

## Preview
<img width="4760" height="6736" alt="image" src="https://github.com/user-attachments/assets/7cd8899e-e107-4f6d-83f8-244018cc2da2" />

### Members

<table width="50%" align="center">
    <tr>
        <td align="center"><b>LEAD/BE</b></td>
        <td align="center"><b>FE</b></td>
        <td align="center"><b>FE/DE</b></td>
        <td align="center"><b>BE</b></td>
        <td align="center"><b>AI/DATA</b></td>
    </tr>
    <tr>
        <td align="center"><img src="https://github.com/user-attachments/assets/561672fc-71f6-49d3-b826-da55d6ace0c4" /></td>
        <td align="center"><img src="https://github.com/user-attachments/assets/b95eea07-c69a-4bbf-9a8f-eccda41c410e" /></td>
        <td align="center"><img src="https://github.com/user-attachments/assets/15ac4334-9325-48f1-9cf6-0485f9cf130f"></td>
        <td align="center"><img src="https://github.com/user-attachments/assets/2572fa94-b981-46c6-9731-10c977267e16" /></td>
        <td align="center"><img src="https://github.com/user-attachments/assets/197a24c6-853c-4d63-b026-44032b27a5f1" /></td>
    </tr>
    <tr>
        <td align="center"><b><a href="https://github.com/hardwoong">박세웅</a></b></td>
        <td align="center"><b><a href="https://github.com/nyun-nye">윤예진</a></b></td>
        <td align="center"><b><a href="https://github.com/hyesngy">윤혜성</a></b></td>
        <td align="center"><b><a href="https://github.com/ggamnunq">김준용</a></b></td> 
        <td align="center"><b><a href="https://github.com/hoya04">신정호</a></b></td> 
    </tr>
</table>

## Tech Stack

- **Python 3.11** - 런타임
- **FastAPI** - 웹 프레임워크
- **LangChain** - LLM 프레임워크
- **Anthropic Claude** - LLM (Haiku, Sonnet)
- **Upstage Embedding** - 벡터 임베딩
- **PostgreSQL + pgvector** - 데이터베이스
- **SQLAlchemy + asyncpg** - ORM (비동기)
- **Docker** - 컨테이너

## Getting Started

### Installation

```bash
# 저장소 클론 (서브모듈 포함)
git clone --recurse-submodules https://github.com/SW-DiffLens/be-sub.git
cd be-sub

# 가상환경 생성 및 활성화
python -m venv venv
source venv/bin/activate

# 의존성 설치
pip install -r requirements.txt
pip install -r ai/requirements.txt
```

### Environment Variables

```env
# LLM API Keys
ANTHROPIC_API_KEY=sk-ant-api03-xxx
UPSTAGE_API_KEY=up_xxx

# Database
DATABASE_URL=localhost
DATABASE_USERNAME=postgres
DATABASE_PASSWORD=your_password
DATABASE_NAME=panel_search
DB_PORT=5432
```

### Run

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Docker

```bash
# 이미지 빌드
docker build -t difflens-ai .

# 컨테이너 실행
docker run -p 8000:8000 --env-file .env difflens-ai
```

## Project Structure

```
be-sub/
├── app/
│   └── main.py              # AI 서브모듈 로더
├── ai/                      # AI 서브모듈 (git submodule)
│   ├── main.py              # FastAPI 앱 엔트리포인트
│   ├── src/
│   │   ├── api/             # API 라우터 및 스키마
│   │   ├── services/        # 비즈니스 로직
│   │   ├── repositories/    # 데이터 접근 계층
│   │   ├── llm/             # LLM 통합 모듈
│   │   ├── domain/          # 도메인 모델
│   │   ├── core/            # 설정 및 유틸리티
│   │   └── utils/           # 상수 정의
│   └── prompts/             # LLM 프롬프트 템플릿
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── start.sh
```

## Key Features

- **자연어 쿼리 파싱**: LLM을 활용한 자연어 → 구조화된 필터 변환
- **하이브리드 검색**: 필터 검색 + 벡터 유사도 검색 조합
- **지능형 차트 추천**: 데이터 특성에 맞는 최적의 시각화 차트 자동 선택
- **개인화 추천**: 업종/회원 검색 이력 기반 맞춤형 패널 추천
- **집단 비교 분석**: 두 코호트 간 통계적 차이 분석 및 AI 인사이트 생성
- **프로필 생성**: 패널 메타데이터 기반 자연어 프로필 및 해시태그 자동 생성

## API Endpoints

### Search API (`/api/search`)

- `POST /api/search/` - 자연어/필터 기반 패널 검색
- `POST /api/search/search-result/{search_id}/refine` - 검색 결과 필터 추가
- `GET /api/search/search-result/{search_id}/info` - 검색 결과 상세 조회

### Recommendations API (`/api/quick-search`)

- `POST /api/quick-search/recommendations` - 업종 기반 패널 추천
- `POST /api/quick-search/recommendations/by-member` - 회원 검색 이력 기반 추천

### Comparison API (`/api/cohort-comparison`)

- `POST /api/cohort-comparison/compare` - 두 코호트 비교 분석
- `GET /api/cohort-comparison/metrics` - 비교 가능한 메트릭 목록

## API Documentation

서버 실행 후 아래 URL에서 확인:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## License

이 프로젝트는 한성대학교 기업연계 SW캡스톤디자인 수업에서 진행되었습니다.
