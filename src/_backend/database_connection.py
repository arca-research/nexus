from __future__ import annotations
from pathlib import Path
from typing import Optional, Literal
from abc import abstractmethod, ABC
from ...config import log
from .._schemas import (
    RelationshipRecord,
    ClaimData,
    AliasConflictError,
    EntityNotFoundError,
    RelationshipCollisionError,
    RelationshipMergeConflict,
    DeletionConflict
)

class Graph_Index_Connection(ABC):
    """
    An abstract class to connect to a graph database connection
    """

    @abstractmethod
    def __init__(self, index_path: str | Path):
        self.index_path = Path(index_path)

    @abstractmethod
    def execute(self, query: str, params: tuple):
        """Execute query and return result"""
        pass

