"""
Outil pour les opérations sur les fichiers
"""

import os
import logging
from typing import Any, Dict
import aiofiles

from .base import BaseTool

logger = logging.getLogger(__name__)


class FileOperationsTool(BaseTool):
    """
    Outil pour lire, écrire et manipuler des fichiers
    """
    
    def __init__(self, workspace_dir: str = "./workspace"):
        super().__init__()
        self.workspace_dir = workspace_dir
        os.makedirs(workspace_dir, exist_ok=True)
    
    @property
    def description(self) -> str:
        return "Effectue des opérations sur les fichiers (lecture, écriture, liste)"
    
    @property
    def parameters(self) -> Dict[str, Any]:
        return {
            "operation": {
                "type": "string",
                "description": "Type d'opération: read, write, list, delete",
                "required": True
            },
            "path": {
                "type": "string",
                "description": "Chemin du fichier ou dossier",
                "required": True
            },
            "content": {
                "type": "string",
                "description": "Contenu à écrire (pour write)",
                "required": False
            }
        }
    
    async def execute(
        self,
        operation: str,
        path: str,
        content: str = None
    ) -> Dict[str, Any]:
        """
        Exécute une opération sur un fichier
        """
        # Sécurité: s'assurer que le chemin est dans le workspace
        full_path = os.path.join(self.workspace_dir, path)
        full_path = os.path.abspath(full_path)
        
        if not full_path.startswith(os.path.abspath(self.workspace_dir)):
            return {
                "success": False,
                "error": "Accès refusé: chemin en dehors du workspace"
            }
        
        try:
            if operation == "read":
                return await self._read_file(full_path)
            elif operation == "write":
                return await self._write_file(full_path, content)
            elif operation == "list":
                return await self._list_directory(full_path)
            elif operation == "delete":
                return await self._delete_file(full_path)
            else:
                return {
                    "success": False,
                    "error": f"Opération non supportée: {operation}"
                }
        except Exception as e:
            logger.error(f"Erreur lors de l'opération {operation}: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def _read_file(self, path: str) -> Dict[str, Any]:
        """Lit un fichier"""
        if not os.path.exists(path):
            return {
                "success": False,
                "error": "Fichier non trouvé"
            }
        
        async with aiofiles.open(path, 'r', encoding='utf-8') as f:
            content = await f.read()
        
        return {
            "success": True,
            "operation": "read",
            "path": path,
            "content": content,
            "size": len(content)
        }
    
    async def _write_file(self, path: str, content: str) -> Dict[str, Any]:
        """Écrit dans un fichier"""
        if content is None:
            return {
                "success": False,
                "error": "Contenu requis pour l'opération write"
            }
        
        # Créer les dossiers parents si nécessaire
        os.makedirs(os.path.dirname(path), exist_ok=True)
        
        async with aiofiles.open(path, 'w', encoding='utf-8') as f:
            await f.write(content)
        
        return {
            "success": True,
            "operation": "write",
            "path": path,
            "bytes_written": len(content)
        }
    
    async def _list_directory(self, path: str) -> Dict[str, Any]:
        """Liste le contenu d'un dossier"""
        if not os.path.exists(path):
            return {
                "success": False,
                "error": "Dossier non trouvé"
            }
        
        if not os.path.isdir(path):
            return {
                "success": False,
                "error": "Le chemin n'est pas un dossier"
            }
        
        items = []
        for item in os.listdir(path):
            item_path = os.path.join(path, item)
            items.append({
                "name": item,
                "type": "directory" if os.path.isdir(item_path) else "file",
                "size": os.path.getsize(item_path) if os.path.isfile(item_path) else 0
            })
        
        return {
            "success": True,
            "operation": "list",
            "path": path,
            "items": items,
            "count": len(items)
        }
    
    async def _delete_file(self, path: str) -> Dict[str, Any]:
        """Supprime un fichier"""
        if not os.path.exists(path):
            return {
                "success": False,
                "error": "Fichier non trouvé"
            }
        
        os.remove(path)
        
        return {
            "success": True,
            "operation": "delete",
            "path": path
        }

