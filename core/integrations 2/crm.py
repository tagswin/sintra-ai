"""
Intégrations CRM
"""

from typing import Dict, Any, List
from .base import BaseIntegration


class SalesforceIntegration(BaseIntegration):
    """Intégration Salesforce"""
    
    def __init__(self):
        super().__init__(
            name="Salesforce",
            icon="☁️",
            description="CRM et gestion des ventes"
        )
        self.base_url = "https://login.salesforce.com/services/oauth2"
    
    def get_required_credentials(self) -> List[Dict[str, str]]:
        return [
            {"name": "client_id", "label": "Client ID", "type": "text", "required": True},
            {"name": "client_secret", "label": "Client Secret", "type": "password", "required": True},
            {"name": "username", "label": "Username", "type": "text", "required": True},
            {"name": "password", "label": "Password", "type": "password", "required": True}
        ]


class HubSpotIntegration(BaseIntegration):
    """Intégration HubSpot"""
    
    def __init__(self):
        super().__init__(
            name="HubSpot",
            icon="🟠",
            description="CRM, marketing et sales automation"
        )
        self.base_url = "https://api.hubapi.com"
    
    def get_required_credentials(self) -> List[Dict[str, str]]:
        return [
            {"name": "api_key", "label": "API Key", "type": "password", "required": True}
        ]
    
    async def create_contact(self, email: str, properties: Dict[str, Any]) -> Dict[str, Any]:
        """Crée un contact"""
        return {"success": True, "contact_id": "mock_123"}


class PipedriveIntegration(BaseIntegration):
    """Intégration Pipedrive"""
    
    def __init__(self):
        super().__init__(
            name="Pipedrive",
            icon="🔵",
            description="Pipeline de ventes et gestion des deals"
        )
        self.base_url = "https://api.pipedrive.com/v1"
    
    def get_required_credentials(self) -> List[Dict[str, str]]:
        return [
            {"name": "api_token", "label": "API Token", "type": "password", "required": True}
        ]

