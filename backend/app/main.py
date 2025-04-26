from fastapi import FastAPI
from fastapi_sqlalchemy import AsyncDBSessionMiddleware
from app import settings  # an object to provide global access to a database session


app = FastAPI()
app.add_middleware(
    AsyncDBSessionMiddleware, 
    db_url=settings.POSTGRES_URL
    )


@app.get("/")
async def root():
    return {"message": "Hello World"}
