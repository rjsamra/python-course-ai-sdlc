from fastapi import FastAPI
from routers import flights
from database import init_db

app = FastAPI()

@app.on_event("startup")
def on_startup():
    init_db()

app.include_router(flights.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Flight API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
