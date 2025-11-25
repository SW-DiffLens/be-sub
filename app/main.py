"""
메인 FastAPI 앱 - AI 서브모듈의 app.py를 직접 사용
"""
import sys
import os
from pathlib import Path

# AI 모듈 경로를 sys.path에 추가
PROJECT_ROOT = Path(__file__).parent.parent
AI_MODULE_PATH = PROJECT_ROOT / "ai"
if str(AI_MODULE_PATH) not in sys.path:
    sys.path.insert(0, str(AI_MODULE_PATH))

# AI_MODULE_ROOT 환경변수 설정 (ai/app.py에서 사용)
os.environ['AI_MODULE_ROOT'] = str(AI_MODULE_PATH)

# AI 모듈의 app 인스턴스를 import
try:
    # ai/app.py를 모듈로 import
    # PYTHONPATH에 ai 경로가 있으므로 'app' 모듈로 import 가능
    # 하지만 ai/app.py이므로 직접 import하기 위해 importlib 사용
    import importlib.util
    app_py_path = AI_MODULE_PATH / "app.py"
    spec = importlib.util.spec_from_file_location("ai_app", app_py_path)
    ai_app_module = importlib.util.module_from_spec(spec)
    
    # ai/app.py 실행 시 필요한 환경 설정
    # ai/app.py는 src 모듈을 import하므로 src 경로가 필요
    spec.loader.exec_module(ai_app_module)
    app = ai_app_module.app
    
    print("✓ AI 서브모듈의 app.py를 성공적으로 로드했습니다")
    
except Exception as e:
    print(f"✗ Warning: Failed to import AI app: {e}")
    import traceback
    traceback.print_exc()
    
    # 폴백: 기본 FastAPI 앱 생성
    from fastapi import FastAPI
    app = FastAPI(
        title="DiffLens FastAPI (Fallback)",
        description="AI 모듈을 로드할 수 없습니다",
        version="1.0.0"
    )

    @app.get("/")
    def root():
        return {
            "error": "AI module not available",
            "message": str(e)
        }

# 메인 레포의 추가 엔드포인트 (메트릭 등)
@app.get("/metrics")
def metrics():
    """헬스 체크 및 메트릭 엔드포인트"""
    return {
        "status": "ok",
        "service": "difflens-fastapi",
        "version": "1.0.0"
    }