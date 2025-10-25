"""
Intégrations pour le support client
"""

from typing import Dict, Any, List
from .base import BaseIntegration


class ZendeskIntegration(BaseIntegration):
    """Intégration Zendesk Support"""
    
    def __init__(self):
        super().__init__(
            name="Zendesk",
            icon="💬",
            description="Gérer les tickets de support et la base de connaissances"
        )
    
    def get_required_credentials(self) -> List[Dict[str, str]]:
        return [
            {"name": "subdomain", "label": "Zendesk Subdomain", "type": "text", "required": True},
            {"name": "email", "label": "Email", "type": "email", "required": True},
            {"name": "api_token", "label": "API Token", "type": "password", "required": True}
        ]
    
    async def get_tickets(self, status: str = "open") -> List[Dict[str, Any]]:
        """Récupère les tickets"""
        return []
    
    async def create_ticket(self, subject: str, description: str, priority: str = "normal") -> Dict[str, Any]:
        """Crée un nouveau ticket"""
        return {"success": True, "ticket_id": "mock_123"}
    
    async def update_ticket(self, ticket_id: str, comment: str) -> Dict[str, Any]:
        """Met à jour un ticket"""
        return {"success": True}


class IntercomIntegration(BaseIntegration):
    """Intégration Intercom"""
    
    def __init__(self):
        super().__init__(
            name="Intercom",
            icon="💭",
            description="Messagerie client et automation"
        )
        self.base_url = "https://api.intercom.io"
    
    def get_required_credentials(self) -> List[Dict[str, str]]:
        return [
            {"name": "access_token", "label": "Access Token", "type": "password", "required": True}
        ]
    
    async def send_message(self, user_id: str, message: str) -> Dict[str, Any]:
        """Envoie un message à un utilisateur"""
        return {"success": True}


class FreshdeskIntegration(BaseIntegration):
    """Intégration Freshdesk"""
    
    def __init__(self):
        super().__init__(
            name="Freshdesk",
            icon="🎫",
            description="Helpdesk et gestion de tickets"
        )
        self.base_url = "https://domain.freshdesk.com/api/v2"
    
    def get_required_credentials(self) -> List[Dict[str, str]]:
        return [
            {"name": "domain", "label": "Freshdesk Domain", "type": "text", "required": True},
            {"name": "api_key", "label": "API Key", "type": "password", "required": True}
        ]

