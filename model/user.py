from dataclasses import dataclass

@dataclass
class User:
    user_id : str
    votes_funny : int
    votes_useful : int
    votes_cool : int
    name : str
    average_stars : float
    review_count : int
    n_bus_reviewed : int = 0

    def __str__(self):
        return f"{self.name} ({self.user_id})"

    def __eq__(self, other):
        return self.user_id == other.user_id

    def __hash__(self):
        return hash(self.user_id)

    def __repr__(self):
        return self.__str__()