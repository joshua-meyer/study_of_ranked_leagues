from lib.matches.base_match import BaseMatch

class StrongestWinsMatch(BaseMatch):

    def determine_winner(self):
        strongest1 = max(self.team1.values())
        strongest2 = max(self.team2.values())
        if strongest1 >= strongest2:
            return 1
        else:
            return 2
