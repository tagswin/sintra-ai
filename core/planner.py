"""
Système de Planification Intelligent
"""

import json
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime

logger = logging.getLogger(__name__)


class TaskPlanner:
    """
    Planificateur de tâches hiérarchique avec capacité de raisonnement
    """
    
    def __init__(self, agent):
        self.agent = agent
        self.planning_history = []
    
    async def create_plan(
        self,
        task_description: str,
        context: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """
        Crée un plan d'exécution détaillé pour une tâche
        
        Args:
            task_description: Description de la tâche
            context: Contexte additionnel
            
        Returns:
            Plan d'exécution structuré
        """
        logger.info("🧠 Création du plan d'exécution...")
        
        # Analyser la tâche
        task_analysis = await self._analyze_task(task_description, context)
        
        # Décomposer en sous-tâches
        subtasks = await self._decompose_task(task_description, task_analysis)
        
        # Créer les étapes d'exécution
        steps = await self._create_execution_steps(subtasks)
        
        # Identifier les dépendances
        dependencies = self._identify_dependencies(steps)
        
        plan = {
            "task": task_description,
            "analysis": task_analysis,
            "steps": steps,
            "dependencies": dependencies,
            "estimated_duration": self._estimate_duration(steps),
            "created_at": datetime.now().isoformat(),
            "metadata": {
                "complexity": task_analysis.get("complexity", "medium"),
                "requires_tools": task_analysis.get("requires_tools", []),
                "risk_level": task_analysis.get("risk_level", "low")
            }
        }
        
        self.planning_history.append(plan)
        logger.info(f"📋 Plan créé avec {len(steps)} étapes")
        
        return plan
    
    async def _analyze_task(
        self,
        task_description: str,
        context: Optional[Dict]
    ) -> Dict[str, Any]:
        """
        Analyse la tâche pour comprendre sa nature et ses exigences
        """
        analysis_prompt = f"""Analyse cette tâche en détail:

Tâche: {task_description}

Contexte: {json.dumps(context) if context else "Aucun"}

Fournis une analyse structurée (JSON):
{{
    "type": "type de tâche (recherche, analyse, création, etc.)",
    "complexity": "simple|medium|complex",
    "requires_tools": ["liste des outils nécessaires"],
    "estimated_steps": "nombre estimé d'étapes",
    "risk_level": "low|medium|high",
    "key_challenges": ["défi 1", "défi 2"],
    "success_criteria": ["critère 1", "critère 2"]
}}
"""
        
        response = await self.agent.think(analysis_prompt)
        
        try:
            return json.loads(response)
        except:
            # Fallback en cas d'échec de parsing
            return {
                "type": "general",
                "complexity": "medium",
                "requires_tools": [],
                "estimated_steps": 3,
                "risk_level": "low",
                "raw_analysis": response
            }
    
    async def _decompose_task(
        self,
        task_description: str,
        analysis: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        Décompose la tâche en sous-tâches gérables
        """
        decomposition_prompt = f"""Décompose cette tâche en sous-tâches simples et actionnables:

Tâche principale: {task_description}

Analyse: {json.dumps(analysis, indent=2)}

Fournis une décomposition structurée (JSON):
{{
    "subtasks": [
        {{
            "id": "step_1",
            "description": "Description de la sous-tâche",
            "action": "action spécifique à effectuer",
            "tool": "outil à utiliser (ou null)",
            "inputs": {{}},
            "expected_output": "ce qui devrait être produit"
        }}
    ]
}}

Principes:
- Chaque sous-tâche doit être simple et claire
- Ordre logique d'exécution
- Chaque sous-tâche doit avoir un résultat mesurable
"""
        
        response = await self.agent.think(decomposition_prompt)
        
        try:
            data = json.loads(response)
            return data.get("subtasks", [])
        except:
            # Fallback: créer une sous-tâche simple
            return [{
                "id": "step_1",
                "description": task_description,
                "action": "execute",
                "tool": None,
                "inputs": {},
                "expected_output": "Résultat de la tâche"
            }]
    
    async def _create_execution_steps(
        self,
        subtasks: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Crée les étapes d'exécution détaillées à partir des sous-tâches
        """
        steps = []
        
        for i, subtask in enumerate(subtasks):
            step = {
                "id": subtask.get("id", f"step_{i+1}"),
                "order": i + 1,
                "description": subtask.get("description", ""),
                "action": subtask.get("action", "execute"),
                "tool": subtask.get("tool"),
                "inputs": subtask.get("inputs", {}),
                "expected_output": subtask.get("expected_output", ""),
                "status": "pending",
                "retries": 0,
                "max_retries": 3
            }
            steps.append(step)
        
        return steps
    
    def _identify_dependencies(self, steps: List[Dict[str, Any]]) -> Dict[str, List[str]]:
        """
        Identifie les dépendances entre les étapes
        
        Pour l'instant, assume une exécution séquentielle simple
        Dans une version avancée, on pourrait analyser les inputs/outputs
        """
        dependencies = {}
        
        for i, step in enumerate(steps):
            step_id = step["id"]
            # Chaque étape dépend de la précédente
            if i > 0:
                dependencies[step_id] = [steps[i-1]["id"]]
            else:
                dependencies[step_id] = []
        
        return dependencies
    
    def _estimate_duration(self, steps: List[Dict[str, Any]]) -> int:
        """
        Estime la durée d'exécution en secondes
        """
        # Estimation simple: 30 secondes par étape
        base_time = len(steps) * 30
        
        # Ajouter du temps pour les outils complexes
        for step in steps:
            tool = step.get("tool")
            if tool in ["web_search", "code_execution"]:
                base_time += 20
        
        return base_time
    
    async def replan(
        self,
        current_plan: Dict[str, Any],
        failed_step: Dict[str, Any],
        error: str
    ) -> Dict[str, Any]:
        """
        Replanifie après un échec
        """
        logger.warning(f"⚠️  Replanification nécessaire après échec de {failed_step['id']}")
        
        replan_prompt = f"""Une étape a échoué. Crée un nouveau plan:

Plan original: {json.dumps(current_plan, indent=2)}

Étape échouée: {json.dumps(failed_step, indent=2)}

Erreur: {error}

Propose une approche alternative ou une correction.
"""
        
        response = await self.agent.think(replan_prompt)
        
        # Pour l'instant, retourne le plan original avec l'étape modifiée
        # Dans une version avancée, on recréerait le plan complètement
        new_plan = current_plan.copy()
        new_plan["replanned"] = True
        new_plan["replan_reason"] = error
        
        return new_plan

