from fastapi import FastAPI

app = FastAPI(title="Simple FastAPI App")

@app.get("/")
def read_root():
    return {"message": "Hi! FastAPI From feature branch for fastapi-demoapp 1 🚀"}

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/items/{item_id}")
def get_item(item_id: int, q: str |  None = None):
    return {
        "item_id": item_id,
        "query": q
    }
