"""
Intégrations email marketing
"""

from typing import Dict, Any, List
from .base import BaseIntegration


class MailchimpIntegration(BaseIntegration):
    """Intégration Mailchimp"""
    
    def __init__(self):
        super().__init__(
            name="Mailchimp",
            icon="📧",
            description="Email marketing et automation"
        )
    
    def get_required_credentials(self) -> List[Dict[str, str]]:
        return [
            {"name": "api_key", "label": "API Key", "type": "password", "required": True},
            {"name": "server_prefix", "label": "Server Prefix (us1, us2, etc.)", "type": "text", "required": True}
        ]
    
    async def create_campaign(self, list_id: str, subject: str, content: str) -> Dict[str, Any]:
        """Crée une campagne email"""
        return {"success": True, "campaign_id": "mock_123"}


class SendGridIntegration(BaseIntegration):
    """Intégration SendGrid"""
    
    def __init__(self):
        super().__init__(
            name="SendGrid",
            icon="✉️",
            description="Envoi d'emails transactionnels et marketing"
        )
        self.base_url = "https://api.sendgrid.com/v3"
    
    def get_required_credentials(self) -> List[Dict[str, str]]:
        return [
            {"name": "api_key", "label": "API Key", "type": "password", "required": True}
        ]
    
    async def send_email(self, to: str, subject: str, content: str) -> Dict[str, Any]:
        """Envoie un email"""
        return {"success": True, "message_id": "mock_123"}


class BrevoIntegration(BaseIntegration):
    """Intégration Brevo (ex-Sendinblue)"""
    
    def __init__(self):
        super().__init__(
            name="Brevo",
            icon="💌",
            description="Email marketing et SMS"
        )
        self.base_url = "https://api.brevo.com/v3"
    
    def get_required_credentials(self) -> List[Dict[str, str]]:
        return [
            {"name": "api_key", "label": "API Key", "type": "password", "required": True}
        ]

