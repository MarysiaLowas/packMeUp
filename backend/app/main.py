from fastapi import FastAPI
from fastapi_sqlalchemy import DBSessionMiddleware  # middleware helper
from fastapi_sqlalchemy import db
from backend import settings  # an object to provide global access to a database session


app = FastAPI()
app.add_middleware(DBSessionMiddleware, db_url=f"postgresql://{settings.POSTGRES_SERVER}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}")


@app.get("/")
async def root():
    return {"message": "Hello World"}
