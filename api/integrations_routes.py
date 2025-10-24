"""
Routes API pour gérer les intégrations des agents
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
from core.specialized_agents import SPECIALIZED_AGENTS

router = APIRouter(prefix="/integrations", tags=["integrations"])


class IntegrationCredentials(BaseModel):
    credentials: Dict[str, Any]


@router.get("/{agent_id}")
async def get_agent_integrations(agent_id: str):
    """Liste toutes les intégrations disponibles pour un agent"""
    if agent_id not in SPECIALIZED_AGENTS:
        raise HTTPException(status_code=404, detail="Agent non trouvé")
    
    # Créer une instance temporaire pour obtenir les intégrations
    agent_class = SPECIALIZED_AGENTS[agent_id]
    temp_agent = agent_class(None)
    
    integrations_info = []
    for integration in temp_agent.integrations:
        integrations_info.append({
            "id": integration.name.lower().replace(" ", "_"),
            "name": integration.name,
            "icon": integration.icon,
            "description": integration.description,
            "status": integration.status.value,
            "is_configured": bool(integration.credentials),
            "required_credentials": integration.get_required_credentials()
        })
    
    return {
        "agent_id": agent_id,
        "agent_name": temp_agent.name,
        "integrations": integrations_info
    }


@router.get("/{agent_id}/{integration_id}")
async def get_integration_details(agent_id: str, integration_id: str):
    """Obtient les détails d'une intégration spécifique"""
    if agent_id not in SPECIALIZED_AGENTS:
        raise HTTPException(status_code=404, detail="Agent non trouvé")
    
    agent_class = SPECIALIZED_AGENTS[agent_id]
    temp_agent = agent_class(None)
    
    # Trouver l'intégration
    integration = None
    for integ in temp_agent.integrations:
        if integ.name.lower().replace(" ", "_") == integration_id:
            integration = integ
            break
    
    if not integration:
        raise HTTPException(status_code=404, detail="Intégration non trouvée")
    
    return {
        "id": integration_id,
        "name": integration.name,
        "icon": integration.icon,
        "description": integration.description,
        "status": integration.status.value,
        "is_configured": bool(integration.credentials),
        "required_credentials": integration.get_required_credentials(),
        "last_sync": integration.last_sync.isoformat() if integration.last_sync else None,
        "error_message": integration.error_message
    }


@router.post("/{agent_id}/{integration_id}/configure")
async def configure_integration(
    agent_id: str, 
    integration_id: str, 
    credentials: IntegrationCredentials
):
    """Configure une intégration avec les credentials"""
    if agent_id not in SPECIALIZED_AGENTS:
        raise HTTPException(status_code=404, detail="Agent non trouvé")
    
    agent_class = SPECIALIZED_AGENTS[agent_id]
    temp_agent = agent_class(None)
    
    # Trouver l'intégration
    integration = None
    for integ in temp_agent.integrations:
        if integ.name.lower().replace(" ", "_") == integration_id:
            integration = integ
            break
    
    if not integration:
        raise HTTPException(status_code=404, detail="Intégration non trouvée")
    
    # Configurer l'intégration
    success = integration.configure(credentials.credentials)
    
    if not success:
        raise HTTPException(status_code=400, detail="Configuration échouée")
    
    return {
        "success": True,
        "message": f"{integration.name} configuré avec succès",
        "status": integration.status.value
    }


@router.post("/{agent_id}/{integration_id}/connect")
async def connect_integration(agent_id: str, integration_id: str):
    """Connecte une intégration (teste la connexion)"""
    if agent_id not in SPECIALIZED_AGENTS:
        raise HTTPException(status_code=404, detail="Agent non trouvé")
    
    agent_class = SPECIALIZED_AGENTS[agent_id]
    temp_agent = agent_class(None)
    
    # Trouver l'intégration
    integration = None
    for integ in temp_agent.integrations:
        if integ.name.lower().replace(" ", "_") == integration_id:
            integration = integ
            break
    
    if not integration:
        raise HTTPException(status_code=404, detail="Intégration non trouvée")
    
    # Tester la connexion
    result = await integration.test_connection()
    
    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["message"])
    
    return result


@router.post("/{agent_id}/{integration_id}/disconnect")
async def disconnect_integration(agent_id: str, integration_id: str):
    """Déconnecte une intégration"""
    if agent_id not in SPECIALIZED_AGENTS:
        raise HTTPException(status_code=404, detail="Agent non trouvé")
    
    agent_class = SPECIALIZED_AGENTS[agent_id]
    temp_agent = agent_class(None)
    
    # Trouver l'intégration
    integration = None
    for integ in temp_agent.integrations:
        if integ.name.lower().replace(" ", "_") == integration_id:
            integration = integ
            break
    
    if not integration:
        raise HTTPException(status_code=404, detail="Intégration non trouvée")
    
    # Déconnecter
    success = await integration.disconnect()
    
    return {
        "success": success,
        "message": f"{integration.name} déconnecté",
        "status": integration.status.value
    }


@router.get("/")
async def list_all_integrations():
    """Liste toutes les intégrations disponibles pour tous les agents"""
    all_integrations = {}
    
    for agent_id, agent_class in SPECIALIZED_AGENTS.items():
        temp_agent = agent_class(None)
        integrations = [
            {
                "id": integ.name.lower().replace(" ", "_"),
                "name": integ.name,
                "icon": integ.icon,
                "description": integ.description
            }
            for integ in temp_agent.integrations
        ]
        all_integrations[agent_id] = {
            "agent_name": temp_agent.name,
            "agent_emoji": temp_agent.emoji,
            "integrations": integrations
        }
    
    return all_integrations

