"""
Moteur d'Exécution des Tâches
"""

import asyncio
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime

from tools import ToolRegistry

logger = logging.getLogger(__name__)


class TaskExecutor:
    """
    Exécute les plans de tâches créés par le planificateur
    """
    
    def __init__(self, agent):
        self.agent = agent
        self.tool_registry = ToolRegistry()
        self.execution_history = []
        self.current_execution = None
    
    async def execute_plan(self, plan: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Exécute un plan complet
        
        Args:
            plan: Le plan à exécuter
            
        Returns:
            Liste des résultats pour chaque étape
        """
        steps = plan["steps"]
        dependencies = plan.get("dependencies", {})
        
        logger.info(f"⚙️  Démarrage de l'exécution de {len(steps)} étapes")
        
        self.current_execution = {
            "plan_id": plan.get("created_at"),
            "start_time": datetime.now(),
            "status": "running"
        }
        
        results = []
        completed_steps = set()
        
        try:
            # Exécuter les étapes dans l'ordre
            for step in steps:
                step_id = step["id"]
                
                # Vérifier les dépendances
                deps = dependencies.get(step_id, [])
                if not all(dep in completed_steps for dep in deps):
                    logger.warning(f"⚠️  Dépendances non satisfaites pour {step_id}")
                    continue
                
                # Exécuter l'étape
                logger.info(f"  📌 Exécution: {step['description']}")
                step_result = await self._execute_step(step, results)
                
                results.append(step_result)
                
                if step_result["success"]:
                    completed_steps.add(step_id)
                    logger.info(f"  ✅ Étape {step_id} complétée")
                else:
                    logger.error(f"  ❌ Étape {step_id} échouée: {step_result.get('error')}")
                    
                    # Décider si on continue ou on arrête
                    if not step.get("optional", False):
                        # Tenter une nouvelle fois
                        if step["retries"] < step["max_retries"]:
                            step["retries"] += 1
                            logger.info(f"  🔄 Nouvelle tentative {step['retries']}/{step['max_retries']}")
                            # Re-exécuter
                            step_result = await self._execute_step(step, results)
                            results[-1] = step_result
                            
                            if step_result["success"]:
                                completed_steps.add(step_id)
                        else:
                            logger.error(f"  ⛔ Nombre maximum de tentatives atteint")
                            break
            
            self.current_execution["status"] = "completed"
            self.current_execution["end_time"] = datetime.now()
            self.execution_history.append(self.current_execution)
            
            return results
            
        except Exception as e:
            logger.error(f"❌ Erreur fatale lors de l'exécution: {str(e)}")
            self.current_execution["status"] = "failed"
            self.current_execution["error"] = str(e)
            raise
        finally:
            self.current_execution = None
    
    async def _execute_step(
        self,
        step: Dict[str, Any],
        previous_results: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Exécute une étape individuelle
        
        Args:
            step: L'étape à exécuter
            previous_results: Résultats des étapes précédentes
            
        Returns:
            Résultat de l'exécution
        """
        step_id = step["id"]
        action = step["action"]
        tool_name = step.get("tool")
        
        result = {
            "step_id": step_id,
            "description": step["description"],
            "start_time": datetime.now().isoformat(),
            "success": False
        }
        
        try:
            # Si un outil est spécifié, l'utiliser
            if tool_name:
                result["output"] = await self._execute_with_tool(
                    tool_name,
                    step["inputs"],
                    previous_results
                )
            else:
                # Sinon, demander à l'agent de réfléchir
                result["output"] = await self._execute_with_thinking(
                    step,
                    previous_results
                )
            
            result["success"] = True
            result["end_time"] = datetime.now().isoformat()
            
        except Exception as e:
            logger.error(f"Erreur lors de l'exécution de {step_id}: {str(e)}")
            result["success"] = False
            result["error"] = str(e)
            result["end_time"] = datetime.now().isoformat()
        
        return result
    
    async def _execute_with_tool(
        self,
        tool_name: str,
        inputs: Dict[str, Any],
        previous_results: List[Dict[str, Any]]
    ) -> Any:
        """
        Exécute une étape en utilisant un outil spécifique
        """
        # Enrichir les inputs avec les résultats précédents si nécessaire
        enriched_inputs = self._enrich_inputs(inputs, previous_results)
        
        # Obtenir et exécuter l'outil
        tool = self.tool_registry.get_tool(tool_name)
        
        if not tool:
            raise ValueError(f"Outil non trouvé: {tool_name}")
        
        logger.debug(f"    🔧 Utilisation de l'outil: {tool_name}")
        
        return await tool.execute(**enriched_inputs)
    
    async def _execute_with_thinking(
        self,
        step: Dict[str, Any],
        previous_results: List[Dict[str, Any]]
    ) -> str:
        """
        Exécute une étape en faisant réfléchir l'agent
        """
        # Construire le contexte
        context = {
            "step": step,
            "previous_results": previous_results
        }
        
        prompt = f"""Exécute cette étape:

Description: {step['description']}
Action: {step['action']}
Inputs: {step.get('inputs', {})}

Résultats précédents:
{self._format_previous_results(previous_results)}

Fournis une réponse claire et actionnable.
"""
        
        logger.debug(f"    🧠 Réflexion sur l'étape")
        
        return await self.agent.think(prompt, context)
    
    def _enrich_inputs(
        self,
        inputs: Dict[str, Any],
        previous_results: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Enrichit les inputs avec les résultats précédents
        
        Résout les références comme {"$ref": "step_1.output"}
        """
        enriched = inputs.copy()
        
        for key, value in inputs.items():
            if isinstance(value, dict) and "$ref" in value:
                # Résoudre la référence
                ref_path = value["$ref"]
                enriched[key] = self._resolve_reference(ref_path, previous_results)
        
        return enriched
    
    def _resolve_reference(
        self,
        ref_path: str,
        previous_results: List[Dict[str, Any]]
    ) -> Any:
        """
        Résout une référence à un résultat précédent
        
        Format: "step_id.field.subfield"
        """
        parts = ref_path.split(".")
        step_id = parts[0]
        
        # Trouver le résultat correspondant
        for result in previous_results:
            if result["step_id"] == step_id:
                # Naviguer dans les champs
                value = result
                for part in parts[1:]:
                    if isinstance(value, dict):
                        value = value.get(part)
                    else:
                        return None
                return value
        
        return None
    
    def _format_previous_results(self, results: List[Dict[str, Any]]) -> str:
        """
        Formate les résultats précédents pour affichage
        """
        if not results:
            return "Aucun résultat précédent"
        
        formatted = []
        for result in results:
            formatted.append(
                f"- {result['step_id']}: {result.get('output', 'N/A')[:100]}"
            )
        
        return "\n".join(formatted)
    
    def get_execution_status(self) -> Optional[Dict[str, Any]]:
        """
        Retourne le statut de l'exécution actuelle
        """
        return self.current_execution

