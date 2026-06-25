from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pathlib import Path
from app.endpoint import summary
# =============================================================
# [EDIT: APP_CONFIG] — ตั้งค่าแอปพลิเคชัน
# =============================================================
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
    "*",  # ⚠️ ลบออกใน Production
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