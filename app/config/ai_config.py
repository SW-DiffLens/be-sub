"""
AI 서브모듈 설정 및 Import 관리
"""
import sys
import os
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

# 프로젝트 루트 경로 계산
PROJECT_ROOT = Path(__file__).parent.parent.parent
AI_MODULE_PATH = PROJECT_ROOT / "ai"

# AI 모듈 경로를 sys.path에 추가
if str(AI_MODULE_PATH) not in sys.path:
    sys.path.insert(0, str(AI_MODULE_PATH))

# AI 모듈의 경로 설정을 override
# (메인 앱에서 실행할 때 경로 문제 해결)
os.environ['AI_MODULE_ROOT'] = str(AI_MODULE_PATH)


def get_ai_module_config():
    """AI 모듈의 DB 설정을 메인 앱 설정과 통합"""
    try:
        from src.config import DB_CONFIG as AI_DB_CONFIG
        return AI_DB_CONFIG
    except ImportError:
        # AI 모듈이 없으면 환경변수에서 직접 생성
        return {
            "host": os.getenv("DATABASE_URL", "localhost"),
            "port": int(os.getenv("DB_PORT", "5432")),
            "database": os.getenv("DATABASE_NAME", "postgres"),
            "user": os.getenv("DATABASE_USERNAME", "postgres"),
            "password": os.getenv("DATABASE_PASSWORD", ""),
        }


def check_ai_module_available() -> bool:
    """AI 모듈 사용 가능 여부 확인"""
    try:
        from src.query_parser import QueryParser
        return True
    except ImportError:
        return False


# 환경변수에서 DB 설정 읽기 (AI 모듈과 공유)
# 여러 환경변수 이름을 체크 (호환성)
DB_HOST = (
    os.getenv("DATABASE_URL") or 
    os.getenv("DB_HOST") or 
    (os.getenv("PSQL_URL") and os.getenv("PSQL_URL").replace("jdbc:postgresql://", "").split("/")[0].split(":")[0]) or
    "localhost"
)
DB_PORT = int(
    os.getenv("DB_PORT") or 
    (os.getenv("PSQL_URL") and os.getenv("PSQL_URL").split(":")[-1].split("/")[0] if ":" in os.getenv("PSQL_URL", "") else None) or
    "5432"
)
DB_NAME = (
    os.getenv("DATABASE_NAME") or 
    os.getenv("DB_NAME") or
    (os.getenv("PSQL_URL") and os.getenv("PSQL_URL").split("/")[-1] if "/" in os.getenv("PSQL_URL", "") else None) or
    "postgres"
)
DB_USER = (
    os.getenv("DATABASE_USERNAME") or 
    os.getenv("DB_USER") or
    os.getenv("PSQL_USERNAME") or
    "postgres"
)
DB_PASSWORD = (
    os.getenv("DATABASE_PASSWORD") or 
    os.getenv("DB_PASSWORD") or
    os.getenv("PSQL_PASSWORD") or
    ""
)

DB_CONFIG_FOR_AI = {
    "host": DB_HOST,
    "port": int(DB_PORT),
    "database": DB_NAME,
    "user": DB_USER,
    "password": DB_PASSWORD,
}

# AI 모듈 경로 export
__all__ = ['AI_MODULE_PATH', 'DB_CONFIG_FOR_AI', 'get_ai_module_config', 'check_ai_module_available']

