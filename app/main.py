from fastapi import FastAPI
from app.api import auth, organisations, users
from app.db.session import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth.router)
app.include_router(organisations.router)
app.include_router(users.router)
