from fastapi import FastAPI
from scalar_fastapi import get_scalar_api_reference
from contextlib import asynccontextmanager
from app.db.session import create_db_tables
from app.api.router import master_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("server started..")
    await create_db_tables()
    yield
    print("server stopped..")
    pass

app = FastAPI(
    title="FastAPI Auth System",
    description="JWT + Email Verification API",
    version="1.0.0",
    lifespan=lifespan
)

app.include_router(master_router)

@app.get("/")
def root():
    return {"message": "API is Working."}


# Scalar API Documentation
@app.get("/scalar", include_in_schema=False)
def get_scalar_docs():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title="Scalar API",
    )