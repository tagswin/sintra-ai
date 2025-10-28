from fastapi import FastAPI
import uvicorn
import os

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/api/agents")
def agents():
    return {
        "agents": [
            {"id": "soshie", "name": "Soshie", "emoji": "📱", "role": "Social Media Manager"},
            {"id": "cassie", "name": "Cassie", "emoji": "🎧", "role": "Customer Support"},
            {"id": "seomi", "name": "Seomi", "emoji": "🔍", "role": "SEO Specialist"},
            {"id": "dexter", "name": "Dexter", "emoji": "📊", "role": "Data Analyst"},
            {"id": "buddy", "name": "Buddy", "emoji": "🤝", "role": "Project Manager"}
        ]
    }

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
