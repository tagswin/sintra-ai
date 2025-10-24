"""
Classe de base pour tous les outils
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List


class BaseTool(ABC):
    """
    Classe de base abstraite pour tous les outils de l'agent
    """
    
    def __init__(self):
        self.name = self.__class__.__name__
        self.usage_count = 0
    
    @property
    @abstractmethod
    def description(self) -> str:
        """Description de ce que fait l'outil"""
        pass
    
    @property
    @abstractmethod
    def parameters(self) -> Dict[str, Any]:
        """
        Schéma des paramètres attendus
        Format: {"param_name": {"type": "string", "description": "...", "required": True}}
        """
        pass
    
    @abstractmethod
    async def execute(self, **kwargs) -> Any:
        """
        Exécute l'outil avec les paramètres donnés
        """
        pass
    
    def validate_parameters(self, **kwargs) -> bool:
        """
        Valide les paramètres fournis
        """
        for param_name, param_spec in self.parameters.items():
            if param_spec.get("required", False) and param_name not in kwargs:
                raise ValueError(f"Paramètre requis manquant: {param_name}")
        return True
    
    async def run(self, **kwargs) -> Any:
        """
        Wrapper qui valide puis exécute
        """
        self.validate_parameters(**kwargs)
        self.usage_count += 1
        return await self.execute(**kwargs)
    
    def get_info(self) -> Dict[str, Any]:
        """
        Retourne les informations sur l'outil
        """
        return {
            "name": self.name,
            "description": self.description,
            "parameters": self.parameters,
            "usage_count": self.usage_count
        }

