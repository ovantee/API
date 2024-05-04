from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.api.main import router as api_router
from app.settings import Settings

settings = Settings.parse_obj({})
app = FastAPI(title="AIDE_Mulbery_API")

app.include_router(api_router, prefix="/api")

@app.get("/", include_in_schema=False)
async def health() -> JSONResponse:
    return JSONResponse({"message": "It worked!!"})
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)