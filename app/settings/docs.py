from fastapi import APIRouter
from fastapi.openapi.docs import get_swagger_ui_html

router = APIRouter()


@router.get("/docs", include_in_schema=False)
async def swagger_ui_html():
    """
    Return swagger API document
    """
    return get_swagger_ui_html(
        openapi_url="/openapi.json",
        title="HeroAPI",
        swagger_favicon_url="static/favicon.png",
    )
