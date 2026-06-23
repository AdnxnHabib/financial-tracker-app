from fastapi import FastAPI

from app.routes.accounts import router as accounts_router
from app.routes.categories import router as categories_router
from app.routes.transactions import router as transactions_router


def create_app() -> FastAPI:
    app = FastAPI(
        title="Financial Tracker API",
        version="0.1.0",
        description="Backend API for the personal finance tracker.",
    )

    @app.get("/", tags=["system"])
    def root():
        return {
            "name": "Financial Tracker API",
            "version": app.version,
            "status": "ok",
        }

    @app.get("/health", tags=["system"])
    def health_check():
        return {"status": "ok"}

    app.include_router(accounts_router)
    app.include_router(categories_router)
    app.include_router(transactions_router)

    return app


app = create_app()
