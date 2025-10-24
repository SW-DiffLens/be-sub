from fastapi import FastAPI
from app.api.routes.search import router as search_router
from ai.scripts.test_prompts import main # ai 레포 함수 import 예시

app = FastAPI(title="DiffLens FastAPI")
app.include_router(search_router)

@app.get("/")
def root():
    result = main()  # AI 함수 호출 예시. 현재 ai.scripts.test_prompts의 main 함수는 콘솔 전용이라 오류 발생
    return {"hello fast api~!"}