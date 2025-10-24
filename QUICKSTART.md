# 🚀 Démarrage Rapide - Sintra AI

## Installation en 5 minutes

### 1. Prérequis

- Python 3.9+
- Node.js 18+
- Une clé API OpenAI ou Anthropic

### 2. Installation Backend

```bash
# Cloner et entrer dans le projet
cd "agent ia"

# Créer l'environnement virtuel
python -m venv venv

# Activer l'environnement (macOS/Linux)
source venv/bin/activate

# Activer l'environnement (Windows)
# venv\Scripts\activate

# Installer les dépendances
pip install -r requirements.txt

# Configurer les clés API
# Créez un fichier .env et ajoutez:
echo "OPENAI_API_KEY=votre_clé_ici" > .env
```

### 3. Installation Frontend

```bash
# Aller dans le dossier frontend
cd frontend

# Installer les dépendances
npm install

# Retourner à la racine
cd ..
```

### 4. Lancement

**Terminal 1 - Backend:**
```bash
python main.py
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

### 5. Accès

- **Interface Web:** http://localhost:3000
- **API Documentation:** http://localhost:8000/docs
- **API:** http://localhost:8000/api

## Premier Test

### Via l'interface web

1. Ouvrez http://localhost:3000
2. Tapez: "Calcule 15 + 27 et explique le résultat"
3. Cliquez sur "🚀 Lancer la tâche"
4. Observez l'agent travailler!

### Via l'API

```bash
curl -X POST http://localhost:8000/api/think \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Quelle est la capitale de la France ?"}'
```

### Via le mode démo

```bash
python main.py demo
```

## Exemples de Tâches

```
✅ "Recherche les dernières tendances en IA"
✅ "Calcule (123 + 456) * 2"
✅ "Crée un plan pour apprendre Python en 30 jours"
✅ "Compare React et Vue.js"
✅ "Écris un script Python pour trier une liste"
```

## Obtenir une Clé API

### OpenAI (Recommandé)

1. Allez sur https://platform.openai.com
2. Créez un compte
3. Section "API Keys"
4. "Create new secret key"
5. Copiez dans `.env`

### Anthropic (Alternatif)

1. Allez sur https://console.anthropic.com
2. Créez un compte
3. Section "API Keys"
4. "Create Key"
5. Copiez dans `.env`

## Configuration Minimale (.env)

```env
OPENAI_API_KEY=sk-...
AGENT_MODEL=gpt-4-turbo-preview
DEBUG=True
HOST=0.0.0.0
PORT=8000
```

## Structure du Projet

```
agent ia/
├── core/              # 🧠 Moteur de l'agent
├── tools/             # 🔧 Outils disponibles
├── api/               # 🌐 API REST
├── frontend/          # 💻 Interface web
├── docs/              # 📚 Documentation
├── main.py            # 🚀 Point d'entrée
└── requirements.txt   # 📦 Dépendances
```

## Commandes Utiles

```bash
# Lancer le backend
python main.py

# Mode démonstration
python main.py demo

# Lancer le frontend (dans /frontend)
npm run dev

# Build production frontend
npm run build

# Voir les logs en direct
tail -f *.log
```

## Dépannage Rapide

### ❌ "OPENAI_API_KEY not found"
→ Créez le fichier `.env` avec votre clé API

### ❌ "ModuleNotFoundError"
→ Activez l'environnement virtuel: `source venv/bin/activate`

### ❌ "Port already in use"
→ Changez le port dans `.env`: `PORT=8001`

### ❌ Frontend ne se connecte pas
→ Vérifiez que le backend tourne sur le port 8000

## Prochaines Étapes

1. 📖 Lisez [USAGE.md](docs/USAGE.md) pour des exemples détaillés
2. 🏗️ Consultez [ARCHITECTURE.md](docs/ARCHITECTURE.md) pour comprendre le système
3. 🔧 Voir [API.md](docs/API.md) pour l'intégration API
4. 📚 Documentation complète dans `/docs`

## Support

- 📝 Documentation complète: `/docs`
- 🌐 API interactive: http://localhost:8000/docs
- 💬 Questions? Ouvrez une issue

## Licence

MIT License - Voir [LICENSE](LICENSE)

---

**Prêt à commencer? Lancez `python main.py` et ouvrez http://localhost:3000! 🎉**

