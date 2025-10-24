# Documentation API - Sintra AI

## Base URL

```
http://localhost:8000/api
```

## Authentification

Actuellement, aucune authentification n'est requise. En production, ajoutez une couche d'authentification (JWT, API Key, etc.).

## Endpoints

### 1. Statut de l'agent

**GET** `/api/agent/status`

Obtient le statut actuel de l'agent.

**Réponse:**
```json
{
  "name": "Sintra",
  "model": "gpt-4-turbo-preview",
  "is_running": false,
  "tasks_completed": 5,
  "memory_size": {
    "working": 3,
    "episodic": 5,
    "semantic": 2
  },
  "current_task": null
}
```

### 2. Créer une tâche

**POST** `/api/tasks`

Crée et lance une nouvelle tâche.

**Corps de la requête:**
```json
{
  "description": "Recherche les dernières tendances en IA",
  "context": {
    "additional_info": "Concentre-toi sur 2024"
  },
  "autonomous": true,
  "model": "gpt-4-turbo-preview"
}
```

**Réponse:**
```json
{
  "task_id": "task_1_20241023120000",
  "status": "pending",
  "created_at": "2024-10-23T12:00:00"
}
```

### 3. Obtenir le statut d'une tâche

**GET** `/api/tasks/{task_id}`

Obtient le statut et les résultats d'une tâche.

**Réponse:**
```json
{
  "task_id": "task_1_20241023120000",
  "status": "completed",
  "description": "Recherche les dernières tendances en IA",
  "created_at": "2024-10-23T12:00:00",
  "updated_at": "2024-10-23T12:05:00",
  "result": {
    "success": true,
    "result": {
      "summary": "Les principales tendances en IA pour 2024 incluent...",
      "key_findings": [
        "LLMs multimodaux",
        "IA générative",
        "Agents autonomes"
      ]
    },
    "duration": 45.2
  }
}
```

### 4. Lister toutes les tâches

**GET** `/api/tasks`

Liste toutes les tâches créées.

**Réponse:**
```json
{
  "tasks": [
    {
      "id": "task_1_20241023120000",
      "description": "...",
      "status": "completed",
      "created_at": "2024-10-23T12:00:00"
    }
  ],
  "count": 1
}
```

### 5. Supprimer une tâche

**DELETE** `/api/tasks/{task_id}`

Supprime une tâche de l'historique.

**Réponse:**
```json
{
  "success": true,
  "message": "Tâche task_1_20241023120000 supprimée"
}
```

### 6. Réflexion directe

**POST** `/api/think`

Fait réfléchir l'agent sur un prompt sans créer de tâche complète.

**Corps de la requête:**
```json
{
  "prompt": "Quelle est la capitale de la France ?",
  "context": {}
}
```

**Réponse:**
```json
{
  "success": true,
  "prompt": "Quelle est la capitale de la France ?",
  "response": "La capitale de la France est Paris..."
}
```

### 7. Obtenir la mémoire

**GET** `/api/memory`

Obtient des informations sur la mémoire de l'agent.

**Réponse:**
```json
{
  "size": {
    "working": 3,
    "episodic": 5,
    "semantic": 2
  },
  "stats": {
    "tasks_stored": 5,
    "knowledge_items": 2,
    "total_retrievals": 10
  },
  "recent_memories": [...]
}
```

### 8. Rechercher dans la mémoire

**GET** `/api/memory/search?query=IA&limit=5`

Recherche dans la mémoire de l'agent.

**Paramètres:**
- `query` (string, requis): Requête de recherche
- `limit` (int, optionnel): Nombre de résultats (défaut: 5)

**Réponse:**
```json
{
  "query": "IA",
  "results": [
    {
      "id": "task_1",
      "description": "Recherche sur l'IA",
      "timestamp": "2024-10-23T12:00:00"
    }
  ],
  "count": 1
}
```

### 9. Réinitialiser l'agent

**POST** `/api/agent/reset`

Réinitialise l'agent (efface la mémoire et l'historique).

**Réponse:**
```json
{
  "success": true,
  "message": "Agent réinitialisé"
}
```

## Codes de statut

- `200`: Succès
- `201`: Créé
- `400`: Requête invalide
- `404`: Ressource non trouvée
- `500`: Erreur serveur

## Statuts de tâche

- `pending`: En attente d'exécution
- `running`: En cours d'exécution
- `completed`: Terminée avec succès
- `failed`: Échouée

## Exemples d'utilisation

### Python

```python
import requests

API_BASE = "http://localhost:8000/api"

# Créer une tâche
response = requests.post(f"{API_BASE}/tasks", json={
    "description": "Calcule 2 + 2",
    "autonomous": True
})
task_id = response.json()["task_id"]

# Vérifier le statut
import time
while True:
    status = requests.get(f"{API_BASE}/tasks/{task_id}").json()
    if status["status"] in ["completed", "failed"]:
        print(status["result"])
        break
    time.sleep(2)
```

### JavaScript

```javascript
const API_BASE = "http://localhost:8000/api";

// Créer une tâche
const response = await fetch(`${API_BASE}/tasks`, {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    description: "Recherche sur l'IA",
    autonomous: true
  })
});

const { task_id } = await response.json();

// Vérifier le statut
const checkStatus = async () => {
  const res = await fetch(`${API_BASE}/tasks/${task_id}`);
  const data = await res.json();
  
  if (data.status === "completed") {
    console.log(data.result);
  } else if (data.status === "running") {
    setTimeout(checkStatus, 2000);
  }
};

checkStatus();
```

### cURL

```bash
# Créer une tâche
curl -X POST http://localhost:8000/api/tasks \
  -H "Content-Type: application/json" \
  -d '{"description": "Calcule 15 + 27", "autonomous": true}'

# Obtenir le statut
curl http://localhost:8000/api/tasks/task_1_20241023120000

# Faire réfléchir l'agent
curl -X POST http://localhost:8000/api/think \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Quelle est la capitale de la France ?"}'
```

## Documentation interactive

La documentation interactive Swagger est disponible sur:
```
http://localhost:8000/docs
```

