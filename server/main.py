import asyncio
from functools import lru_cache
from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session
from lib.watcher import ppomppu
from datetime import datetime

import models
import schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


app = FastAPI()


class BackgroundPostWatcher:
    def __init__(self):
        self.db = SessionLocal()

    async def run_main(self):
        while True:
            await asyncio.sleep(60 - datetime.now().second)
            await ppomppu(self.db)


watcher = BackgroundPostWatcher()


@app.on_event("startup")
async def app_startup():
    asyncio.create_task(watcher.run_main())


@app.get("/", response_model=list[schemas.Posts])
async def root(db: Session = Depends(get_db)):
    posts = db.query(models.Posts).all()
    return posts
