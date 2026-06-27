from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pathlib import Path
import time
from app.endpoint import summary
from app.core import get_logger

logger = get_logger(__name__)

app = FastAPI(
    title="Loan Approval API",
    description="ระบบประเมินสินเชื่อด้วย AI",
    version="1.0.0",
)

# [EDIT: CORS_ORIGINS] — เพิ่ม domain ที่อนุญาตให้เรียก API
ALLOWED_ORIGINS = [
    "http://localhost",
    "http://localhost:3000",
    "http://127.0.0.1",
    "http://127.0.0.1:5500",  # VS Code Live Server
    "http://localhost:8000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(summary.router)

@app.get("/")
async def root():
    return FileResponse(
        Path(__file__).parent.parent / "frontend" / "index.html"
    )
    
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start = time.perf_counter()

    response = await call_next(request)

    duration = time.perf_counter() - start
    logger.info(f"{request.method} {request.url.path} took {duration:.4f}s")

    return response