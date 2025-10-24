# Sintra AI - Frontend

Interface web pour Sintra AI, construite avec Next.js 14, React et TailwindCSS.

## 🚀 Démarrage

### Installation

```bash
npm install
```

### Configuration

Créez un fichier `.env.local`:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000/api
```

### Développement

```bash
npm run dev
```

L'application sera disponible sur http://localhost:3000

### Production

```bash
npm run build
npm start
```

## 📁 Structure

```
frontend/
├── app/              # Pages Next.js (App Router)
├── components/       # Composants React réutilisables
├── public/          # Assets statiques
└── styles/          # Styles globaux
```

## 🎨 Fonctionnalités

- ✅ Interface moderne et responsive
- ✅ Création et suivi de tâches en temps réel
- ✅ Visualisation de la mémoire de l'agent
- ✅ Animations fluides avec Framer Motion
- ✅ Design moderne avec TailwindCSS
- ✅ Support du mode sombre

## 🛠️ Technologies

- **Next.js 14** - Framework React
- **React 18** - Bibliothèque UI
- **TailwindCSS** - Framework CSS
- **Framer Motion** - Animations
- **Axios** - Requêtes HTTP
- **TypeScript** - Typage statique

