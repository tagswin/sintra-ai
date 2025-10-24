"""
Outil de calcul mathématique
"""

import logging
import ast
import operator
from typing import Any, Dict

from .base import BaseTool

logger = logging.getLogger(__name__)


class CalculatorTool(BaseTool):
    """
    Outil pour effectuer des calculs mathématiques
    """
    
    # Opérations autorisées
    ALLOWED_OPERATORS = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.FloorDiv: operator.floordiv,
        ast.Mod: operator.mod,
        ast.Pow: operator.pow,
        ast.UAdd: operator.pos,
        ast.USub: operator.neg,
    }
    
    @property
    def description(self) -> str:
        return "Effectue des calculs mathématiques sécurisés"
    
    @property
    def parameters(self) -> Dict[str, Any]:
        return {
            "expression": {
                "type": "string",
                "description": "Expression mathématique à évaluer (ex: '2 + 2', '10 * 5 + 3')",
                "required": True
            }
        }
    
    async def execute(self, expression: str) -> Dict[str, Any]:
        """
        Évalue une expression mathématique de manière sécurisée
        """
        logger.info(f"🔢 Calcul: {expression}")
        
        try:
            # Parser l'expression
            tree = ast.parse(expression, mode='eval')
            
            # Évaluer de manière sécurisée
            result = self._eval_node(tree.body)
            
            return {
                "success": True,
                "expression": expression,
                "result": result
            }
            
        except Exception as e:
            logger.error(f"Erreur de calcul: {str(e)}")
            return {
                "success": False,
                "expression": expression,
                "error": str(e)
            }
    
    def _eval_node(self, node):
        """
        Évalue un nœud AST de manière sécurisée
        """
        if isinstance(node, ast.Constant):
            return node.value
        
        elif isinstance(node, ast.Num):  # Pour compatibilité Python < 3.8
            return node.n
        
        elif isinstance(node, ast.BinOp):
            left = self._eval_node(node.left)
            right = self._eval_node(node.right)
            op_type = type(node.op)
            
            if op_type not in self.ALLOWED_OPERATORS:
                raise ValueError(f"Opération non autorisée: {op_type}")
            
            return self.ALLOWED_OPERATORS[op_type](left, right)
        
        elif isinstance(node, ast.UnaryOp):
            operand = self._eval_node(node.operand)
            op_type = type(node.op)
            
            if op_type not in self.ALLOWED_OPERATORS:
                raise ValueError(f"Opération non autorisée: {op_type}")
            
            return self.ALLOWED_OPERATORS[op_type](operand)
        
        elif isinstance(node, ast.Compare):
            # Pour supporter les comparaisons
            left = self._eval_node(node.left)
            comparisons = []
            
            for op, comparator in zip(node.ops, node.comparators):
                right = self._eval_node(comparator)
                
                if isinstance(op, ast.Lt):
                    comparisons.append(left < right)
                elif isinstance(op, ast.LtE):
                    comparisons.append(left <= right)
                elif isinstance(op, ast.Gt):
                    comparisons.append(left > right)
                elif isinstance(op, ast.GtE):
                    comparisons.append(left >= right)
                elif isinstance(op, ast.Eq):
                    comparisons.append(left == right)
                elif isinstance(op, ast.NotEq):
                    comparisons.append(left != right)
                else:
                    raise ValueError(f"Comparateur non autorisé: {type(op)}")
                
                left = right
            
            return all(comparisons)
        
        else:
            raise ValueError(f"Type de nœud non autorisé: {type(node)}")

