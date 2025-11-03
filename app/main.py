from fastapi import FastAPI
from app.api.routes.search import router as search_router

# AI 모듈 라우터 추가
try:
    from src.api_recommendations import router as recommendations_router
    from src.cohort_comparison import router as cohort_comparison_router
    AI_ROUTERS_AVAILABLE = True
except ImportError as e:
    print(f"Warning: AI routers not available: {e}")
    recommendations_router = None
    cohort_comparison_router = None
    AI_ROUTERS_AVAILABLE = False

app = FastAPI(
    title="DiffLens FastAPI",
    description="AI 기반 패널 검색 및 분석 API",
    version="1.0.0"
)

# 기본 라우터
app.include_router(search_router)

# AI 모듈 라우터 (사용 가능한 경우)
if AI_ROUTERS_AVAILABLE:
    if recommendations_router:
        app.include_router(recommendations_router)
    if cohort_comparison_router:
        app.include_router(cohort_comparison_router)

@app.get("/")
def root():
    return {
        "message": "DiffLens FastAPI Server",
        "status": "running",
        "ai_module_available": AI_ROUTERS_AVAILABLE,
        "endpoints": {
            "search": "/search/natural",
            "recommendations": "/api/recommendations" if AI_ROUTERS_AVAILABLE else None,
            "cohort_comparison": "/api/cohort-comparison/compare" if AI_ROUTERS_AVAILABLE else None,
            "docs": "/docs"
        }
    }