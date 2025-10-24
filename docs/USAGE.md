# Guide d'utilisation - Sintra AI

## Introduction

Sintra AI est un agent IA autonome qui peut comprendre, planifier et exécuter des tâches complexes pour vous.

## Démarrage rapide

### 1. Lancer le système

**Backend:**
```bash
python main.py
```

**Frontend:**
```bash
cd frontend
npm run dev
```

### 2. Accéder à l'interface

Ouvrez http://localhost:3000 dans votre navigateur.

## Interface utilisateur

### Page d'accueil

L'interface principale se compose de trois onglets:

#### 📋 Tâches

C'est ici que vous créez et suivez vos tâches.

**Créer une tâche:**
1. Tapez votre demande dans le champ de texte
2. Cliquez sur "🚀 Lancer la tâche"
3. L'agent commence immédiatement à travailler

**Exemples de tâches:**
- "Recherche les dernières tendances en IA"
- "Calcule la somme de 123 + 456 et multiplie le résultat par 2"
- "Crée un plan d'apprentissage pour Python"
- "Analyse les avantages de TypeScript par rapport à JavaScript"

**Suivre une tâche:**
- L'état s'actualise automatiquement toutes les 5 secondes
- Les tâches passent par les états: En attente → En cours → Terminée/Échouée

#### 🧠 Mémoire

Visualisez ce dont l'agent se souvient.

**Statistiques:**
- Mémoire de travail: Contexte actuel
- Mémoire épisodique: Tâches passées
- Mémoire sémantique: Connaissances apprises

**Recherche:**
- Tapez une requête pour chercher dans la mémoire
- L'agent trouve les souvenirs pertinents

#### ℹ️ À propos

Informations sur le système et ses capacités.

## Utilisation de l'API

### Python

```python
import requests
import time

API_BASE = "http://localhost:8000/api"

# Créer une tâche
response = requests.post(f"{API_BASE}/tasks", json={
    "description": "Recherche sur l'intelligence artificielle",
    "autonomous": True
})

task_id = response.json()["task_id"]
print(f"Tâche créée: {task_id}")

# Attendre la complétion
while True:
    status = requests.get(f"{API_BASE}/tasks/{task_id}").json()
    
    if status["status"] == "completed":
        print("✅ Tâche terminée!")
        print("Résultat:", status["result"])
        break
    elif status["status"] == "failed":
        print("❌ Tâche échouée:", status.get("error"))
        break
    else:
        print("⏳ En cours...")
        time.sleep(3)
```

### JavaScript/TypeScript

```javascript
const API_BASE = "http://localhost:8000/api";

async function runTask(description) {
  // Créer la tâche
  const createRes = await fetch(`${API_BASE}/tasks`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      description,
      autonomous: true
    })
  });
  
  const { task_id } = await createRes.json();
  console.log(`Tâche créée: ${task_id}`);
  
  // Polling du statut
  while (true) {
    const statusRes = await fetch(`${API_BASE}/tasks/${task_id}`);
    const status = await statusRes.json();
    
    if (status.status === "completed") {
      console.log("✅ Terminée!", status.result);
      return status.result;
    } else if (status.status === "failed") {
      console.error("❌ Échouée:", status.error);
      throw new Error(status.error);
    }
    
    await new Promise(resolve => setTimeout(resolve, 3000));
  }
}

// Utilisation
runTask("Explique-moi l'apprentissage par renforcement");
```

### cURL

```bash
# Créer une tâche
curl -X POST http://localhost:8000/api/tasks \
  -H "Content-Type: application/json" \
  -d '{
    "description": "Calcule 15 * 27 + 100",
    "autonomous": true
  }'

# Récupérer le statut
curl http://localhost:8000/api/tasks/task_1_20241023120000

# Faire réfléchir l'agent
curl -X POST http://localhost:8000/api/think \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Quelle est la différence entre ML et DL ?"
  }'
```

## Types de tâches supportées

### 1. Recherche d'information

```
"Recherche des informations sur [sujet]"
"Trouve les dernières nouvelles sur [topic]"
"Quelles sont les tendances de [domaine] ?"
```

### 2. Calculs

```
"Calcule 123 + 456 * 2"
"Quelle est la racine carrée de 144 ?"
"Convertis 100 USD en EUR"
```

### 3. Analyse

```
"Analyse les avantages et inconvénients de [technologie]"
"Compare [A] et [B]"
"Quelles sont les implications de [événement] ?"
```

### 4. Planification

```
"Crée un plan pour apprendre [compétence]"
"Organise un projet de [type]"
"Planifie un itinéraire pour [destination]"
```

### 5. Génération de contenu

```
"Écris un article sur [sujet]"
"Génère des idées pour [projet]"
"Crée un résumé de [texte]"
```

### 6. Programmation

```
"Écris un script Python pour [tâche]"
"Debug ce code: [code]"
"Explique comment fonctionne [concept de programmation]"
```

## Bonnes pratiques

### 1. Soyez spécifique

❌ **Mauvais:** "Recherche sur l'IA"
✅ **Bon:** "Recherche les applications pratiques de l'IA en médecine en 2024"

### 2. Décomposez les tâches complexes

❌ **Mauvais:** "Crée-moi une entreprise complète"
✅ **Bon:** 
- Tâche 1: "Génère des idées de startup en tech"
- Tâche 2: "Analyse le marché pour [idée choisie]"
- Tâche 3: "Crée un business plan pour [idée]"

### 3. Fournissez du contexte

❌ **Mauvais:** "Analyse ce document"
✅ **Bon:** "Analyse ce document de spécifications techniques pour identifier les risques potentiels et les recommandations d'amélioration"

### 4. Utilisez les exemples

L'interface propose des exemples de tâches. Cliquez dessus pour les utiliser comme point de départ.

### 5. Surveillez la mémoire

L'agent apprend de ses expériences. Consultez l'onglet Mémoire pour voir ce qu'il a retenu.

## Mode démonstration

Pour tester rapidement l'agent sans l'interface:

```bash
python main.py demo
```

Cela exécute une tâche de démonstration prédéfinie.

## Configuration avancée

### Changer le modèle d'IA

Dans `.env`:
```env
# OpenAI
AGENT_MODEL=gpt-4-turbo-preview
# ou
AGENT_MODEL=gpt-3.5-turbo

# Anthropic
AGENT_MODEL=claude-3-opus-20240229
# ou
AGENT_MODEL=claude-3-sonnet-20240229
```

### Ajuster la température

Plus élevée = Plus créatif, moins prévisible
Plus basse = Plus déterministe, plus cohérent

```env
TEMPERATURE=0.7  # Par défaut
# 0.0 = très déterministe
# 1.0 = très créatif
```

### Limites

```env
MAX_ITERATIONS=50          # Nombre max d'itérations
MAX_TASK_DURATION=3600     # Timeout en secondes
MAX_CONCURRENT_TASKS=5     # Tâches simultanées
```

## Résolution de problèmes

### L'agent ne répond pas

1. Vérifiez que le backend est lancé
2. Vérifiez votre clé API
3. Consultez les logs dans le terminal

### Tâche échoue immédiatement

1. La tâche est peut-être trop vague
2. Vérifiez les logs pour l'erreur exacte
3. Réessayez avec plus de contexte

### Résultats incohérents

1. Augmentez le nombre d'itérations
2. Baissez la température
3. Soyez plus spécifique dans votre demande

### Performance lente

1. Vérifiez votre connexion internet
2. Certaines tâches prennent naturellement plus de temps
3. Envisagez un modèle plus rapide (gpt-3.5-turbo)

## Exemples d'utilisation avancée

### Chaîner des tâches

```python
# Tâche 1: Recherche
task1 = create_task("Recherche les frameworks JS populaires en 2024")
result1 = wait_for_task(task1)

# Tâche 2: Analyse basée sur les résultats
frameworks = extract_frameworks(result1)
task2 = create_task(f"Compare {frameworks[0]} et {frameworks[1]}")
result2 = wait_for_task(task2)

# Tâche 3: Recommandation
task3 = create_task(f"Recommande le meilleur framework pour un projet {project_type} basé sur l'analyse précédente")
result3 = wait_for_task(task3)
```

### Intégration dans une application

```python
from sintra_client import SintraClient

client = SintraClient("http://localhost:8000/api")

# Dans votre application
@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json
    
    # Utiliser Sintra pour l'analyse
    result = client.run_task(
        f"Analyse ces données: {data}"
    )
    
    return jsonify(result)
```

## Limites actuelles

1. **Code exécution**: Sandbox basique (pas de Docker)
2. **Recherche web**: Simulée (pas de vraie API)
3. **Mémoire**: En RAM (pas de persistance)
4. **Multi-utilisateurs**: Non supporté
5. **Streaming**: Pas de réponses en streaming

Ces limitations seront adressées dans les versions futures.

## Support

- Documentation: `/docs`
- API interactive: http://localhost:8000/docs
- Issues: GitHub (si open source)

## Prochaines étapes

1. Explorez les différents types de tâches
2. Testez l'API dans vos projets
3. Expérimentez avec différents modèles
4. Consultez la documentation avancée dans `/docs`

