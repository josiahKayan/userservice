from fastapi import FastAPI
from api.database.database import database,engine
from api.model import models
from api.routers import userrouter

app = FastAPI()

app.include_router(userrouter.router)

def create_tables():
    models.Base.metadata.create_all(bind=engine)

@app.on_event("startup")
async def startup():
    # Create tables if they don't exist
    create_tables()
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host='0.0.0.0', port=8001, reload=True)


