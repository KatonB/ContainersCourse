from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator
from api.shop_v1.routes import items, carts

app = FastAPI(title="Shop API")
Instrumentator().instrument(app).expose(app)

app.include_router(items.router, prefix="/item", tags=["items"])
app.include_router(carts.router, prefix="/cart", tags=["carts"])

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
