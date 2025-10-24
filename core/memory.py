"""
Système de Mémoire pour l'Agent
"""

import asyncio
import json
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
from collections import defaultdict

logger = logging.getLogger(__name__)


class MemorySystem:
    """
    Système de mémoire multi-niveaux pour l'agent:
    - Mémoire de travail (court terme)
    - Mémoire épisodique (tâches passées)
    - Mémoire sémantique (connaissances apprises)
    """
    
    def __init__(self, max_working_memory: int = 10):
        self.max_working_memory = max_working_memory
        
        # Mémoire de travail (court terme)
        self.working_memory = []
        
        # Mémoire épisodique (expériences passées)
        self.episodic_memory = []
        
        # Mémoire sémantique (connaissances)
        self.semantic_memory = defaultdict(list)
        
        # Métadonnées
        self.memory_stats = {
            "tasks_stored": 0,
            "knowledge_items": 0,
            "total_retrievals": 0
        }
        
        logger.info("💾 Système de mémoire initialisé")
    
    async def store_task(
        self,
        task_description: str,
        plan: Dict[str, Any],
        results: List[Dict[str, Any]],
        final_result: Dict[str, Any]
    ):
        """
        Stocke une tâche complétée dans la mémoire épisodique
        """
        memory_entry = {
            "id": f"task_{len(self.episodic_memory) + 1}",
            "timestamp": datetime.now().isoformat(),
            "description": task_description,
            "plan": plan,
            "results": results,
            "final_result": final_result,
            "success": final_result.get("summary") is not None,
            "type": "episodic"
        }
        
        self.episodic_memory.append(memory_entry)
        
        # Ajouter à la mémoire de travail
        self._add_to_working_memory(memory_entry)
        
        # Extraire et stocker les connaissances
        await self._extract_knowledge(memory_entry)
        
        self.memory_stats["tasks_stored"] += 1
        
        logger.info(f"💾 Tâche stockée en mémoire: {task_description[:50]}...")
    
    def _add_to_working_memory(self, entry: Dict[str, Any]):
        """
        Ajoute une entrée à la mémoire de travail
        """
        self.working_memory.append(entry)
        
        # Limiter la taille de la mémoire de travail
        if len(self.working_memory) > self.max_working_memory:
            self.working_memory.pop(0)
    
    async def _extract_knowledge(self, task_entry: Dict[str, Any]):
        """
        Extrait des connaissances d'une tâche complétée
        """
        # Identifier les patterns réussis
        if task_entry["success"]:
            plan_type = task_entry["plan"].get("analysis", {}).get("type", "general")
            
            knowledge_item = {
                "id": f"knowledge_{self.memory_stats['knowledge_items'] + 1}",
                "source": task_entry["id"],
                "timestamp": datetime.now().isoformat(),
                "category": plan_type,
                "content": {
                    "successful_approach": task_entry["plan"].get("steps", []),
                    "tools_used": [step.get("tool") for step in task_entry["plan"].get("steps", []) if step.get("tool")],
                    "outcome": task_entry["final_result"]
                }
            }
            
            self.semantic_memory[plan_type].append(knowledge_item)
            self.memory_stats["knowledge_items"] += 1
    
    async def retrieve_relevant(
        self,
        query: str,
        limit: int = 5,
        memory_type: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Récupère les mémoires pertinentes pour une requête
        
        Args:
            query: La requête de recherche
            limit: Nombre maximum de résultats
            memory_type: Type de mémoire à chercher (episodic, semantic, working)
        """
        self.memory_stats["total_retrievals"] += 1
        
        relevant_memories = []
        
        # Recherche simple par mots-clés (dans une version avancée, utiliser embeddings)
        query_lower = query.lower()
        
        # Chercher dans la mémoire de travail
        if memory_type is None or memory_type == "working":
            for memory in reversed(self.working_memory):
                if self._is_relevant(memory, query_lower):
                    relevant_memories.append(memory)
                if len(relevant_memories) >= limit:
                    return relevant_memories
        
        # Chercher dans la mémoire épisodique
        if memory_type is None or memory_type == "episodic":
            for memory in reversed(self.episodic_memory):
                if self._is_relevant(memory, query_lower):
                    relevant_memories.append(memory)
                if len(relevant_memories) >= limit:
                    return relevant_memories
        
        # Chercher dans la mémoire sémantique
        if memory_type is None or memory_type == "semantic":
            for category, items in self.semantic_memory.items():
                for item in reversed(items):
                    if query_lower in category.lower() or self._is_relevant(item, query_lower):
                        relevant_memories.append(item)
                    if len(relevant_memories) >= limit:
                        return relevant_memories
        
        return relevant_memories[:limit]
    
    def _is_relevant(self, memory: Dict[str, Any], query: str) -> bool:
        """
        Vérifie si une mémoire est pertinente pour une requête
        """
        # Recherche simple dans la description
        memory_str = json.dumps(memory).lower()
        
        # Découper la requête en mots
        query_words = query.split()
        
        # Vérifier si au moins 2 mots sont présents
        matches = sum(1 for word in query_words if word in memory_str)
        
        return matches >= min(2, len(query_words))
    
    def get_recent_memories(self, count: int = 5) -> List[Dict[str, Any]]:
        """
        Retourne les mémoires les plus récentes
        """
        all_memories = self.working_memory + self.episodic_memory
        all_memories.sort(key=lambda x: x.get("timestamp", ""), reverse=True)
        return all_memories[:count]
    
    def get_knowledge_by_category(self, category: str) -> List[Dict[str, Any]]:
        """
        Retourne les connaissances d'une catégorie spécifique
        """
        return self.semantic_memory.get(category, [])
    
    def size(self) -> Dict[str, int]:
        """
        Retourne la taille de chaque type de mémoire
        """
        return {
            "working": len(self.working_memory),
            "episodic": len(self.episodic_memory),
            "semantic": sum(len(items) for items in self.semantic_memory.values())
        }
    
    async def clear(self, memory_type: Optional[str] = None):
        """
        Efface la mémoire
        """
        if memory_type == "working" or memory_type is None:
            self.working_memory = []
        
        if memory_type == "episodic" or memory_type is None:
            self.episodic_memory = []
        
        if memory_type == "semantic" or memory_type is None:
            self.semantic_memory = defaultdict(list)
        
        logger.info(f"🗑️  Mémoire effacée: {memory_type or 'all'}")
    
    def export_memories(self) -> Dict[str, Any]:
        """
        Exporte toutes les mémoires en format JSON
        """
        return {
            "working_memory": self.working_memory,
            "episodic_memory": self.episodic_memory,
            "semantic_memory": dict(self.semantic_memory),
            "stats": self.memory_stats,
            "exported_at": datetime.now().isoformat()
        }
    
    def import_memories(self, data: Dict[str, Any]):
        """
        Importe des mémoires depuis un format JSON
        """
        if "working_memory" in data:
            self.working_memory = data["working_memory"]
        
        if "episodic_memory" in data:
            self.episodic_memory = data["episodic_memory"]
        
        if "semantic_memory" in data:
            self.semantic_memory = defaultdict(list, data["semantic_memory"])
        
        if "stats" in data:
            self.memory_stats = data["stats"]
        
        logger.info("📥 Mémoires importées avec succès")

