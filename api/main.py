import asyncio

import uvicorn
from beanie import init_beanie
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from motor.motor_asyncio import AsyncIOMotorClient

from api.config import get_settings
from api.models.catalog import DatasetMetadataDOC
from api.models.user import Submission, User
from api.routes.catalog import router as catalog_router
from api.routes.discovery import router as discovery_router

# had to use load_dotenv() to get the env variables to work during testing
load_dotenv()
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_db_client():
    settings = get_settings()
    app.mongodb_client = AsyncIOMotorClient(settings.db_connection_string)
    app.mongodb = app.mongodb_client[settings.database_name]
    await init_beanie(database=app.mongodb, document_models=[DatasetMetadataDOC, User, Submission])


@app.on_event("shutdown")
async def shutdown_db_client():
    app.mongodb_client.close()


@app.get("/")
async def health_check():
    return JSONResponse(status_code=200, content={"status": "healthy"})


app.include_router(catalog_router, tags=["Dataset"], prefix="/api/catalog")
app.include_router(discovery_router, tags=["Discovery"], prefix="/api/discovery")

app.mount("/api/schemas", StaticFiles(directory="api/models/schemas"), name="schemas")

openapi_schema = get_openapi(
    title="I-GUIDE Catalog API",
    version="1.0",
    description="Standardized interface with validation for managing catalog",
    routes=app.routes,
)
app.openapi_schema = openapi_schema


class Server(uvicorn.Server):
    def handle_exit(self, sig: int, frame) -> None:
        return super().handle_exit(sig, frame)


async def main():
    """Run FastAPI"""

    server = Server(config=uvicorn.Config(app, workers=1, loop="asyncio", host="0.0.0.0", port=8000))
    api = asyncio.create_task(server.serve())

    await asyncio.wait([api])


if __name__ == "__main__":
    asyncio.run(main())
