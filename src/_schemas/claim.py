from dataclasses import dataclass, field
from typing import Optional

@dataclass
class ClaimData:
    content: str
    source: str
    date_added: str
    source_date: Optional[str] = None
    claim_date: Optional[str] = None
    entities: list[str] = field(default_factory=list)