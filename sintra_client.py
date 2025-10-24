"""
Client Python pour Sintra AI
Facilite l'utilisation de l'API Sintra
"""

import time
import requests
from typing import Dict, Any, Optional, List


class SintraClient:
    """
    Client Python pour interagir avec l'API Sintra AI
    
    Usage:
        client = SintraClient("http://localhost:8000/api")
        result = client.run_task("Calcule 2 + 2")
        print(result)
    """
    
    def __init__(self, api_base: str = "http://localhost:8000/api"):
        """
        Initialise le client
        
        Args:
            api_base: URL de base de l'API
        """
        self.api_base = api_base.rstrip('/')
        self.session = requests.Session()
    
    def run_task(
        self,
        description: str,
        context: Optional[Dict] = None,
        timeout: int = 300,
        poll_interval: int = 2
    ) -> Dict[str, Any]:
        """
        Exécute une tâche et attend le résultat
        
        Args:
            description: Description de la tâche
            context: Contexte additionnel
            timeout: Timeout en secondes
            poll_interval: Intervalle de vérification en secondes
            
        Returns:
            Résultat de la tâche
            
        Raises:
            TimeoutError: Si la tâche dépasse le timeout
            RuntimeError: Si la tâche échoue
        """
        # Créer la tâche
        response = self.session.post(
            f"{self.api_base}/tasks",
            json={
                "description": description,
                "context": context or {},
                "autonomous": True
            }
        )
        response.raise_for_status()
        
        task_id = response.json()["task_id"]
        print(f"✓ Tâche créée: {task_id}")
        
        # Attendre la complétion
        start_time = time.time()
        
        while True:
            # Vérifier le timeout
            if time.time() - start_time > timeout:
                raise TimeoutError(f"Tâche {task_id} a dépassé le timeout de {timeout}s")
            
            # Obtenir le statut
            status_response = self.session.get(f"{self.api_base}/tasks/{task_id}")
            status_response.raise_for_status()
            status = status_response.json()
            
            if status["status"] == "completed":
                print(f"✓ Tâche terminée en {time.time() - start_time:.1f}s")
                return status["result"]
            
            elif status["status"] == "failed":
                error = status.get("error", "Erreur inconnue")
                raise RuntimeError(f"Tâche échouée: {error}")
            
            # Attendre avant la prochaine vérification
            time.sleep(poll_interval)
    
    def think(self, prompt: str, context: Optional[Dict] = None) -> str:
        """
        Fait réfléchir l'agent sur un prompt
        
        Args:
            prompt: Le prompt
            context: Contexte additionnel
            
        Returns:
            Réponse de l'agent
        """
        response = self.session.post(
            f"{self.api_base}/think",
            json={
                "prompt": prompt,
                "context": context or {}
            }
        )
        response.raise_for_status()
        
        return response.json()["response"]
    
    def get_agent_status(self) -> Dict[str, Any]:
        """
        Obtient le statut de l'agent
        
        Returns:
            Statut de l'agent
        """
        response = self.session.get(f"{self.api_base}/agent/status")
        response.raise_for_status()
        return response.json()
    
    def list_tasks(self) -> List[Dict[str, Any]]:
        """
        Liste toutes les tâches
        
        Returns:
            Liste des tâches
        """
        response = self.session.get(f"{self.api_base}/tasks")
        response.raise_for_status()
        return response.json()["tasks"]
    
    def get_task(self, task_id: str) -> Dict[str, Any]:
        """
        Obtient les détails d'une tâche
        
        Args:
            task_id: ID de la tâche
            
        Returns:
            Détails de la tâche
        """
        response = self.session.get(f"{self.api_base}/tasks/{task_id}")
        response.raise_for_status()
        return response.json()
    
    def delete_task(self, task_id: str) -> bool:
        """
        Supprime une tâche
        
        Args:
            task_id: ID de la tâche
            
        Returns:
            True si succès
        """
        response = self.session.delete(f"{self.api_base}/tasks/{task_id}")
        response.raise_for_status()
        return response.json()["success"]
    
    def search_memory(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """
        Recherche dans la mémoire de l'agent
        
        Args:
            query: Requête de recherche
            limit: Nombre de résultats
            
        Returns:
            Résultats de la recherche
        """
        response = self.session.get(
            f"{self.api_base}/memory/search",
            params={"query": query, "limit": limit}
        )
        response.raise_for_status()
        return response.json()["results"]
    
    def get_memory(self) -> Dict[str, Any]:
        """
        Obtient des informations sur la mémoire
        
        Returns:
            Informations mémoire
        """
        response = self.session.get(f"{self.api_base}/memory")
        response.raise_for_status()
        return response.json()
    
    def reset_agent(self) -> bool:
        """
        Réinitialise l'agent
        
        Returns:
            True si succès
        """
        response = self.session.post(f"{self.api_base}/agent/reset")
        response.raise_for_status()
        return response.json()["success"]


def main():
    """
    Fonction de démonstration
    """
    print("🤖 Client Sintra AI - Démonstration\n")
    
    # Créer le client
    client = SintraClient()
    
    try:
        # Vérifier le statut
        print("📊 Statut de l'agent:")
        status = client.get_agent_status()
        print(f"   Nom: {status['name']}")
        print(f"   Modèle: {status['model']}")
        print(f"   Tâches complétées: {status['tasks_completed']}")
        print()
        
        # Réflexion simple
        print("🧠 Test de réflexion:")
        response = client.think("Quelle est la capitale de la France ?")
        print(f"   {response[:100]}...")
        print()
        
        # Exécuter une tâche
        print("🚀 Exécution d'une tâche:")
        result = client.run_task("Calcule 15 + 27 et explique le résultat")
        print(f"   Résultat: {result}")
        print()
        
        # Lister les tâches
        print("📋 Liste des tâches:")
        tasks = client.list_tasks()
        print(f"   {len(tasks)} tâche(s) trouvée(s)")
        
    except Exception as e:
        print(f"❌ Erreur: {str(e)}")
        print("\nAssurez-vous que le serveur Sintra AI est lancé:")
        print("   python main.py")


if __name__ == "__main__":
    main()

