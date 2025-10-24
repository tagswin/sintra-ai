# 🤖 Agents Spécialisés - Sintra AI

## ✅ Intégration complète réussie !

Votre système Sintra AI dispose maintenant de **7 agents spécialisés**, chacun avec ses propres compétences et personnalité.

## 👥 Les Agents Disponibles

### 1. **Soshie** 📱 - Social Media Manager
**Rôle:** Experte en médias sociaux et création de contenu

**Spécialités:**
- Création de posts pour réseaux sociaux
- Stratégie de contenu social media
- Analyse des tendances
- Planification de calendrier éditorial
- Engagement et community management
- Hashtags et optimisation de portée
- Stories et reels créatifs

**Personnalité:** Créative, tendance, dynamique, orientée viralité

---

### 2. **Cassie** 💬 - Customer Support Specialist
**Rôle:** Experte en support client et satisfaction

**Spécialités:**
- Réponses aux questions clients
- Résolution de problèmes
- Gestion des réclamations
- Création de FAQ
- Scripts de support
- Emails de suivi client
- Amélioration de l'expérience client

**Personnalité:** Empathique, patiente, communicante, toujours positive

---

### 3. **Seomi** 🔍 - SEO Specialist
**Rôle:** Expert en référencement naturel

**Spécialités:**
- Recherche de mots-clés
- Optimisation on-page SEO
- Stratégie de backlinks
- Analyse de la concurrence
- Rédaction SEO-friendly
- Audit technique SEO
- Amélioration du ranking Google

**Personnalité:** Analytique, méthodique, orientée données, stratège

---

### 4. **Dexter** 📊 - Data Analyst
**Rôle:** Expert en analyse de données

**Spécialités:**
- Analyse de données complexes
- Création de rapports et dashboards
- Prévisions et modélisation
- KPIs et métriques business
- Visualisation de données
- Statistiques et probabilités
- Insights actionnables

**Personnalité:** Précis, rigoureux, analytique, orienté résultats

---

### 5. **Buddy** 💼 - Business Development Manager
**Rôle:** Expert en développement business

**Spécialités:**
- Stratégies de croissance
- Analyse de marché
- Business plans
- Partenariats stratégiques
- Pitch decks
- Opportunités de marché
- Expansion business

**Personnalité:** Visionnaire, stratégique, networker, entrepreneurial

---

### 6. **Emmie** 📧 - Email Marketing Specialist
**Rôle:** Experte en email marketing

**Spécialités:**
- Campagnes email marketing
- Séquences d'automation
- Copywriting persuasif
- A/B testing
- Segmentation audience
- Taux d'ouverture et clics
- Nurturing et conversion

**Personnalité:** Persuasive, convaincante, créative, data-driven

---

### 7. **Penn** ✍️ - Copywriter
**Rôle:** Expert en rédaction publicitaire

**Spécialités:**
- Copywriting publicitaire
- Headlines accrocheurs
- Landing pages
- Scripts de vente
- Storytelling de marque
- Contenu persuasif
- Annonces qui convertissent

**Personnalité:** Créatif, percutant, maître des mots, persuasif

---

## 🎯 Comment utiliser les agents

### 1. **Sélection manuelle**
Dans l'interface, choisissez l'agent qui correspond à votre besoin avant de lancer une tâche.

### 2. **Sélection automatique** (recommandé)
Laissez "Auto" activé et le système choisira automatiquement l'agent le plus adapté à votre tâche.

### 3. **Via l'API**
```bash
curl -X POST http://localhost:8000/api/tasks \
  -H "Content-Type: application/json" \
  -d '{
    "description": "Crée 5 posts Instagram pour mon produit",
    "agent_id": "soshie"
  }'
```

## 📋 Exemples de tâches par agent

### Soshie (Social Media)
```
"Crée 5 posts Instagram pour ma startup tech"
"Génère des idées de stories pour promouvoir mon événement"
"Analyse les tendances TikTok dans mon secteur"
```

### Cassie (Customer Support)
```
"Rédige une réponse à une réclamation client"
"Crée une FAQ pour mon service de livraison"
"Écris un email d'excuses pour un retard de commande"
```

### Seomi (SEO)
```
"Optimise ma page produit pour le SEO"
"Trouve les meilleurs mots-clés pour mon blog tech"
"Analyse le SEO de mon concurrent principal"
```

### Dexter (Data Analysis)
```
"Analyse mes données de ventes du mois"
"Crée un rapport sur mes KPIs marketing"
"Prévois les ventes du prochain trimestre"
```

### Buddy (Business Development)
```
"Crée un business plan pour mon idée de startup"
"Analyse le marché de la livraison de nourriture"
"Rédige un pitch deck pour mes investisseurs"
```

### Emmie (Email Marketing)
```
"Crée une séquence d'emails de bienvenue"
"Rédige un email de relance pour paniers abandonnés"
"Optimise mes subject lines pour augmenter l'ouverture"
```

### Penn (Copywriting)
```
"Écris une landing page pour mon cours en ligne"
"Crée un slogan accrocheur pour ma marque"
"Rédige une annonce Facebook qui convertit"
```

## 🔧 API Endpoints

### Lister tous les agents
```bash
GET http://localhost:8000/api/agents
```

### Détails d'un agent
```bash
GET http://localhost:8000/api/agents/soshie
```

### Créer une tâche avec un agent spécifique
```bash
POST http://localhost:8000/api/tasks
{
  "description": "Votre tâche",
  "agent_id": "soshie"  // ou null pour auto-sélection
}
```

## 🎨 Interface

### Nouvelle interface de sélection
- **Sélecteur visuel** avec emoji et description de chaque agent
- **Auto-sélection intelligente** basée sur les mots-clés de la tâche
- **Affichage de l'agent** dans l'historique des tâches
- **Page dédiée** présentant tous les agents avec leurs détails

### Navigation
1. **Onglet Tâches** : Créez des tâches et sélectionnez votre agent
2. **Onglet À propos** : Découvrez tous les agents disponibles

## 🚀 Architecture Technique

### Backend
- `core/specialized_agents.py` - Classes des agents spécialisés
- `api/routes.py` - Endpoints API pour les agents
- Auto-routing intelligent basé sur l'analyse sémantique

### Frontend
- `components/AgentSelector.tsx` - Sélecteur d'agent
- `components/AgentsGallery.tsx` - Galerie de présentation
- `components/TaskList.tsx` - Affichage de l'agent dans les tâches

## ✨ Fonctionnalités

✅ **7 agents spécialisés** avec personnalités uniques
✅ **Auto-sélection intelligente** de l'agent adapté
✅ **Sélection manuelle** pour un contrôle total
✅ **Historique** montrant quel agent a traité chaque tâche
✅ **Page de présentation** avec tous les détails des agents
✅ **API complète** pour l'intégration
✅ **Interface moderne** avec animations

## 🎯 Prochaines étapes

Pour configurer les agents plus en détail, vous pouvez :

1. **Personnaliser les prompts** dans `core/specialized_agents.py`
2. **Ajouter des outils spécifiques** à chaque agent
3. **Créer de nouveaux agents** en suivant le modèle existant
4. **Affiner l'auto-sélection** en ajustant les mots-clés

## 📊 Statistiques

Chaque agent garde un compteur de tâches complétées, visible dans l'interface.

Bon travail avec vos nouveaux agents spécialisés ! 🎉

