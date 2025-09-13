# from app.routes import tessaract_ocrRoute
# from app.routes import easy_ocrRoute
from app.routes import aspire_ocrRoute
from fastapi import FastAPI
from app.routes import health

def create_app() -> FastAPI:
    app = FastAPI(
        title="BillBot Backend",
        description="AI-powered bill processing system",
        version="1.0.0"
    )

    # Register routes
    app.include_router(health.router)
    app.include_router(aspire_ocrRoute.router)
    # app.include_router(easy_ocrRoute.router)
    # app.include_router(tessaract_ocrRoute.router)

    return app

app = create_app()
