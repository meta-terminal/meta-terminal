from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, Base
from .api.v1 import auth, terminal, ai, files, system, upgrade
from .core.auth_handler import get_current_user

# ایجاد جداول پایگاه داده
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Meta-Terminal Backend",
    description="هسته اصلی ابرمتاترمینال — خودارتقاعی، چندزبانه، چندهوش",
    version="2.0.0"
)

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # TODO: تغییر به دامنه واقعی
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# اضافه کردن روترها
app.include_router(auth.router, prefix="/api/v1", tags=["auth"])
app.include_router(terminal.router, prefix="/api/v1", tags=["terminal"], dependencies=[Depends(get_current_user)])
app.include_router(ai.router, prefix="/api/v1", tags=["ai"], dependencies=[Depends(get_current_user)])
app.include_router(files.router, prefix="/api/v1", tags=["files"], dependencies=[Depends(get_current_user)])
app.include_router(system.router, prefix="/api/v1", tags=["system"], dependencies=[Depends(get_current_user)])
app.include_router(upgrade.router, prefix="/api/v1", tags=["upgrade"], dependencies=[Depends(get_current_user)])

@app.get("/")
def read_root():
    return {"message": "Meta-Terminal Backend v2.0.0 is running!", "docs": "/docs"}

@app.get("/health")
def health_check():
    return {"status": "ok", "service": "backend"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
