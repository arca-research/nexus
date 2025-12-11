from dataclasses import dataclass, field

@dataclass
class ClaimData:
    content: str
    source: str
    date_added: str
    claim_date: str
    entities: list[str] = field(default_factory=list)