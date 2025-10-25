"""
Intégrations pour le contenu et le copywriting
"""

from typing import Dict, Any, List
from .base import BaseIntegration


class GrammarlyIntegration(BaseIntegration):
    """Intégration Grammarly"""
    
    def __init__(self):
        super().__init__(
            name="Grammarly",
            icon="✍️",
            description="Vérification grammaticale et amélioration du style"
        )
    
    def get_required_credentials(self) -> List[Dict[str, str]]:
        return [
            {"name": "api_key", "label": "API Key", "type": "password", "required": True}
        ]
    
    async def check_text(self, text: str) -> Dict[str, Any]:
        """Vérifie un texte"""
        return {
            "corrections": [],
            "score": 100
        }


class CopyAIIntegration(BaseIntegration):
    """Intégration Copy.ai"""
    
    def __init__(self):
        super().__init__(
            name="Copy.ai",
            icon="🤖",
            description="Génération de contenu marketing"
        )
    
    def get_required_credentials(self) -> List[Dict[str, str]]:
        return [
            {"name": "api_key", "label": "API Key", "type": "password", "required": True}
        ]


class JasperIntegration(BaseIntegration):
    """Intégration Jasper AI"""
    
    def __init__(self):
        super().__init__(
            name="Jasper",
            icon="💎",
            description="Assistant de copywriting IA"
        )
    
    def get_required_credentials(self) -> List[Dict[str, str]]:
        return [
            {"name": "api_key", "label": "API Key", "type": "password", "required": True}
        ]

