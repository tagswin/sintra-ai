"""
Intégrations pour l'analytics
"""

from typing import Dict, Any, List
from .base import BaseIntegration


class GoogleAnalyticsIntegration(BaseIntegration):
    """Intégration Google Analytics 4"""
    
    def __init__(self):
        super().__init__(
            name="Google Analytics",
            icon="📊",
            description="Analyser le trafic et le comportement utilisateur"
        )
        self.base_url = "https://analyticsdata.googleapis.com/v1beta"
    
    def get_required_credentials(self) -> List[Dict[str, str]]:
        return [
            {"name": "property_id", "label": "GA4 Property ID", "type": "text", "required": True},
            {"name": "credentials_json", "label": "Service Account JSON", "type": "textarea", "required": True}
        ]
    
    async def get_traffic_data(self, start_date: str, end_date: str) -> Dict[str, Any]:
        """Récupère les données de trafic"""
        return {
            "sessions": 0,
            "users": 0,
            "pageviews": 0,
            "bounce_rate": 0.0
        }


class MixpanelIntegration(BaseIntegration):
    """Intégration Mixpanel"""
    
    def __init__(self):
        super().__init__(
            name="Mixpanel",
            icon="📉",
            description="Analytics produit et tracking d'événements"
        )
        self.base_url = "https://mixpanel.com/api"
    
    def get_required_credentials(self) -> List[Dict[str, str]]:
        return [
            {"name": "project_id", "label": "Project ID", "type": "text", "required": True},
            {"name": "api_secret", "label": "API Secret", "type": "password", "required": True}
        ]


class AmplitudeIntegration(BaseIntegration):
    """Intégration Amplitude"""
    
    def __init__(self):
        super().__init__(
            name="Amplitude",
            icon="📱",
            description="Analytics comportementale et rétention"
        )
        self.base_url = "https://amplitude.com/api/2"
    
    def get_required_credentials(self) -> List[Dict[str, str]]:
        return [
            {"name": "api_key", "label": "API Key", "type": "password", "required": True},
            {"name": "secret_key", "label": "Secret Key", "type": "password", "required": True}
        ]

