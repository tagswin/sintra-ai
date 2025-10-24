# 🎉 Sintra AI est maintenant lancé !

## ✅ Serveurs actifs :

- **Frontend** : http://localhost:3000
- **Backend API** : http://localhost:8000
- **Documentation API** : http://localhost:8000/docs

## ⚠️ Configuration importante :

Le backend affiche cet avertissement :
```
⚠️  Aucune clé API configurée! Configurez OPENAI_API_KEY ou ANTHROPIC_API_KEY
```

### Pour utiliser Sintra AI, ajoutez votre clé API :

1. Créez/éditez le fichier `.env` à la racine :
```bash
nano .env
```

2. Ajoutez votre clé :
```env
OPENAI_API_KEY=sk-votre-clé-openai-ici
```

3. Redémarrez le backend :
```bash
source venv/bin/activate
python main.py
```

### Obtenir une clé API :

**OpenAI (recommandé)** :
1. Allez sur https://platform.openai.com/api-keys
2. Créez un compte si nécessaire
3. Cliquez sur "Create new secret key"
4. Copiez la clé dans votre fichier `.env`

**Anthropic (alternatif)** :
1. Allez sur https://console.anthropic.com
2. Créez un compte
3. Générez une clé API
4. Utilisez `ANTHROPIC_API_KEY=` dans `.env`

## 🚀 Premiers pas :

1. Ouvrez http://localhost:3000
2. Tapez une tâche simple : "Bonjour, présente-toi"
3. Cliquez sur "🚀 Lancer la tâche"

## 📚 Documentation :

- `README.md` - Vue d'ensemble
- `QUICKSTART.md` - Guide rapide
- `docs/USAGE.md` - Utilisation détaillée
- `docs/API.md` - Documentation API

## 🔧 Commandes utiles :

```bash
# Arrêter les serveurs
pkill -f "python main.py"
pkill -f "next dev"

# Redémarrer backend
source venv/bin/activate && python main.py

# Redémarrer frontend
cd frontend && npm run dev
```

Bon coding avec Sintra AI ! 🤖
