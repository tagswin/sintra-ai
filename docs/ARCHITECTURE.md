# Architecture de Sintra AI

## Vue d'ensemble

Sintra AI est un système d'agent IA autonome composé de plusieurs modules interconnectés travaillant ensemble pour accomplir des tâches complexes.

```
┌─────────────────────────────────────────────────────────┐
│                    Frontend (Next.js)                    │
│  ┌──────────┐  ┌──────────┐  ┌─────────────────────┐   │
│  │   UI     │  │  Tasks   │  │      Memory         │   │
│  │ Components│  │  Manager │  │      Viewer         │   │
│  └──────────┘  └──────────┘  └─────────────────────┘   │
└─────────────────────────────────────────────────────────┘
                          │ HTTP/REST
┌─────────────────────────────────────────────────────────┐
│                   API Layer (FastAPI)                    │
│  ┌──────────┐  ┌──────────┐  ┌─────────────────────┐   │
│  │  Routes  │  │  Models  │  │    Middleware       │   │
│  └──────────┘  └──────────┘  └─────────────────────┘   │
└─────────────────────────────────────────────────────────┘
                          │
┌─────────────────────────────────────────────────────────┐
│                    Core Agent System                     │
│  ┌──────────────────────────────────────────────────┐   │
│  │               Sintra Agent                       │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────────┐  │   │
│  │  │ Planner  │→ │ Executor │→ │ Synthesizer  │  │   │
│  │  └──────────┘  └──────────┘  └──────────────┘  │   │
│  └──────────────────────────────────────────────────┘   │
│                          ↕                               │
│  ┌──────────────────────────────────────────────────┐   │
│  │            Memory System                         │   │
│  │  ┌────────────┐ ┌────────────┐ ┌─────────────┐ │   │
│  │  │  Working   │ │ Episodic   │ │  Semantic   │ │   │
│  │  │  Memory    │ │  Memory    │ │   Memory    │ │   │
│  │  └────────────┘ └────────────┘ └─────────────┘ │   │
│  └──────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
                          │
┌─────────────────────────────────────────────────────────┐
│                    Tool Registry                         │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌────────┐ │
│  │   Web    │  │   Code   │  │  Files   │  │  Calc  │ │
│  │  Search  │  │  Executor│  │  Manager │  │        │ │
│  └──────────┘  └──────────┘  └──────────┘  └────────┘ │
└─────────────────────────────────────────────────────────┘
                          │
┌─────────────────────────────────────────────────────────┐
│                 External Services                        │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐             │
│  │  OpenAI  │  │ Anthropic│  │ Database │             │
│  └──────────┘  └──────────┘  └──────────┘             │
└─────────────────────────────────────────────────────────┘
```

## Composants principaux

### 1. Frontend (Next.js)

Interface utilisateur moderne et réactive.

**Responsabilités:**
- Affichage de l'interface utilisateur
- Création et gestion des tâches
- Visualisation de la mémoire
- Communication avec l'API

**Technologies:**
- Next.js 14 (App Router)
- React 18
- TailwindCSS
- Framer Motion
- Axios

### 2. API Layer (FastAPI)

Couche API REST pour la communication.

**Responsabilités:**
- Exposition des endpoints REST
- Validation des requêtes
- Gestion des erreurs
- Documentation automatique (Swagger)

**Endpoints principaux:**
- `/api/agent/status` - Statut de l'agent
- `/api/tasks` - Gestion des tâches
- `/api/memory` - Système de mémoire
- `/api/think` - Réflexion directe

### 3. Core Agent System

Cœur du système d'IA autonome.

#### 3.1 SintraAgent

Classe principale orchestrant toutes les opérations.

**Méthodes clés:**
- `run_task()` - Exécute une tâche complète
- `think()` - Fait réfléchir l'agent
- `get_status()` - Retourne le statut
- `reset()` - Réinitialise l'agent

#### 3.2 TaskPlanner

Système de planification hiérarchique.

**Responsabilités:**
- Analyse de la tâche
- Décomposition en sous-tâches
- Identification des dépendances
- Estimation de durée
- Replanification en cas d'échec

**Algorithme:**
```python
1. Analyser la tâche (type, complexité, outils requis)
2. Décomposer en sous-tâches atomiques
3. Créer les étapes d'exécution
4. Identifier les dépendances
5. Générer le plan complet
```

#### 3.3 TaskExecutor

Moteur d'exécution des plans.

**Responsabilités:**
- Exécution séquentielle des étapes
- Gestion des dépendances
- Gestion des erreurs et retries
- Utilisation des outils
- Résolution des références

**Flux d'exécution:**
```python
Pour chaque étape du plan:
  1. Vérifier les dépendances
  2. Si outil spécifié:
     - Exécuter avec l'outil
  3. Sinon:
     - Faire réfléchir l'agent
  4. Enregistrer le résultat
  5. Si échec et retries disponibles:
     - Réessayer
  6. Sinon:
     - Continuer ou arrêter
```

#### 3.4 MemorySystem

Système de mémoire multi-niveaux.

**Types de mémoire:**

1. **Mémoire de travail (Working Memory)**
   - Court terme
   - Taille limitée (10 entrées)
   - Contexte immédiat

2. **Mémoire épisodique (Episodic Memory)**
   - Expériences passées
   - Tâches complétées
   - Historique complet

3. **Mémoire sémantique (Semantic Memory)**
   - Connaissances apprises
   - Patterns réussis
   - Organisée par catégorie

**Opérations:**
- `store_task()` - Stocke une tâche
- `retrieve_relevant()` - Recherche pertinente
- `extract_knowledge()` - Extrait des connaissances
- `clear()` - Efface la mémoire

### 4. Tool Registry

Registre des outils disponibles.

**Outils disponibles:**

1. **WebSearchTool**
   - Recherche sur le web
   - Extraction de contenu

2. **CodeExecutorTool**
   - Exécution de code Python
   - Sandbox sécurisé

3. **FileOperationsTool**
   - Lecture/écriture de fichiers
   - Gestion du workspace

4. **CalculatorTool**
   - Calculs mathématiques
   - Évaluation sécurisée

**Architecture d'outil:**
```python
class BaseTool(ABC):
    @property
    def description() -> str
    
    @property
    def parameters() -> Dict
    
    async def execute(**kwargs) -> Any
```

## Flux de traitement d'une tâche

```
1. Réception de la tâche
   ↓
2. Analyse par le Planner
   ├─ Analyse de la complexité
   ├─ Identification des outils nécessaires
   └─ Décomposition en étapes
   ↓
3. Création du plan d'exécution
   ├─ Étapes détaillées
   ├─ Dépendances
   └─ Estimation de durée
   ↓
4. Exécution par l'Executor
   ├─ Pour chaque étape:
   │  ├─ Utilisation d'outil ou réflexion
   │  ├─ Enregistrement du résultat
   │  └─ Gestion des erreurs
   ↓
5. Synthèse des résultats
   ├─ Agrégation des résultats
   ├─ Génération du résumé
   └─ Recommandations
   ↓
6. Stockage en mémoire
   ├─ Mémoire épisodique
   └─ Extraction de connaissances
   ↓
7. Retour au client
```

## Patterns de conception utilisés

### 1. Strategy Pattern
Utilisé pour les différents modèles d'IA (OpenAI, Anthropic).

### 2. Registry Pattern
Utilisé pour le registre d'outils.

### 3. Observer Pattern
Utilisé pour le suivi des tâches en arrière-plan.

### 4. Template Method Pattern
Utilisé dans la classe `BaseTool`.

### 5. Facade Pattern
`SintraAgent` agit comme une façade pour tous les sous-systèmes.

## Gestion d'état

### Backend
- En mémoire pour la démo
- Peut être étendu avec Redis/PostgreSQL

### Frontend
- State local avec React hooks
- Pas de state management global (suffisant pour cette taille)
- Pourrait utiliser Zustand/Redux si nécessaire

## Sécurité

### Mesures actuelles:
1. **Sandbox de code**: Vérifications basiques des imports
2. **Workspace isolé**: Fichiers limités au workspace
3. **CORS**: Configuration des origines autorisées
4. **Validation**: Pydantic pour la validation des données

### À ajouter en production:
1. Authentification (JWT, API Keys)
2. Rate limiting
3. Sandbox Docker pour l'exécution de code
4. Chiffrement des données sensibles
5. Audit logging
6. HTTPS obligatoire

## Scalabilité

### Horizontale:
- API stateless facilement réplicable
- Utiliser Redis pour le state partagé
- Load balancer devant les instances

### Verticale:
- Async/await pour les I/O
- Queue de tâches avec Celery
- Cache avec Redis

### Optimisations futures:
1. Pool de connexions pour les APIs externes
2. Cache des résultats de recherche
3. Streaming des réponses longues
4. Parallélisation des étapes indépendantes

## Monitoring et observabilité

### À implémenter:
1. Logging structuré (JSON logs)
2. Métriques (Prometheus)
3. Tracing distribué (OpenTelemetry)
4. Health checks détaillés
5. Alerting

## Tests

### Backend:
```bash
pytest tests/
```

### Frontend:
```bash
npm test
```

### Tests à implémenter:
1. Unit tests pour chaque composant
2. Integration tests pour les workflows
3. E2E tests pour l'interface
4. Load tests pour la performance

## Déploiement

### Options:

1. **VPS/Serveur dédié**
   - Backend: Gunicorn + Nginx
   - Frontend: Next.js standalone
   - Base de données: PostgreSQL

2. **Docker/Kubernetes**
   - Containers isolés
   - Orchestration automatique
   - Scaling facile

3. **Serverless**
   - Backend: AWS Lambda / Cloud Functions
   - Frontend: Vercel / Netlify
   - Base de données: Cloud SQL

4. **Platform as a Service**
   - Heroku, Railway, Render
   - Déploiement simplifié
   - Bon pour prototyping

