from fastapi import FastAPI
from api import routes

app = FastAPI()

app.include_router(routes.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)
