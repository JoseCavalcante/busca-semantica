from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse

from api.queryrouter import router as api_query_router
from api.ingestrouter import router as api_ingest_router
from api.authenticationrouter import router as api_authentication_router 
from api.jobrouter import router as api_job_router
from api.historyrouter import router as api_history_router
from api.assistenterouter import router as api_assistente_router

from fastapi.middleware.cors import CORSMiddleware

import os
from dotenv import load_dotenv

app = FastAPI()
load_dotenv()

#configurações de CORS
def get_cors_origins():

    origins = os.getenv('CORS_ORIGINS')

    if origins:
        return [origins.strip() for origin in origins.split(',')]

    return []


app.add_middleware(
    CORSMiddleware,
    allow_origins = get_cors_origins(),
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"]
)

#app.include_router(api_index_router)
#app.include_router(api_embedding_router)
#app.include_router(api_extractPDF_router)
#app.include_router(api_upsert_router)

app.include_router(api_query_router)
app.include_router(api_ingest_router)
app.include_router(api_authentication_router)
app.include_router(api_job_router)
app.include_router(api_history_router)
app.include_router(api_assistente_router)

print("--- Job Router Included ---")
print("--- Authentication Router Included ---")

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def root():
    return RedirectResponse(url="/static/login.html")


