from dataclasses import dataclass

@dataclass
class Spigolo:
    id1: str
    id2: str
    comuni: int

    def __str__(self):
        return f"{self.id1} {self.id2}"
    def __repr__(self):
        return self.__str__()