"""
Sintra AI - Agent IA Autonome
Point d'entrée principal
"""

import asyncio
import logging
import os
from dotenv import load_dotenv

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from api.routes import router
from api.integrations_routes import router as integrations_router
from core import SintraAgent

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Charger les variables d'environnement
load_dotenv()

# Créer l'application FastAPI
app = FastAPI(
    title="Sintra AI",
    description="Agent IA Autonome avec capacités de planification et d'exécution",
    version="1.0.0"
)

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En production, spécifier les origines autorisées
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclure les routes de l'API
app.include_router(router)
app.include_router(integrations_router, prefix="/api")


@app.on_event("startup")
async def startup_event():
    """Actions au démarrage de l'application"""
    logger.info("🚀 Démarrage de Sintra AI...")
    logger.info(f"📍 API disponible sur http://{os.getenv('HOST', '0.0.0.0')}:{os.getenv('PORT', '8000')}")
    logger.info(f"📚 Documentation: http://{os.getenv('HOST', '0.0.0.0')}:{os.getenv('PORT', '8000')}/docs")
    
    # Vérifier les clés API
    if not os.getenv("OPENAI_API_KEY") and not os.getenv("ANTHROPIC_API_KEY"):
        logger.warning("⚠️  Aucune clé API configurée! Configurez OPENAI_API_KEY ou ANTHROPIC_API_KEY")


@app.on_event("shutdown")
async def shutdown_event():
    """Actions à l'arrêt de l'application"""
    logger.info("👋 Arrêt de Sintra AI...")


@app.get("/")
async def root():
    """Page d'accueil"""
    return {
        "name": "Sintra AI",
        "version": "1.0.0",
        "description": "Agent IA Autonome",
        "status": "operational",
        "api_docs": "/docs",
        "api_base": "/api"
    }


@app.get("/health")
async def health_check():
    """Point de contrôle de santé"""
    return {
        "status": "healthy",
        "service": "Sintra AI"
    }


async def demo_task():
    """
    Fonction de démonstration pour tester l'agent directement
    """
    logger.info("\n" + "="*60)
    logger.info("DÉMONSTRATION SINTRA AI")
    logger.info("="*60 + "\n")
    
    # Créer l'agent
    agent = SintraAgent(
        api_key=os.getenv("OPENAI_API_KEY"),
        anthropic_key=os.getenv("ANTHROPIC_API_KEY"),
        model=os.getenv("AGENT_MODEL", "gpt-4-turbo-preview")
    )
    
    # Tâche de test
    task_description = "Calcule 15 + 27, puis multiplie le résultat par 3"
    
    logger.info(f"Tâche: {task_description}\n")
    
    # Exécuter la tâche
    result = await agent.run_task(task_description)
    
    logger.info("\n" + "="*60)
    logger.info("RÉSULTAT")
    logger.info("="*60)
    logger.info(f"Succès: {result['success']}")
    
    if result['success']:
        logger.info(f"Résultat: {result['result']}")
        logger.info(f"Durée: {result['duration']:.2f}s")
    else:
        logger.error(f"Erreur: {result.get('error')}")
    
    logger.info("="*60 + "\n")


def main():
    """
    Point d'entrée principal
    """
    import sys
    
    # Vérifier les arguments
    if len(sys.argv) > 1 and sys.argv[1] == "demo":
        # Mode démonstration
        asyncio.run(demo_task())
    else:
        # Mode serveur
        host = os.getenv("HOST", "0.0.0.0")
        port = int(os.getenv("PORT", "8000"))
        debug = os.getenv("DEBUG", "False").lower() == "true"
        
        uvicorn.run(
            "main:app",
            host=host,
            port=port,
            reload=debug,
            log_level="info"
        )


if __name__ == "__main__":
    main()

