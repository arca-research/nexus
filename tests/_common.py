from ..src.build import VectorDBBuilder, GraphBuilder
from ..src.query import VectorQueryEngine, GraphQueryEngine
from ..src.state import GraphIndex
from ..config import GraphConfig, VectorDBConfig, LLMConfig
from dataclasses import dataclass
from pathlib import Path

@dataclass
class DocData:
    """Container for document information."""
    document_id: int
    filepath: Path | str

GRAPH_CONFIG = GraphConfig()
GRAPH_BUILDER = GraphBuilder(debug=True)
LLM_CONFIG = LLMConfig()
