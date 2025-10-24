"""
Registre des outils disponibles
"""

import logging
from typing import Dict, List, Optional, Any

from .base import BaseTool
from .web_search import WebSearchTool
from .code_executor import CodeExecutorTool
from .file_operations import FileOperationsTool
from .calculator import CalculatorTool

logger = logging.getLogger(__name__)


class ToolRegistry:
    """
    Registre centralisé de tous les outils disponibles pour l'agent
    """
    
    def __init__(self):
        self._tools: Dict[str, BaseTool] = {}
        self._initialize_default_tools()
    
    def _initialize_default_tools(self):
        """
        Initialise les outils par défaut
        """
        default_tools = [
            WebSearchTool(),
            CodeExecutorTool(),
            FileOperationsTool(),
            CalculatorTool()
        ]
        
        for tool in default_tools:
            self.register_tool(tool)
        
        logger.info(f"🔧 {len(self._tools)} outils enregistrés")
    
    def register_tool(self, tool: BaseTool):
        """
        Enregistre un nouvel outil
        """
        tool_name = tool.name.lower().replace("tool", "")
        self._tools[tool_name] = tool
        logger.debug(f"Outil enregistré: {tool_name}")
    
    def get_tool(self, tool_name: str) -> Optional[BaseTool]:
        """
        Récupère un outil par son nom
        """
        tool_name = tool_name.lower().replace("tool", "")
        return self._tools.get(tool_name)
    
    def list_tools(self) -> List[Dict[str, Any]]:
        """
        Liste tous les outils disponibles
        """
        return [tool.get_info() for tool in self._tools.values()]
    
    def get_tool_names(self) -> List[str]:
        """
        Retourne la liste des noms d'outils
        """
        return list(self._tools.keys())
    
    async def execute_tool(self, tool_name: str, **kwargs) -> Any:
        """
        Exécute un outil par son nom
        """
        tool = self.get_tool(tool_name)
        
        if not tool:
            raise ValueError(f"Outil non trouvé: {tool_name}")
        
        return await tool.run(**kwargs)

