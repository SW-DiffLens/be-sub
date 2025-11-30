"""
DiffLens FastAPI 서버 - AI 서브모듈 통합
AI 서브모듈(ai/)의 FastAPI 앱을 로드하여 실행합니다.
"""
import sys
import os
from pathlib import Path

# AI 모듈 경로 설정
PROJECT_ROOT = Path(__file__).parent.parent
AI_MODULE_PATH = PROJECT_ROOT / "ai"

# sys.path에 AI 모듈 경로 추가
if str(AI_MODULE_PATH) not in sys.path:
    sys.path.insert(0, str(AI_MODULE_PATH))

# 환경변수 설정
os.environ['AI_MODULE_ROOT'] = str(AI_MODULE_PATH)

# AI 서브모듈의 FastAPI 앱 import
try:
    # ai/main.py의 app 인스턴스 import
    import importlib.util
    main_py_path = AI_MODULE_PATH / "main.py"
    spec = importlib.util.spec_from_file_location("ai_main", main_py_path)
    ai_main_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(ai_main_module)
    app = ai_main_module.app
    
    print("✓ AI 서브모듈 로드 완료")
    
except Exception as e:
    print(f"✗ AI 서브모듈 로드 실패: {e}")
    import traceback
    traceback.print_exc()
    
    # Fallback: 기본 FastAPI 앱
    from fastapi import FastAPI
    app = FastAPI(
        title="DiffLens FastAPI (Fallback)",
        description="AI 서브모듈을 로드할 수 없습니다",
        version="1.0.0"
    )
    
    @app.get("/")
    def root():
        return {
            "status": "fallback",
            "error": "AI module not available",
            "message": str(e)
        }


# 추가 엔드포인트
@app.get("/metrics")
def metrics():
    """헬스 체크 및 메트릭"""
    return {
        "status": "ok",
        "service": "difflens-fastapi",
        "version": "1.0.0"
    }
