from fastapi import APIRouter, Query, Response
from api import utils
from typing import Optional

router = APIRouter(prefix="/lucidus")


@router.get("/card_v1")
async def get_svg(
        theme: Optional[str] = Query(default="", description="The theme name (optional)"),
        name: Optional[str] = Query(default=""),
        job: Optional[str] = Query(default=""),
        company: Optional[str] = Query(default=""),
        address: Optional[str] = Query(default=""),
        about: Optional[str] = Query(default=""),
        email: Optional[str] = Query(default="test@test.com"),
        linkedin: Optional[str] = Query(default=""),
):
    data = {
        "theme": theme,
        "name": name,
        "job": job,
        "company": company,
        "address": address,
        "about": about,
        "email": email,
        "linkedin": linkedin
    }
    card_svg = utils.generate_card(data)
    response = Response(content=card_svg, media_type="image/svg+xml")
    return response
