from fastapi import FastAPI
import uvicorn
import os

app = FastAPI(title="Sintra AI")

@app.get("/")
def root():
    return {"message": "Sintra AI Backend", "status": "ok"}

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.get("/api/agents")
def get_agents():
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
