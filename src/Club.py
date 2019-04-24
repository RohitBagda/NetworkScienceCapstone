class Club:
    def __init__(self, club_id, club_name):
        self.club_id = club_id
        self.club_name = club_name

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.club_id == other.club_id
        return False

    def __ne__(self, other):
        if isinstance(other, self.__class__):
            return self.club_id != other.club_id
        return False

    def __str__(self):
        return str(self.club_id)

    def __hash__(self):
        return hash(str(self))