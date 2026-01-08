from typing import Optional
from datetime import datetime
import json

from fastapi import APIRouter, Query, Response, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates

from api import utils

router = APIRouter(prefix="/lucidus")
templates = Jinja2Templates(directory="templates")
LOG_FILE = "usage.log"


def log_usage(version: str, theme: Optional[str] = None):
    with open(LOG_FILE, "a") as f:
        timestamp = datetime.utcnow().isoformat()
        log_entry = f"{timestamp},{version}"
        if theme:
            log_entry += f",{theme}"
        f.write(log_entry + "\n")


@router.get("/", response_class=HTMLResponse)
async def serve_template(request: Request):
    return templates.TemplateResponse("preview.html", {"request": request})


@router.get("/card_v1")
async def get_svg_v1(
        theme: Optional[str] = Query(default="",
                                     description="The theme name (optional)"),
        name: Optional[str] = Query(default=""),
        job: Optional[str] = Query(default=""),
        company: Optional[str] = Query(default=""),
        address: Optional[str] = Query(default=""),
        about: Optional[str] = Query(default=""),
        email: Optional[str] = Query(default="test@test.com"),
        linkedin: Optional[str] = Query(default=""),
        linkedin_color: Optional[str] = Query(default="#c37d16"),
):
    log_usage("v1", theme)
    data = {
        "theme": theme,
        "name": name,
        "job": job,
        "company": company,
        "address": address,
        "about": about,
        "email": email,
        "linkedin": linkedin,
        "linkedin_color": linkedin_color,
    }
    card_svg = utils.generate_card_v1(data=data)
    response = Response(content=card_svg, media_type="image/svg+xml")
    return response


@router.get("/card_v2")
async def get_svg_v2(
        name: Optional[str] = Query(default=""),
        job: Optional[str] = Query(default=""),
        company: Optional[str] = Query(default=""),
        address: Optional[str] = Query(default=""),
        about: Optional[str] = Query(default=""),
        github: Optional[str] = Query(default="https://www.github.com"),
        linkedin: Optional[str] = Query(default=""),
        linkedin_color: Optional[str] = Query(default="#c37d16"),
):
    log_usage("v2")
    data = {
        "name": name,
        "job": job,
        "company": company,
        "address": address,
        "about": about,
        "github": github,
        "linkedin": linkedin,
        "linkedin_color": linkedin_color,
    }
    card_svg = utils.generate_card_v2(data=data)
    response = Response(content=card_svg, media_type="image/svg+xml")
    return response


@router.get("/stats")
async def get_stats():
    try:
        with open(LOG_FILE, "r") as f:
            lines = f.readlines()
    except FileNotFoundError:
        return JSONResponse(content={"error": "Log file not found."}, status_code=404)

    total_requests = len(lines)
    v1_requests = 0
    v2_requests = 0
    theme_counts = {}

    for line in lines:
        parts = line.strip().split(",")
        if len(parts) >= 2:
            version = parts[1]
            if version == "v1":
                v1_requests += 1
                if len(parts) >= 3:
                    theme = parts[2]
                    theme_counts[theme] = theme_counts.get(theme, 0) + 1
            elif version == "v2":
                v2_requests += 1

    stats = {
        "total_requests": total_requests,
        "v1_requests": v1_requests,
        "v2_requests": v2_requests,
        "v1_themes": theme_counts,
    }

    return JSONResponse(content=stats)
