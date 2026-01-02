from fastapi import FastAPI

app = FastAPI(title="Simple FastAPI App")

@app.get("/")
def read_root():
    return {"message": "Hello FastAPI From fix branch for ci demo1 🚀"}

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/items/{item_id}")
def get_item(item_id: int, q: str |  None = None):
    return {
        "item_id": item_id,
        "query": q
    }
