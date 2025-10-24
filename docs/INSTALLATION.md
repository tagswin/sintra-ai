# Guide d'installation - Sintra AI

## Prérequis

- Python 3.9 ou supérieur
- Node.js 18 ou supérieur
- pip (gestionnaire de paquets Python)
- npm ou yarn (gestionnaire de paquets Node.js)

## Installation Backend

### 1. Cloner le projet

```bash
git clone <votre-repo>
cd agent\ ia
```

### 2. Créer un environnement virtuel

```bash
python -m venv venv

# Sur macOS/Linux
source venv/bin/activate

# Sur Windows
venv\Scripts\activate
```

### 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 4. Configurer les variables d'environnement

Créez un fichier `.env` à la racine du projet:

```env
# Clés API (au moins une requise)
OPENAI_API_KEY=sk-...
# OU
ANTHROPIC_API_KEY=sk-ant-...

# Configuration de l'agent
AGENT_NAME=Sintra
AGENT_MODEL=gpt-4-turbo-preview
MAX_ITERATIONS=50
TEMPERATURE=0.7

# Configuration serveur
HOST=0.0.0.0
PORT=8000
DEBUG=True

# Base de données
DATABASE_URL=sqlite:///./sintra.db
REDIS_URL=redis://localhost:6379

# Limites
MAX_TASK_DURATION=3600
MAX_CONCURRENT_TASKS=5
```

### 5. Obtenir les clés API

#### OpenAI
1. Créez un compte sur https://platform.openai.com
2. Allez dans API Keys
3. Créez une nouvelle clé
4. Copiez-la dans `.env`

#### Anthropic (optionnel)
1. Créez un compte sur https://console.anthropic.com
2. Allez dans API Keys
3. Créez une nouvelle clé
4. Copiez-la dans `.env`

### 6. Lancer le serveur

```bash
python main.py
```

Le serveur démarre sur http://localhost:8000

La documentation API est disponible sur http://localhost:8000/docs

## Installation Frontend

### 1. Aller dans le dossier frontend

```bash
cd frontend
```

### 2. Installer les dépendances

```bash
npm install
```

### 3. Configurer l'URL de l'API

Créez un fichier `.env.local`:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000/api
```

### 4. Lancer l'interface

```bash
npm run dev
```

L'interface est accessible sur http://localhost:3000

## Test de l'installation

### Test du backend

```bash
# Mode démonstration
python main.py demo
```

### Test de l'API

```bash
curl http://localhost:8000/health
```

Vous devriez recevoir:
```json
{
  "status": "healthy",
  "service": "Sintra AI"
}
```

### Test du frontend

Ouvrez http://localhost:3000 dans votre navigateur.

## Dépannage

### Erreur: "No module named 'openai'"

```bash
pip install -r requirements.txt
```

### Erreur: "OPENAI_API_KEY not found"

Vérifiez que le fichier `.env` existe et contient votre clé API.

### Le frontend ne se connecte pas au backend

1. Vérifiez que le backend est lancé sur le port 8000
2. Vérifiez l'URL dans `.env.local` du frontend
3. Vérifiez les CORS si vous utilisez un domaine différent

### Erreur de port déjà utilisé

Changez le port dans `.env`:
```env
PORT=8001
```

## Installation en production

### Backend

```bash
# Installer gunicorn
pip install gunicorn

# Lancer avec gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### Frontend

```bash
cd frontend

# Build de production
npm run build

# Lancer en production
npm start
```

## Docker (optionnel)

Un Dockerfile sera fourni dans une version future pour faciliter le déploiement.

## Besoin d'aide ?

- Consultez la documentation complète dans `/docs`
- Ouvrez une issue sur GitHub
- Consultez les logs dans le terminal

