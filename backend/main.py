from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/performance")
async def get_performance():
    return {"data": [80, 75, 85, 78, 90, 88, 92, 95, 89, 93, 96, 94]}

@app.get("/api/stats")
async def get_stats():
    return {"total": 785200, "efficiency": 58000, "quality": 92000}