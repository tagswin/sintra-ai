"""
Agent IA Autonome Principal
"""

import asyncio
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
import json

from openai import AsyncOpenAI
from anthropic import AsyncAnthropic

from .planner import TaskPlanner
from .memory import MemorySystem
from .executor import TaskExecutor
from tools import ToolRegistry

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SintraAgent:
    """
    Agent IA autonome capable de planifier et exécuter des tâches complexes
    """
    
    def __init__(
        self,
        name: str = "Sintra",
        model: str = "gpt-4-turbo-preview",
        api_key: Optional[str] = None,
        anthropic_key: Optional[str] = None,
        max_iterations: int = 50,
        temperature: float = 0.7
    ):
        self.name = name
        self.model = model
        self.max_iterations = max_iterations
        self.temperature = temperature
        
        # Initialisation des clients API
        self.openai_client = AsyncOpenAI(api_key=api_key) if api_key else None
        self.anthropic_client = AsyncAnthropic(api_key=anthropic_key) if anthropic_key else None
        
        # Initialisation des composants
        self.planner = TaskPlanner(self)
        self.memory = MemorySystem()
        self.executor = TaskExecutor(self)
        self.tool_registry = ToolRegistry()
        
        # État de l'agent
        self.current_task = None
        self.task_history = []
        self.is_running = False
        
        logger.info(f"Agent {self.name} initialisé avec le modèle {self.model}")
    
    async def run_task(self, task_description: str, context: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Exécute une tâche de manière autonome
        
        Args:
            task_description: Description de la tâche à accomplir
            context: Contexte additionnel pour la tâche
            
        Returns:
            Résultat de l'exécution de la tâche
        """
        if self.is_running:
            raise RuntimeError("L'agent est déjà en cours d'exécution d'une tâche")
        
        self.is_running = True
        self.current_task = {
            "description": task_description,
            "context": context or {},
            "start_time": datetime.now(),
            "status": "running"
        }
        
        try:
            logger.info(f"🚀 Démarrage de la tâche: {task_description}")
            
            # Étape 1: Planification
            logger.info("📋 Phase de planification...")
            plan = await self.planner.create_plan(task_description, context)
            self.current_task["plan"] = plan
            
            # Étape 2: Exécution
            logger.info(f"⚙️  Exécution du plan ({len(plan['steps'])} étapes)...")
            results = await self.executor.execute_plan(plan)
            
            # Étape 3: Synthèse
            logger.info("📊 Synthèse des résultats...")
            final_result = await self._synthesize_results(task_description, results)
            
            # Sauvegarder dans la mémoire
            await self.memory.store_task(task_description, plan, results, final_result)
            
            self.current_task["status"] = "completed"
            self.current_task["end_time"] = datetime.now()
            self.current_task["result"] = final_result
            self.task_history.append(self.current_task)
            
            logger.info("✅ Tâche complétée avec succès!")
            
            return {
                "success": True,
                "result": final_result,
                "plan": plan,
                "execution_results": results,
                "duration": (self.current_task["end_time"] - self.current_task["start_time"]).total_seconds()
            }
            
        except Exception as e:
            logger.error(f"❌ Erreur lors de l'exécution: {str(e)}")
            self.current_task["status"] = "failed"
            self.current_task["error"] = str(e)
            self.current_task["end_time"] = datetime.now()
            
            return {
                "success": False,
                "error": str(e),
                "task": self.current_task
            }
        finally:
            self.is_running = False
            self.current_task = None
    
    async def think(self, prompt: str, context: Optional[Dict] = None) -> str:
        """
        Fait réfléchir l'agent avec un prompt donné
        
        Args:
            prompt: Le prompt à envoyer au modèle
            context: Contexte additionnel
            
        Returns:
            La réponse du modèle
        """
        # Récupérer la mémoire pertinente
        relevant_memories = await self.memory.retrieve_relevant(prompt, limit=5)
        
        # Construire le prompt avec contexte
        full_prompt = self._build_prompt(prompt, context, relevant_memories)
        
        # Envoyer au modèle approprié
        if self.model.startswith("gpt"):
            return await self._openai_completion(full_prompt)
        elif self.model.startswith("claude"):
            return await self._anthropic_completion(full_prompt)
        else:
            raise ValueError(f"Modèle non supporté: {self.model}")
    
    def _build_prompt(
        self,
        prompt: str,
        context: Optional[Dict],
        memories: List[Dict]
    ) -> str:
        """Construit le prompt complet avec contexte et mémoires"""
        
        system_prompt = f"""Tu es {self.name}, un agent IA autonome sophistiqué.

Tes capacités:
- Planification et décomposition de tâches complexes
- Raisonnement logique et résolution de problèmes
- Utilisation d'outils (recherche web, exécution de code, etc.)
- Apprentissage et adaptation

Outils disponibles:
{self._format_available_tools()}

Principes:
1. Décompose les tâches complexes en étapes simples
2. Vérifie toujours tes résultats
3. Apprends de tes expériences passées
4. Sois précis et méthodique
"""
        
        context_section = ""
        if context:
            context_section = f"\n\nContexte actuel:\n{json.dumps(context, indent=2)}"
        
        memory_section = ""
        if memories:
            memory_section = "\n\nExpériences pertinentes:\n"
            for mem in memories:
                memory_section += f"- {mem['description']}\n"
        
        return f"{system_prompt}{context_section}{memory_section}\n\nTâche:\n{prompt}"
    
    def _format_available_tools(self) -> str:
        """Formate la liste des outils disponibles"""
        tools = self.tool_registry.list_tools()
        return "\n".join([f"- {tool['name']}: {tool['description']}" for tool in tools])
    
    async def _openai_completion(self, prompt: str) -> str:
        """Obtient une complétion via OpenAI"""
        if not self.openai_client:
            raise ValueError("Client OpenAI non initialisé")
        
        response = await self.openai_client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "Tu es Sintra, un agent IA autonome."},
                {"role": "user", "content": prompt}
            ],
            temperature=self.temperature,
            max_tokens=4000
        )
        
        return response.choices[0].message.content
    
    async def _anthropic_completion(self, prompt: str) -> str:
        """Obtient une complétion via Anthropic"""
        if not self.anthropic_client:
            raise ValueError("Client Anthropic non initialisé")
        
        response = await self.anthropic_client.messages.create(
            model=self.model,
            max_tokens=4000,
            temperature=self.temperature,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        return response.content[0].text
    
    async def _synthesize_results(
        self,
        task_description: str,
        execution_results: List[Dict]
    ) -> Dict[str, Any]:
        """
        Synthétise les résultats d'exécution en une réponse finale
        """
        synthesis_prompt = f"""Tâche originale: {task_description}

Résultats d'exécution:
{json.dumps(execution_results, indent=2)}

Synthétise ces résultats en une réponse claire et complète.
Format de réponse (JSON):
{{
    "summary": "Résumé de ce qui a été accompli",
    "key_findings": ["Point clé 1", "Point clé 2"],
    "data": {{}},  // Données structurées pertinentes
    "next_steps": ["Recommandation 1", "Recommandation 2"]
}}
"""
        
        response = await self.think(synthesis_prompt)
        
        try:
            # Tenter de parser en JSON
            return json.loads(response)
        except:
            # Si échec, retourner en format texte
            return {
                "summary": response,
                "raw_results": execution_results
            }
    
    def get_status(self) -> Dict[str, Any]:
        """Retourne le statut actuel de l'agent"""
        return {
            "name": self.name,
            "model": self.model,
            "is_running": self.is_running,
            "current_task": self.current_task,
            "tasks_completed": len(self.task_history),
            "memory_size": self.memory.size()
        }
    
    async def reset(self):
        """Réinitialise l'agent"""
        self.current_task = None
        self.task_history = []
        self.is_running = False
        await self.memory.clear()
        logger.info(f"Agent {self.name} réinitialisé")

