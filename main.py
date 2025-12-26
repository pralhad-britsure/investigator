from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from src.models.user import Base
from src.database import engine
from src.api.auth import router as auth_router
from src.api.master import router as master_router
from src.api.user_management import router as user_management_router

app = FastAPI()

Base.metadata.create_all(bind=engine)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(auth_router, prefix="/api/user", tags=["User"])
app.include_router(master_router, prefix="/api", tags=["Master Data"])
app.include_router(user_management_router, prefix="/api/users", tags=["User Management"])


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=6000, reload=True)
