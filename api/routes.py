from fastapi import APIRouter, Query, Response
from api import utils

router = APIRouter(prefix="/lucidus")


@router.get("/card_v1")
async def get_svg():
  card_svg = utils.generate_card()
  response = Response(content=card_svg, media_type="image/svg+xml")
  return response
