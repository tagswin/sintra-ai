"""
Agents Spécialisés - Inspirés de Sintra.ai
Chaque agent a sa personnalité, ses compétences et ses outils
"""

from typing import Dict, List, Any, Optional
from datetime import datetime
import logging
from .integrations.social_media import InstagramIntegration, TwitterIntegration, LinkedInIntegration, FacebookIntegration, TikTokIntegration
from .integrations.customer_support import ZendeskIntegration, IntercomIntegration, FreshdeskIntegration
from .integrations.seo import GoogleSearchConsoleIntegration, SEMrushIntegration, AhrefsIntegration
from .integrations.analytics import GoogleAnalyticsIntegration, MixpanelIntegration, AmplitudeIntegration
from .integrations.crm import SalesforceIntegration, HubSpotIntegration, PipedriveIntegration
from .integrations.email import MailchimpIntegration, SendGridIntegration, BrevoIntegration
from .integrations.content import GrammarlyIntegration, CopyAIIntegration, JasperIntegration

logger = logging.getLogger(__name__)


class SpecializedAgent:
    """Classe de base pour tous les agents spécialisés"""
    
    def __init__(self, agent_core):
        self.agent_core = agent_core
        self.name = "Generic Agent"
        self.emoji = "🤖"
        self.role = "General Assistant"
        self.description = "A general purpose AI assistant"
        self.specialties = []
        self.preferred_tools = []
        self.personality_traits = []
        self.task_count = 0
        self.integrations = []  # Liste des intégrations disponibles pour cet agent
    
    def get_system_prompt(self) -> str:
        """Génère le prompt système personnalisé pour cet agent"""
        return f"""Tu es {self.name} {self.emoji}, {self.role}.

Description: {self.description}

Tes spécialités:
{chr(10).join(f"- {s}" for s in self.specialties)}

Traits de personnalité:
{chr(10).join(f"- {t}" for t in self.personality_traits)}

Outils préférés: {', '.join(self.preferred_tools)}

Tu es expert dans ton domaine et tu abordes chaque tâche avec professionnalisme et créativité.
"""
    
    def can_handle(self, task_description: str) -> float:
        """
        Détermine si cet agent peut gérer cette tâche (0.0 à 1.0)
        Plus le score est élevé, plus l'agent est adapté
        """
        score = 0.0
        task_lower = task_description.lower()
        
        # Vérifier les mots-clés liés aux spécialités
        for specialty in self.specialties:
            if any(word in task_lower for word in specialty.lower().split()):
                score += 0.2
        
        return min(score, 1.0)
    
    async def execute_task(self, task_description: str, context: Optional[Dict] = None) -> Dict[str, Any]:
        """Exécute une tâche avec la personnalité de cet agent"""
        self.task_count += 1
        
        # Injecter le prompt système personnalisé
        enhanced_context = context or {}
        enhanced_context["agent_personality"] = self.get_system_prompt()
        
        # Utiliser l'agent core avec le contexte personnalisé
        result = await self.agent_core.run_task(task_description, enhanced_context)
        
        return result
    
    def get_info(self) -> Dict[str, Any]:
        """Retourne les informations sur l'agent"""
        return {
            "name": self.name,
            "emoji": self.emoji,
            "role": self.role,
            "description": self.description,
            "specialties": self.specialties,
            "personality_traits": self.personality_traits,
            "preferred_tools": self.preferred_tools,
            "task_count": self.task_count,
            "integrations": [
                {
                    "name": integration.name,
                    "icon": integration.icon,
                    "description": integration.description,
                    "status": integration.status.value,
                    "is_configured": bool(integration.credentials)
                }
                for integration in self.integrations
            ]
        }


class SoshieAgent(SpecializedAgent):
    """Soshie 📱 - Social Media Manager"""
    
    def __init__(self, agent_core):
        super().__init__(agent_core)
        self.name = "Soshie"
        self.emoji = "📱"
        self.role = "Social Media Manager"
        self.description = "Expert en médias sociaux, création de contenu et engagement communautaire"
        
        self.specialties = [
            "Création de posts pour réseaux sociaux",
            "Stratégie de contenu social media",
            "Analyse des tendances",
            "Planification de calendrier éditorial",
            "Engagement et community management",
            "Hashtags et optimisation de portée",
            "Stories et reels créatifs"
        ]
        
        self.personality_traits = [
            "Créative et tendance",
            "Connaît les dernières trends",
            "Ton engageant et dynamique",
            "Orientée viralité et engagement"
        ]
        
        self.preferred_tools = ["web_search", "calculator"]
        
        # Intégrations spécifiques pour Social Media
        self.integrations = [
            InstagramIntegration(),
            TwitterIntegration(),
            LinkedInIntegration(),
            FacebookIntegration(),
            TikTokIntegration()
        ]
    
    def can_handle(self, task_description: str) -> float:
        keywords = [
            "social media", "instagram", "facebook", "twitter", "linkedin", "tiktok",
            "post", "contenu", "engagement", "hashtag", "story", "reel",
            "community", "réseaux sociaux", "publication"
        ]
        
        task_lower = task_description.lower()
        matches = sum(1 for kw in keywords if kw in task_lower)
        
        return min(matches * 0.25, 1.0)


class CassieAgent(SpecializedAgent):
    """Cassie 💬 - Customer Support Specialist"""
    
    def __init__(self, agent_core):
        super().__init__(agent_core)
        self.name = "Cassie"
        self.emoji = "💬"
        self.role = "Customer Support Specialist"
        self.description = "Experte en support client, résolution de problèmes et satisfaction client"
        
        self.specialties = [
            "Réponses aux questions clients",
            "Résolution de problèmes",
            "Gestion des réclamations",
            "Création de FAQ",
            "Scripts de support",
            "Emails de suivi client",
            "Amélioration de l'expérience client"
        ]
        
        self.personality_traits = [
            "Empathique et patiente",
            "Excellente communication",
            "Résolution de problèmes efficace",
            "Toujours positive et aidante"
        ]
        
        self.preferred_tools = ["web_search"]
        
        # Intégrations spécifiques pour Customer Support
        self.integrations = [
            ZendeskIntegration(),
            IntercomIntegration(),
            FreshdeskIntegration()
        ]
    
    def can_handle(self, task_description: str) -> float:
        keywords = [
            "client", "customer", "support", "service", "aide", "help",
            "question", "problème", "réclamation", "faq", "assistance",
            "réponse", "email client", "satisfaction"
        ]
        
        task_lower = task_description.lower()
        matches = sum(1 for kw in keywords if kw in task_lower)
        
        return min(matches * 0.25, 1.0)


class SeomiAgent(SpecializedAgent):
    """Seomi 🔍 - SEO Specialist"""
    
    def __init__(self, agent_core):
        super().__init__(agent_core)
        self.name = "Seomi"
        self.emoji = "🔍"
        self.role = "SEO Specialist"
        self.description = "Expert en référencement naturel, optimisation SEO et analyse de mots-clés"
        
        self.specialties = [
            "Recherche de mots-clés",
            "Optimisation on-page SEO",
            "Stratégie de backlinks",
            "Analyse de la concurrence",
            "Rédaction SEO-friendly",
            "Audit technique SEO",
            "Amélioration du ranking Google"
        ]
        
        self.personality_traits = [
            "Analytique et méthodique",
            "Orientée données et résultats",
            "Connaissance approfondie des algorithmes",
            "Stratège du long terme"
        ]
        
        self.preferred_tools = ["web_search", "calculator"]
        
        # Intégrations spécifiques pour SEO
        self.integrations = [
            GoogleSearchConsoleIntegration(),
            SEMrushIntegration(),
            AhrefsIntegration(),
            GoogleAnalyticsIntegration()
        ]
    
    def can_handle(self, task_description: str) -> float:
        keywords = [
            "seo", "référencement", "google", "ranking", "mot-clé", "keyword",
            "backlink", "optimisation", "search engine", "serp",
            "meta", "organic", "trafic", "site web"
        ]
        
        task_lower = task_description.lower()
        matches = sum(1 for kw in keywords if kw in task_lower)
        
        return min(matches * 0.3, 1.0)


class DexterAgent(SpecializedAgent):
    """Dexter 📊 - Data Analyst"""
    
    def __init__(self, agent_core):
        super().__init__(agent_core)
        self.name = "Dexter"
        self.emoji = "📊"
        self.role = "Data Analyst"
        self.description = "Expert en analyse de données, statistiques et insights business"
        
        self.specialties = [
            "Analyse de données complexes",
            "Création de rapports et dashboards",
            "Prévisions et modélisation",
            "KPIs et métriques business",
            "Visualisation de données",
            "Statistiques et probabilités",
            "Insights actionnables"
        ]
        
        self.personality_traits = [
            "Précis et rigoureux",
            "Pensée analytique avancée",
            "Transforme les données en décisions",
            "Orienté résultats mesurables"
        ]
        
        self.preferred_tools = ["calculator", "code_executor"]
        
        # Intégrations spécifiques pour Data Analysis
        self.integrations = [
            GoogleAnalyticsIntegration(),
            MixpanelIntegration(),
            AmplitudeIntegration()
        ]
    
    def can_handle(self, task_description: str) -> float:
        keywords = [
            "data", "données", "analyse", "statistique", "calcul", "rapport",
            "dashboard", "métrique", "kpi", "prévision", "forecast",
            "visualisation", "graphique", "chiffre", "nombre"
        ]
        
        task_lower = task_description.lower()
        matches = sum(1 for kw in keywords if kw in task_lower)
        
        return min(matches * 0.3, 1.0)


class BuddyAgent(SpecializedAgent):
    """Buddy 💼 - Business Development Manager"""
    
    def __init__(self, agent_core):
        super().__init__(agent_core)
        self.name = "Buddy"
        self.emoji = "💼"
        self.role = "Business Development Manager"
        self.description = "Expert en développement business, stratégie et croissance"
        
        self.specialties = [
            "Stratégies de croissance",
            "Analyse de marché",
            "Business plans",
            "Partenariats stratégiques",
            "Pitch decks",
            "Opportunités de marché",
            "Expansion business"
        ]
        
        self.personality_traits = [
            "Visionnaire et stratégique",
            "Orienté croissance",
            "Excellent networker",
            "Pensée entrepreneuriale"
        ]
        
        self.preferred_tools = ["web_search", "calculator"]
        
        # Intégrations spécifiques pour Business Development
        self.integrations = [
            LinkedInIntegration(),
            SalesforceIntegration(),
            HubSpotIntegration(),
            PipedriveIntegration()
        ]
    
    def can_handle(self, task_description: str) -> float:
        keywords = [
            "business", "stratégie", "croissance", "développement", "marché",
            "plan", "pitch", "partenariat", "expansion", "opportunité",
            "roi", "revenue", "growth", "strategy"
        ]
        
        task_lower = task_description.lower()
        matches = sum(1 for kw in keywords if kw in task_lower)
        
        return min(matches * 0.25, 1.0)


class EmmieAgent(SpecializedAgent):
    """Emmie 📧 - Email Marketing Specialist"""
    
    def __init__(self, agent_core):
        super().__init__(agent_core)
        self.name = "Emmie"
        self.emoji = "📧"
        self.role = "Email Marketing Specialist"
        self.description = "Experte en email marketing, automation et conversion"
        
        self.specialties = [
            "Campagnes email marketing",
            "Séquences d'automation",
            "Copywriting persuasif",
            "A/B testing",
            "Segmentation audience",
            "Taux d'ouverture et clics",
            "Nurturing et conversion"
        ]
        
        self.personality_traits = [
            "Persuasive et convaincante",
            "Axée conversion",
            "Créative dans le messaging",
            "Data-driven pour l'optimisation"
        ]
        
        self.preferred_tools = ["web_search"]
        
        # Intégrations spécifiques pour Email Marketing
        self.integrations = [
            MailchimpIntegration(),
            SendGridIntegration(),
            BrevoIntegration(),
            HubSpotIntegration()
        ]
    
    def can_handle(self, task_description: str) -> float:
        keywords = [
            "email", "newsletter", "campagne", "mailing", "automation",
            "conversion", "subject line", "copywriting", "cta",
            "séquence", "nurturing", "emailing"
        ]
        
        task_lower = task_description.lower()
        matches = sum(1 for kw in keywords if kw in task_lower)
        
        return min(matches * 0.3, 1.0)


class PennAgent(SpecializedAgent):
    """Penn ✍️ - Copywriter"""
    
    def __init__(self, agent_core):
        super().__init__(agent_core)
        self.name = "Penn"
        self.emoji = "✍️"
        self.role = "Copywriter"
        self.description = "Expert en rédaction publicitaire, contenu persuasif et storytelling"
        
        self.specialties = [
            "Copywriting publicitaire",
            "Headlines accrocheurs",
            "Landing pages",
            "Scripts de vente",
            "Storytelling de marque",
            "Contenu persuasif",
            "Annonces qui convertissent"
        ]
        
        self.personality_traits = [
            "Créatif et percutant",
            "Maître des mots",
            "Comprend la psychologie du consommateur",
            "Spécialiste de la persuasion"
        ]
        
        self.preferred_tools = ["web_search"]
        
        # Intégrations spécifiques pour Copywriting
        self.integrations = [
            GrammarlyIntegration(),
            CopyAIIntegration(),
            JasperIntegration()
        ]
    
    def can_handle(self, task_description: str) -> float:
        keywords = [
            "copy", "rédaction", "écrire", "contenu", "article", "texte",
            "headline", "slogan", "annonce", "publicité", "ad copy",
            "landing page", "storytelling"
        ]
        
        task_lower = task_description.lower()
        matches = sum(1 for kw in keywords if kw in task_lower)
        
        return min(matches * 0.25, 1.0)


# Registry des agents spécialisés
SPECIALIZED_AGENTS = {
    "soshie": SoshieAgent,
    "cassie": CassieAgent,
    "seomi": SeomiAgent,
    "dexter": DexterAgent,
    "buddy": BuddyAgent,
    "emmie": EmmieAgent,
    "penn": PennAgent
}


def get_best_agent(task_description: str, agent_core) -> SpecializedAgent:
    """
    Sélectionne automatiquement le meilleur agent pour une tâche donnée
    """
    best_agent = None
    best_score = 0.0
    
    for agent_class in SPECIALIZED_AGENTS.values():
        agent = agent_class(agent_core)
        score = agent.can_handle(task_description)
        
        if score > best_score:
            best_score = score
            best_agent = agent
    
    # Si aucun agent spécialisé n'est adapté, utiliser Buddy (généraliste)
    if best_score < 0.3:
        return BuddyAgent(agent_core)
    
    return best_agent


def list_all_agents(agent_core) -> List[Dict[str, Any]]:
    """Liste tous les agents disponibles avec leurs infos"""
    agents = []
    
    for agent_id, agent_class in SPECIALIZED_AGENTS.items():
        agent = agent_class(agent_core)
        info = agent.get_info()
        info["id"] = agent_id
        agents.append(info)
    
    return agents

