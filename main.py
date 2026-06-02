from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from api import routes


class CachedStaticFiles(StaticFiles):
    """StaticFiles with a Cache-Control header so CSS/JS are served from the
    CDN/browser cache and don't hit the (possibly sleeping) origin."""

    def file_response(self, *args, **kwargs):
        response = super().file_response(*args, **kwargs)
        response.headers["Cache-Control"] = "public, max-age=86400"
        return response


app = FastAPI()
BASE_DIR = Path(__file__).resolve().parent
app.mount("/static", CachedStaticFiles(directory=str(BASE_DIR / "static")),
          name="static")

app.include_router(routes.router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=5000)
