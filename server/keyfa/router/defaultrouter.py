from fastapi import APIRouter, Request, Header
from fastapi.responses import PlainTextResponse


import yaml
router = APIRouter(prefix="/keyfa", tags=["KEY FastAPI Default"])


@router.get("/health")
async def get_health() -> str:    
    return "ok"

@router.get("/openapi.yaml", response_class=PlainTextResponse)
async def get_opnapi_yaml(request: Request):
    openapi_json = request.app.openapi()
    openapi_yaml = yaml.dump(openapi_json)
    return openapi_yaml