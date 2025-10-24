#!/bin/bash

# Script d'installation automatique pour Sintra AI
# Usage: bash setup.sh

echo "================================================"
echo "   🤖 Installation de Sintra AI"
echo "================================================"
echo ""

# Couleurs pour l'affichage
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Vérifier Python
echo "📦 Vérification des prérequis..."
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 n'est pas installé${NC}"
    echo "Installez Python 3.9+ depuis https://python.org"
    exit 1
fi

echo -e "${GREEN}✅ Python trouvé: $(python3 --version)${NC}"

# Vérifier Node.js
if ! command -v node &> /dev/null; then
    echo -e "${YELLOW}⚠️  Node.js n'est pas installé (optionnel pour le frontend)${NC}"
else
    echo -e "${GREEN}✅ Node.js trouvé: $(node --version)${NC}"
fi

# Créer l'environnement virtuel
echo ""
echo "🔧 Création de l'environnement virtuel..."
python3 -m venv venv

if [ $? -ne 0 ]; then
    echo -e "${RED}❌ Échec de la création de l'environnement virtuel${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Environnement virtuel créé${NC}"

# Activer l'environnement virtuel
echo "🔧 Activation de l'environnement virtuel..."
source venv/bin/activate

# Installer les dépendances Python
echo ""
echo "📦 Installation des dépendances Python..."
pip install --upgrade pip
pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo -e "${RED}❌ Échec de l'installation des dépendances${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Dépendances Python installées${NC}"

# Créer le fichier .env s'il n'existe pas
if [ ! -f .env ]; then
    echo ""
    echo "🔑 Configuration de l'environnement..."
    
    read -p "Entrez votre clé API OpenAI (ou laissez vide): " openai_key
    read -p "Entrez votre clé API Anthropic (ou laissez vide): " anthropic_key
    
    cat > .env << EOF
# Configuration Sintra AI

# Clés API (au moins une requise)
OPENAI_API_KEY=${openai_key}
ANTHROPIC_API_KEY=${anthropic_key}

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
EOF
    
    echo -e "${GREEN}✅ Fichier .env créé${NC}"
else
    echo -e "${YELLOW}⚠️  Fichier .env existant conservé${NC}"
fi

# Installer le frontend si Node.js est disponible
if command -v node &> /dev/null; then
    echo ""
    echo "📦 Installation du frontend..."
    cd frontend
    npm install
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ Frontend installé${NC}"
        
        # Créer .env.local pour le frontend
        if [ ! -f .env.local ]; then
            echo "NEXT_PUBLIC_API_URL=http://localhost:8000/api" > .env.local
            echo -e "${GREEN}✅ Configuration frontend créée${NC}"
        fi
    else
        echo -e "${YELLOW}⚠️  Installation du frontend échouée (non critique)${NC}"
    fi
    cd ..
fi

# Créer le dossier workspace
mkdir -p workspace

echo ""
echo "================================================"
echo -e "${GREEN}✅ Installation terminée avec succès!${NC}"
echo "================================================"
echo ""
echo "🚀 Pour démarrer Sintra AI:"
echo ""
echo "   1. Activez l'environnement virtuel:"
echo "      source venv/bin/activate"
echo ""
echo "   2. Lancez le backend:"
echo "      python main.py"
echo ""
if command -v node &> /dev/null; then
    echo "   3. Dans un autre terminal, lancez le frontend:"
    echo "      cd frontend && npm run dev"
    echo ""
fi
echo "   4. Ouvrez http://localhost:3000 dans votre navigateur"
echo ""
echo "📚 Documentation: docs/"
echo "🌐 API Docs: http://localhost:8000/docs"
echo ""
echo "Besoin d'aide? Consultez QUICKSTART.md"
echo ""

