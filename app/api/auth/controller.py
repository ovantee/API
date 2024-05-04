from fastapi import APIRouter, Depends, Path, Request
from fastapi.responses import JSONResponse

from app.settings import Settings
from app.auth.JWT import JWT
from pydantic import BaseModel

class Token(BaseModel):
    token: str

class Payload(BaseModel):
    client_name: str
    secret_key: str



settings = Settings.parse_obj({})
router = APIRouter(prefix="/authentication")

@router.post("/generation-token", include_in_schema=False)
async def generation_token(body: Payload) -> JSONResponse:
    request = body.dict()
    client_name = request['client_name']
    secret_key = request['secret_key']
    params = {
        "client_name": client_name
    }

    token = JWT.create_access_token(params, secret_key, settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return JSONResponse({"message": "Generation Token", "data": token})