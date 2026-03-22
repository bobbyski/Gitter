from dataclasses import dataclass
from BusinessLogic.GitManager import GitManager

@dataclass
class Issue:
    number: str
    title: str