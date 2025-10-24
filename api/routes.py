"""
Routes de l'API REST
"""

import asyncio
import logging
from typing import Dict, Any, Optional
from datetime import datetime

from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel, Field

from core.specialized_agents import (
    SPECIALIZED_AGENTS, 
    get_best_agent, 
    list_all_agents
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api")

# Store pour les agents actifs (en production, utiliser Redis ou une vraie DB)
active_agents = {}
task_store = {}


class TaskRequest(BaseModel):
    """Requête de création de tâche"""
    description: str = Field(..., description="Description de la tâche à accomplir")
    context: Optional[Dict[str, Any]] = Field(None, description="Contexte additionnel")
    autonomous: bool = Field(True, description="Mode autonome activé")
    model: Optional[str] = Field(None, description="Modèle à utiliser")
    agent_id: Optional[str] = Field(None, description="ID de l'agent spécialisé (soshie, cassie, seomi, dexter, buddy, emmie, penn) - auto si null")


class TaskResponse(BaseModel):
    """Réponse de création de tâche"""
    task_id: str
    status: str
    created_at: str


class TaskStatusResponse(BaseModel):
    """Réponse de statut de tâche"""
    task_id: str
    status: str
    description: str
    created_at: str
    updated_at: str
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None


class AgentStatusResponse(BaseModel):
    """Réponse de statut de l'agent"""
    name: str
    model: str
    is_running: bool
    tasks_completed: int
    memory_size: Dict[str, int]
    current_task: Optional[Dict[str, Any]] = None


class ThinkRequest(BaseModel):
    """Requête de réflexion"""
    prompt: str = Field(..., description="Prompt pour faire réfléchir l'agent")
    context: Optional[Dict[str, Any]] = Field(None, description="Contexte additionnel")


@router.get("/")
async def root():
    """Point d'entrée de l'API"""
    return {
        "name": "Sintra AI API",
        "version": "1.0.0",
        "status": "operational",
        "endpoints": [
            "/api/agent/status",
            "/api/tasks",
            "/api/tasks/{task_id}",
            "/api/think",
            "/api/memory"
        ]
    }


@router.get("/agent/status", response_model=AgentStatusResponse)
async def get_agent_status():
    """Obtient le statut de l'agent"""
    from core import SintraAgent
    
    agent_id = "default"
    
    if agent_id not in active_agents:
        # Créer un agent par défaut
        import os
        from dotenv import load_dotenv
        load_dotenv()
        
        agent = SintraAgent(
            api_key=os.getenv("OPENAI_API_KEY"),
            anthropic_key=os.getenv("ANTHROPIC_API_KEY"),
            model=os.getenv("AGENT_MODEL", "gpt-4-turbo-preview")
        )
        active_agents[agent_id] = agent
    
    agent = active_agents[agent_id]
    status = agent.get_status()
    
    return AgentStatusResponse(**status)


@router.post("/tasks", response_model=TaskResponse)
async def create_task(request: TaskRequest, background_tasks: BackgroundTasks):
    """Crée une nouvelle tâche"""
    from core import SintraAgent
    import os
    from dotenv import load_dotenv
    load_dotenv()
    
    # Obtenir ou créer l'agent core
    agent_id = "default"
    if agent_id not in active_agents:
        agent = SintraAgent(
            api_key=os.getenv("OPENAI_API_KEY"),
            anthropic_key=os.getenv("ANTHROPIC_API_KEY"),
            model=request.model or os.getenv("AGENT_MODEL", "gpt-4-turbo-preview")
        )
        active_agents[agent_id] = agent
    else:
        agent = active_agents[agent_id]
    
    # Sélectionner l'agent spécialisé
    if request.agent_id and request.agent_id in SPECIALIZED_AGENTS:
        specialized_agent = SPECIALIZED_AGENTS[request.agent_id](agent)
        selected_agent_info = {
            "id": request.agent_id,
            "name": specialized_agent.name,
            "emoji": specialized_agent.emoji
        }
    else:
        # Auto-sélection du meilleur agent
        specialized_agent = get_best_agent(request.description, agent)
        selected_agent_info = {
            "id": "auto",
            "name": specialized_agent.name,
            "emoji": specialized_agent.emoji
        }
    
    # Créer l'ID de tâche
    task_id = f"task_{len(task_store) + 1}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    # Initialiser la tâche
    task_store[task_id] = {
        "id": task_id,
        "description": request.description,
        "context": request.context,
        "status": "pending",
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat(),
        "agent": selected_agent_info
    }
    
    # Lancer la tâche en arrière-plan
    background_tasks.add_task(execute_task_background_specialized, specialized_agent, task_id, request)
    
    logger.info(f"Tâche créée: {task_id} avec agent {selected_agent_info['name']}")
    
    return TaskResponse(
        task_id=task_id,
        status="pending",
        created_at=task_store[task_id]["created_at"]
    )


async def execute_task_background(agent, task_id: str, request: TaskRequest):
    """Exécute une tâche en arrière-plan"""
    try:
        task_store[task_id]["status"] = "running"
        task_store[task_id]["updated_at"] = datetime.now().isoformat()
        
        # Exécuter la tâche
        result = await agent.run_task(request.description, request.context)
        
        # Mettre à jour le store
        if result["success"]:
            task_store[task_id]["status"] = "completed"
            task_store[task_id]["result"] = result
        else:
            task_store[task_id]["status"] = "failed"
            task_store[task_id]["error"] = result.get("error")
        
        task_store[task_id]["updated_at"] = datetime.now().isoformat()
        
    except Exception as e:
        logger.error(f"Erreur lors de l'exécution de la tâche {task_id}: {str(e)}")
        task_store[task_id]["status"] = "failed"
        task_store[task_id]["error"] = str(e)
        task_store[task_id]["updated_at"] = datetime.now().isoformat()


async def execute_task_background_specialized(specialized_agent, task_id: str, request: TaskRequest):
    """Exécute une tâche avec un agent spécialisé en arrière-plan"""
    try:
        task_store[task_id]["status"] = "running"
        task_store[task_id]["updated_at"] = datetime.now().isoformat()
        
        # Exécuter la tâche avec l'agent spécialisé
        result = await specialized_agent.execute_task(request.description, request.context)
        
        # Mettre à jour le store
        if result["success"]:
            task_store[task_id]["status"] = "completed"
            task_store[task_id]["result"] = result
        else:
            task_store[task_id]["status"] = "failed"
            task_store[task_id]["error"] = result.get("error")
        
        task_store[task_id]["updated_at"] = datetime.now().isoformat()
        
    except Exception as e:
        logger.error(f"Erreur lors de l'exécution de la tâche {task_id}: {str(e)}")
        task_store[task_id]["status"] = "failed"
        task_store[task_id]["error"] = str(e)
        task_store[task_id]["updated_at"] = datetime.now().isoformat()


@router.get("/tasks/{task_id}", response_model=TaskStatusResponse)
async def get_task_status(task_id: str):
    """Obtient le statut d'une tâche"""
    if task_id not in task_store:
        raise HTTPException(status_code=404, detail="Tâche non trouvée")
    
    task = task_store[task_id]
    
    return TaskStatusResponse(
        task_id=task["id"],
        status=task["status"],
        description=task["description"],
        created_at=task["created_at"],
        updated_at=task["updated_at"],
        result=task.get("result"),
        error=task.get("error")
    )


@router.get("/tasks")
async def list_tasks():
    """Liste toutes les tâches"""
    return {
        "tasks": list(task_store.values()),
        "count": len(task_store)
    }


@router.post("/think")
async def think(request: ThinkRequest):
    """Fait réfléchir l'agent sur un prompt"""
    from core import SintraAgent
    import os
    from dotenv import load_dotenv
    load_dotenv()
    
    # Obtenir ou créer l'agent
    agent_id = "default"
    if agent_id not in active_agents:
        agent = SintraAgent(
            api_key=os.getenv("OPENAI_API_KEY"),
            anthropic_key=os.getenv("ANTHROPIC_API_KEY"),
            model=os.getenv("AGENT_MODEL", "gpt-4-turbo-preview")
        )
        active_agents[agent_id] = agent
    else:
        agent = active_agents[agent_id]
    
    try:
        response = await agent.think(request.prompt, request.context)
        
        return {
            "success": True,
            "prompt": request.prompt,
            "response": response
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/memory")
async def get_memory():
    """Obtient des informations sur la mémoire"""
    agent_id = "default"
    
    if agent_id not in active_agents:
        return {
            "error": "Aucun agent actif"
        }
    
    agent = active_agents[agent_id]
    
    return {
        "size": agent.memory.size(),
        "stats": agent.memory.memory_stats,
        "recent_memories": agent.memory.get_recent_memories(5)
    }


@router.get("/memory/search")
async def search_memory(query: str, limit: int = 5):
    """Recherche dans la mémoire"""
    agent_id = "default"
    
    if agent_id not in active_agents:
        raise HTTPException(status_code=404, detail="Aucun agent actif")
    
    agent = active_agents[agent_id]
    
    results = await agent.memory.retrieve_relevant(query, limit)
    
    return {
        "query": query,
        "results": results,
        "count": len(results)
    }


@router.post("/agent/reset")
async def reset_agent():
    """Réinitialise l'agent"""
    agent_id = "default"
    
    if agent_id in active_agents:
        agent = active_agents[agent_id]
        await agent.reset()
        
        return {
            "success": True,
            "message": "Agent réinitialisé"
        }
    
    return {
        "success": False,
        "message": "Aucun agent actif"
    }


@router.delete("/tasks/{task_id}")
async def delete_task(task_id: str):
    """Supprime une tâche"""
    if task_id not in task_store:
        raise HTTPException(status_code=404, detail="Tâche non trouvée")
    
    del task_store[task_id]
    
    return {
        "success": True,
        "message": f"Tâche {task_id} supprimée"
    }


@router.get("/agents")
async def get_agents():
    """Liste tous les agents spécialisés disponibles"""
    # Liste statique des agents sans nécessiter d'initialisation
    agents_info = []
    
    for agent_id, agent_class in SPECIALIZED_AGENTS.items():
        # Créer une instance temporaire juste pour obtenir les infos
        # Sans passer par le core agent complet
        temp_agent = agent_class(None)  # Passer None pour éviter l'init du core
        info = {
            "id": agent_id,
            "name": temp_agent.name,
            "emoji": temp_agent.emoji,
            "role": temp_agent.role,
            "description": temp_agent.description,
            "specialties": temp_agent.specialties,
            "personality_traits": temp_agent.personality_traits,
            "preferred_tools": temp_agent.preferred_tools,
            "task_count": temp_agent.task_count
        }
        agents_info.append(info)
    
    return {
        "agents": agents_info,
        "count": len(agents_info)
    }


@router.get("/agents/{agent_id}")
async def get_agent_info(agent_id: str):
    """Obtient les détails d'un agent spécialisé"""
    if agent_id not in SPECIALIZED_AGENTS:
        raise HTTPException(status_code=404, detail="Agent non trouvé")
    
    # Créer une instance temporaire sans le core agent
    agent_class = SPECIALIZED_AGENTS[agent_id]
    temp_agent = agent_class(None)
    
    info = {
        "id": agent_id,
        "name": temp_agent.name,
        "emoji": temp_agent.emoji,
        "role": temp_agent.role,
        "description": temp_agent.description,
        "specialties": temp_agent.specialties,
        "personality_traits": temp_agent.personality_traits,
        "preferred_tools": temp_agent.preferred_tools,
        "task_count": temp_agent.task_count
    }
    
    return info

