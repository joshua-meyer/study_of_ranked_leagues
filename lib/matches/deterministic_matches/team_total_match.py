from lib.matches.base_match import BaseMatch

class TeamTotalMatch(BaseMatch):

    def determine_winner(self):
        total1 = sum(self.team1.values())
        total2 = sum(self.team2.values())
        if total1 >= total2:
            return 1
        else:
            return 2
