from typing import Optional

from fastapi import APIRouter, Query, Response, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates

from api import utils

router = APIRouter(prefix="/lucidus")
templates = Jinja2Templates(directory="templates")


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
