"""
Intégrations pour le SEO
"""

from typing import Dict, Any, List
from .base import BaseIntegration


class GoogleSearchConsoleIntegration(BaseIntegration):
    """Intégration Google Search Console"""
    
    def __init__(self):
        super().__init__(
            name="Google Search Console",
            icon="🔍",
            description="Analyser les performances de recherche"
        )
        self.base_url = "https://www.googleapis.com/webmasters/v3"
    
    def get_required_credentials(self) -> List[Dict[str, str]]:
        return [
            {"name": "client_id", "label": "Client ID", "type": "text", "required": True},
            {"name": "client_secret", "label": "Client Secret", "type": "password", "required": True},
            {"name": "site_url", "label": "Site URL", "type": "url", "required": True}
        ]
    
    async def get_search_analytics(self, days: int = 30) -> Dict[str, Any]:
        """Récupère les analytics de recherche"""
        return {
            "clicks": 0,
            "impressions": 0,
            "ctr": 0.0,
            "position": 0.0
        }


class SEMrushIntegration(BaseIntegration):
    """Intégration SEMrush API"""
    
    def __init__(self):
        super().__init__(
            name="SEMrush",
            icon="📈",
            description="Recherche de mots-clés et analyse de concurrence"
        )
        self.base_url = "https://api.semrush.com"
    
    def get_required_credentials(self) -> List[Dict[str, str]]:
        return [
            {"name": "api_key", "label": "API Key", "type": "password", "required": True}
        ]
    
    async def keyword_research(self, keyword: str, database: str = "us") -> Dict[str, Any]:
        """Recherche de mots-clés"""
        return {
            "keyword": keyword,
            "volume": 0,
            "difficulty": 0,
            "cpc": 0.0
        }


class AhrefsIntegration(BaseIntegration):
    """Intégration Ahrefs API"""
    
    def __init__(self):
        super().__init__(
            name="Ahrefs",
            icon="🔗",
            description="Analyse de backlinks et audit SEO"
        )
        self.base_url = "https://api.ahrefs.com/v3"
    
    def get_required_credentials(self) -> List[Dict[str, str]]:
        return [
            {"name": "api_key", "label": "API Key", "type": "password", "required": True}
        ]
    
    async def get_backlinks(self, domain: str) -> Dict[str, Any]:
        """Récupère les backlinks d'un domaine"""
        return {
            "total_backlinks": 0,
            "referring_domains": 0,
            "domain_rating": 0
        }

