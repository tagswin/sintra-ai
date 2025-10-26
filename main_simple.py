"""
Sintra AI - Version simplifiée pour Railway
Point d'entrée principal sans dépendances lourdes
"""

import logging
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Création de l'application FastAPI
app = FastAPI(
    title="Sintra AI",
    description="Agent IA Autonome - Version Railway",
    version="1.0.0"
)

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Endpoint de healthcheck pour Railway
@app.get("/health")
async def health_check():
    """Endpoint de healthcheck pour Railway"""
    return {
        "status": "healthy", 
        "message": "Sintra AI is running",
        "version": "1.0.0"
    }

# Endpoint racine
@app.get("/")
async def root():
    """Endpoint racine"""
    return {"message": "Sintra AI Backend is running!", "status": "ok"}

# Endpoint agents simplifié
@app.get("/api/agents")
async def get_agents():
    """Retourne la liste des agents"""
    agents = [
        {
            "id": "soshie",
            "name": "Soshie",
            "emoji": "📱",
            "role": "Social Media Manager",
            "description": "Expert en médias sociaux, création de contenu et engagement communautaire",
            "specialties": ["Création de posts", "Stratégie de contenu", "Analyse des tendances"],
            "personality_traits": ["Créative et tendance", "Connaît les dernières trends"],
            "task_count": 0
        },
        {
            "id": "cassie",
            "name": "Cassie",
            "emoji": "🎧",
            "role": "Customer Support",
            "description": "Spécialiste du support client et de la satisfaction utilisateur",
            "specialties": ["Résolution de problèmes", "Communication", "Analyse des tickets"],
            "personality_traits": ["Empathique et patiente", "Excellente communicatrice"],
            "task_count": 0
        },
        {
            "id": "seomi",
            "name": "Seomi",
            "emoji": "🔍",
            "role": "SEO Specialist",
            "description": "Experte en optimisation pour les moteurs de recherche",
            "specialties": ["Recherche de mots-clés", "Optimisation technique", "Analyse de concurrence"],
            "personality_traits": ["Analytique et méthodique", "Orientée résultats"],
            "task_count": 0
        },
        {
            "id": "dexter",
            "name": "Dexter",
            "emoji": "📊",
            "role": "Data Analyst",
            "description": "Analyste de données et expert en intelligence business",
            "specialties": ["Analyse statistique", "Visualisation de données", "Rapports d'insights"],
            "personality_traits": ["Logique et précis", "Orienté données"],
            "task_count": 0
        },
        {
            "id": "buddy",
            "name": "Buddy",
            "emoji": "🤝",
            "role": "Project Manager",
            "description": "Gestionnaire de projet et coordinateur d'équipe",
            "specialties": ["Planification", "Coordination", "Suivi de projets"],
            "personality_traits": ["Organisé et motivant", "Excellent leader"],
            "task_count": 0
        }
    ]
    
    return {"agents": agents}

# Endpoint agent individuel
@app.get("/api/agents/{agent_id}")
async def get_agent(agent_id: str):
    """Retourne les détails d'un agent spécifique"""
    agents_data = {
        "soshie": {
            "id": "soshie",
            "name": "Soshie",
            "emoji": "📱",
            "role": "Social Media Manager",
            "description": "Expert en médias sociaux, création de contenu et engagement communautaire",
            "specialties": ["Création de posts", "Stratégie de contenu", "Analyse des tendances"],
            "personality_traits": ["Créative et tendance", "Connaît les dernières trends"],
            "task_count": 0,
            "tools": ["Instagram API", "Facebook API", "Twitter API", "Analytics"],
            "integrations": ["Instagram", "Facebook", "Twitter", "Google Analytics"]
        },
        "cassie": {
            "id": "cassie",
            "name": "Cassie",
            "emoji": "🎧",
            "role": "Customer Support",
            "description": "Spécialiste du support client et de la satisfaction utilisateur",
            "specialties": ["Résolution de problèmes", "Communication", "Analyse des tickets"],
            "personality_traits": ["Empathique et patiente", "Excellente communicatrice"],
            "task_count": 0,
            "tools": ["Zendesk", "Intercom", "Freshdesk", "LiveChat"],
            "integrations": ["Zendesk", "Intercom", "Freshdesk", "Slack"]
        },
        "seomi": {
            "id": "seomi",
            "name": "Seomi",
            "emoji": "🔍",
            "role": "SEO Specialist",
            "description": "Experte en optimisation pour les moteurs de recherche",
            "specialties": ["Recherche de mots-clés", "Optimisation technique", "Analyse de concurrence"],
            "personality_traits": ["Analytique et méthodique", "Orientée résultats"],
            "task_count": 0,
            "tools": ["Google Search Console", "SEMrush", "Ahrefs", "Screaming Frog"],
            "integrations": ["Google Search Console", "SEMrush", "Ahrefs", "Google Analytics"]
        },
        "dexter": {
            "id": "dexter",
            "name": "Dexter",
            "emoji": "📊",
            "role": "Data Analyst",
            "description": "Analyste de données et expert en intelligence business",
            "specialties": ["Analyse statistique", "Visualisation de données", "Rapports d'insights"],
            "personality_traits": ["Logique et précis", "Orienté données"],
            "task_count": 0,
            "tools": ["Python", "R", "Tableau", "Power BI"],
            "integrations": ["Google Analytics", "Mixpanel", "Amplitude", "Snowflake"]
        },
        "buddy": {
            "id": "buddy",
            "name": "Buddy",
            "emoji": "🤝",
            "role": "Project Manager",
            "description": "Gestionnaire de projet et coordinateur d'équipe",
            "specialties": ["Planification", "Coordination", "Suivi de projets"],
            "personality_traits": ["Organisé et motivant", "Excellent leader"],
            "task_count": 0,
            "tools": ["Jira", "Asana", "Trello", "Monday.com"],
            "integrations": ["Jira", "Asana", "Trello", "Slack"]
        }
    }
    
    if agent_id not in agents_data:
        return {"error": "Agent not found"}
    
    return agents_data[agent_id]

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    host = os.environ.get("HOST", "0.0.0.0")
    
    logger.info(f"🚀 Démarrage de Sintra AI...")
    logger.info(f"📍 API disponible sur http://{host}:{port}")
    logger.info(f"📚 Documentation: http://{host}:{port}/docs")
    
    uvicorn.run(app, host=host, port=port, log_level="info")
