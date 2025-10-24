"""
Classe de base pour toutes les intégrations
"""

from enum import Enum
from typing import Dict, Any, Optional, List
from datetime import datetime
import aiohttp


class IntegrationStatus(Enum):
    CONNECTED = "connected"
    DISCONNECTED = "disconnected"
    ERROR = "error"
    PENDING = "pending"


class BaseIntegration:
    """Classe de base pour toutes les intégrations externes"""
    
    def __init__(self, name: str, icon: str, description: str):
        self.name = name
        self.icon = icon
        self.description = description
        self.status = IntegrationStatus.DISCONNECTED
        self.api_key: Optional[str] = None
        self.credentials: Dict[str, Any] = {}
        self.last_sync: Optional[datetime] = None
        self.error_message: Optional[str] = None
        
    def configure(self, credentials: Dict[str, Any]) -> bool:
        """Configure l'intégration avec les credentials"""
        self.credentials = credentials
        self.api_key = credentials.get('api_key')
        return True
    
    async def connect(self) -> bool:
        """Établit la connexion avec le service externe"""
        try:
            is_valid = await self.validate_credentials()
            if is_valid:
                self.status = IntegrationStatus.CONNECTED
                self.last_sync = datetime.now()
                return True
            else:
                self.status = IntegrationStatus.ERROR
                self.error_message = "Invalid credentials"
                return False
        except Exception as e:
            self.status = IntegrationStatus.ERROR
            self.error_message = str(e)
            return False
    
    async def disconnect(self) -> bool:
        """Déconnecte l'intégration"""
        self.status = IntegrationStatus.DISCONNECTED
        self.api_key = None
        self.credentials = {}
        return True
    
    async def validate_credentials(self) -> bool:
        """Valide les credentials avec l'API externe"""
        # À implémenter dans les classes filles
        return True
    
    async def test_connection(self) -> Dict[str, Any]:
        """Test la connexion à l'API"""
        try:
            is_connected = await self.connect()
            return {
                "success": is_connected,
                "status": self.status.value,
                "message": self.error_message if not is_connected else "Connection successful"
            }
        except Exception as e:
            return {
                "success": False,
                "status": "error",
                "message": str(e)
            }
    
    def get_status(self) -> Dict[str, Any]:
        """Retourne le statut de l'intégration"""
        return {
            "name": self.name,
            "icon": self.icon,
            "status": self.status.value,
            "last_sync": self.last_sync.isoformat() if self.last_sync else None,
            "error_message": self.error_message,
            "is_configured": bool(self.credentials)
        }
    
    def get_required_credentials(self) -> List[Dict[str, str]]:
        """Retourne la liste des credentials requis"""
        return [
            {
                "name": "api_key",
                "label": "API Key",
                "type": "password",
                "required": True
            }
        ]
    
    async def make_api_call(self, method: str, url: str, **kwargs) -> Dict[str, Any]:
        """Effectue un appel API générique"""
        async with aiohttp.ClientSession() as session:
            async with session.request(method, url, **kwargs) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    raise Exception(f"API call failed with status {response.status}")

