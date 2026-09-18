from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import analytics, auth, projects, sites

app = FastAPI(
    title="Darukaa.Earth API",
    version="1.0.0",
)

# CORS dependency
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(projects.router)
app.include_router(sites.router)
app.include_router(analytics.router)

@app.get("/")
def read_root():
    return {"message": "Darukaa.Earth API is running"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}
