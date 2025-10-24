"""
Outil d'exécution de code
"""

import asyncio
import logging
import subprocess
import tempfile
import os
from typing import Any, Dict

from .base import BaseTool

logger = logging.getLogger(__name__)


class CodeExecutorTool(BaseTool):
    """
    Outil pour exécuter du code dans un environnement sécurisé
    """
    
    @property
    def description(self) -> str:
        return "Exécute du code Python dans un environnement sécurisé et retourne le résultat"
    
    @property
    def parameters(self) -> Dict[str, Any]:
        return {
            "code": {
                "type": "string",
                "description": "Le code Python à exécuter",
                "required": True
            },
            "timeout": {
                "type": "integer",
                "description": "Timeout en secondes",
                "required": False,
                "default": 30
            }
        }
    
    async def execute(self, code: str, timeout: int = 30) -> Dict[str, Any]:
        """
        Exécute du code Python
        
        ATTENTION: Cette implémentation est basique.
        En production, utilisez un sandbox approprié:
        - Docker container
        - VM isolée
        - Service tiers comme Judge0, Piston, etc.
        """
        logger.info(f"💻 Exécution de code Python ({len(code)} caractères)")
        
        # Vérifications de sécurité basiques
        forbidden_imports = ['os', 'subprocess', 'sys', '__import__', 'eval', 'exec']
        for forbidden in forbidden_imports:
            if forbidden in code.lower():
                return {
                    "success": False,
                    "error": f"Import interdit détecté: {forbidden}",
                    "output": "",
                    "code": code
                }
        
        try:
            # Créer un fichier temporaire
            with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
                f.write(code)
                temp_file = f.name
            
            try:
                # Exécuter le code
                process = await asyncio.create_subprocess_exec(
                    'python3', temp_file,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE
                )
                
                try:
                    stdout, stderr = await asyncio.wait_for(
                        process.communicate(),
                        timeout=timeout
                    )
                    
                    output = stdout.decode('utf-8')
                    error = stderr.decode('utf-8')
                    
                    return {
                        "success": process.returncode == 0,
                        "output": output,
                        "error": error if error else None,
                        "return_code": process.returncode,
                        "code": code
                    }
                    
                except asyncio.TimeoutError:
                    process.kill()
                    return {
                        "success": False,
                        "error": f"Timeout: l'exécution a dépassé {timeout} secondes",
                        "output": "",
                        "code": code
                    }
            finally:
                # Nettoyer le fichier temporaire
                os.unlink(temp_file)
                
        except Exception as e:
            logger.error(f"Erreur lors de l'exécution: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "output": "",
                "code": code
            }
    
    def validate_code(self, code: str) -> Dict[str, Any]:
        """
        Valide la syntaxe du code sans l'exécuter
        """
        try:
            compile(code, '<string>', 'exec')
            return {
                "valid": True,
                "message": "Code syntaxiquement valide"
            }
        except SyntaxError as e:
            return {
                "valid": False,
                "error": str(e),
                "line": e.lineno
            }

