"""
Sintra AI - Version ultra-minimaliste pour Railway
Point d'entrée le plus simple possible
"""

from fastapi import FastAPI
import uvicorn
import os

# Création de l'application FastAPI ultra-simple
app = FastAPI(title="Sintra AI")

# Endpoint de healthcheck ultra-simple
@app.get("/health")
def health_check():
    return {"status": "ok"}

# Endpoint racine ultra-simple
@app.get("/")
def root():
    return {"message": "Sintra AI Backend"}

# Endpoint agents ultra-simple
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
