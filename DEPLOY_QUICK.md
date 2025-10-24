# 🚀 Déploiement Rapide - 5 Minutes

## Étape 1 : GitHub (2 min)

```bash
cd "/Users/teddy-vann/Desktop/agent ia"

# Initialiser Git
git init
git add .
git commit -m "🚀 Initial commit"

# Créer un repo sur github.com puis :
git remote add origin https://github.com/VOTRE_USERNAME/sintra-ai.git
git push -u origin main
```

## Étape 2 : Frontend sur Vercel (1 min)

1. Aller sur [vercel.com](https://vercel.com)
2. Se connecter avec GitHub
3. "New Project" → Import `sintra-ai`
4. **Root Directory** : `frontend`
5. **Environment Variable** :
   ```
   NEXT_PUBLIC_API_URL=https://votre-backend.railway.app/api
   ```
   (mettre l'URL Railway après étape 3)
6. Deploy

✅ Frontend en ligne !

## Étape 3 : Backend sur Railway (2 min)

1. Aller sur [railway.app](https://railway.app)
2. Se connecter avec GitHub
3. "New Project" → Deploy from GitHub
4. Sélectionner `sintra-ai`
5. **Variables d'environnement** :
   ```
   OPENAI_API_KEY=votre-clé
   PORT=8000
   ENVIRONMENT=production
   ```
6. Deploy

✅ Backend en ligne !

## Étape 4 : Connecter les deux

1. **Copier l'URL** du backend Railway
2. **Retourner sur Vercel** → Settings → Environment Variables
3. **Modifier** `NEXT_PUBLIC_API_URL` avec l'URL Railway
4. **Redéployer** le frontend

## ✅ C'est Fait !

Votre site est en ligne sur :
- Frontend : `https://votre-projet.vercel.app`
- Backend : `https://votre-projet.railway.app`

## 🔄 Pour Modifier avec l'IA

```bash
# 1. Modifier le code avec l'assistant IA
# 2. Tester en local
# 3. Pousser les changements :
git add .
git commit -m "Description des changements"
git push
```

**Le déploiement est automatique !** 🎉

