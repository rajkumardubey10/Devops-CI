from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI(title="Simple FastAPI App")

# -------------------------
# HTML Home Page
# -------------------------
@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>FastAPI CI Demo </title>
        <style>
            body {
                margin: 0;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea, #764ba2);
                height: 100vh;
                display: flex;
                justify-content: center;
                align-items: center;
                color: #fff;
            }
            .card {
                background: rgba(255, 255, 255, 0.15);
                padding: 40px;
                border-radius: 16px;
                width: 420px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.3);
                text-align: center;
                backdrop-filter: blur(10px);
            }
            h1 {
                margin-bottom: 10px;
                font-size: 32px;
            }
            p {
                font-size: 16px;
                opacity: 0.9;
            }
            .endpoints {
                margin-top: 25px;
                text-align: left;
            }
            .endpoints code {
                display: block;
                background: rgba(0,0,0,0.3);
                padding: 10px;
                border-radius: 8px;
                margin-bottom: 10px;
                color: #00ffcc;
                font-size: 14px;
            }
            footer {
                margin-top: 20px;
                font-size: 13px;
                opacity: 0.8;
            }
        </style>
    </head>
    <body>
        <div class="card">
            <h1>🚀 FastAPI CI Demo with private secured docker Image and running from Kubernetes  </h1>
            <p>Hello FastAPI from <b>fix branch</b> for CI demo</p>

            <div class="endpoints">
                <h3>Available Endpoints</h3>
                <code>GET /health</code>
                <code>GET /items/{item_id}?q=value</code>
                <code>GET /docs</code>
            </div>

            <footer>
                Built with ❤️ using FastAPI
            </footer>
        </div>
    </body>
    </html>
    """

# -------------------------
# Health Check
# -------------------------
@app.get("/health")
def health_check():
    return {"status": "ok"}

# -------------------------
# Items API
# -------------------------
@app.get("/items/{item_id}")
def get_item(item_id: int, q: str | None = None):
    return {
        "item_id": item_id,
        "query": q
    }


