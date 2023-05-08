from abc import ABC, abstractmethod

class Index(ABC):
    """
    """
    def __init__(self, score: int) -> None:
        self.score = score
