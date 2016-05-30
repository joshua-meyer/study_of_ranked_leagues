from lib.base import *

class BaseMatch():

    def __init__(self, team1, team2):
        self.team1 = team1
        self.team2 = team2
        self.w = None
        self.l = None

    def winner(self):
        if self.w is None:
            self.w = self.determine_winner()
        return self.w

    def determine_winner(self):
        return 1

    def loser(self):
        if self.l is None:
            if self.winner() == 1:
                self.l = 2
            else:
                self.l = 1
        return self.l
