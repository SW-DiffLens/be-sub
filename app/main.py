from fastapi import FastAPI
from app.api.routes.search import router as search_router

app = FastAPI(title="DiffLens FastAPI")
app.include_router(search_router)

@app.get("/")
def root():
    return {"hello fast api~!"}