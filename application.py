import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",   # ← เปลี่ยนเป็น "127.0.0.1" ใน Production
        port=8000,          # ← เปลี่ยน port ได้ที่นี่
        reload=True,        # ← ปิดใน Production (reload=False)
    )