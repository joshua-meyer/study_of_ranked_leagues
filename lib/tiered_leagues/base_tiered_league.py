import string
from random import shuffle

from lib.base import *
from lib.matches.base_match import BaseMatch

class BaseTieredLeague():
    NUMBER_OF_LEAGUES = 3
    NUMBER_OF_TIERS = 3
    PLAYERS_PER_TEAM = 2
    MATCH = BaseMatch
    POINTS_PER_MATCH = 1
    POINTS_FOR_PROMOTION = 10

    def __init__(self, player_generator):
        self.player_generator = player_generator
        self.player_base = player_generator.player_base
        self.tiered_league = {}
        for league in range(0, self.NUMBER_OF_LEAGUES):
            self.tiered_league[league] = {}
            for tier in range(0, self.NUMBER_OF_TIERS):
                self.tiered_league[league][tier] = {}
        self.perform_initial_placement()

    def perform_initial_placement(self):
        for player in self.player_base.keys():
            self.tiered_league[self.NUMBER_OF_LEAGUES - 1][self.NUMBER_OF_TIERS - 1][player] = 0

    def print_summary(self):
        for league_rank, tiers in self.tiered_league.iteritems():
            print "league " + str(league_rank) + ":"
            for tier_rank, tier in tiers.iteritems():
                print "\ttier " + str(tier_rank) + ":"
                print "\t\tplayers == " + str(len(tier))
                total_points_in_tier = sum(tier.values())
                print "\t\tpoints == " + str(total_points_in_tier)

    def do_an_iteration(self):
        for league_rank, tiers in self.tiered_league.iteritems():
            for tier_rank, tier in tiers.iteritems():
                self.do_round(league_rank, tier_rank, tier)
        self.apply_tier_adjustments()

    def do_round(self, league_rank, tier_rank, tier):
        matches = self.construct_matches(tier.keys())
        for matchup in matches:
            team1 = matchup[1]
            team2 = matchup[2]
            match = self.MATCH(team1, team2)
            winner = match.winner()
            loser = match.loser()
            for winning_player in matchup[winner].keys():
                self.tiered_league[league_rank][tier_rank][winning_player] += self.POINTS_PER_MATCH
            for losing_player in matchup[loser].keys():
                self.tiered_league[league_rank][tier_rank][losing_player] -= self.POINTS_PER_MATCH

    def construct_matches(self, players):
        matches = []
        shuffle(players)
        while len(players) >= self.PLAYERS_PER_TEAM*2:
            players_for_match = []
            while len(players_for_match) < self.PLAYERS_PER_TEAM*2:
                new_player = players.pop()
                players_for_match.append(new_player)
            shuffle(players_for_match)
            matchup = { 1: {}, 2: {} }
            while len(players_for_match) > self.PLAYERS_PER_TEAM:
                next_player = players_for_match.pop()
                matchup[1][next_player] = self.player_base[next_player]
            while len(players_for_match) > 0:
                next_player = players_for_match.pop()
                matchup[2][next_player] = self.player_base[next_player]
            matches.append(matchup)
        return matches

    def apply_tier_adjustments(self):
        new_tiered_league = {}
        for league in range(0, self.NUMBER_OF_LEAGUES):
            new_tiered_league[league] = {}
            for tier in range(0, self.NUMBER_OF_TIERS):
                new_tiered_league[league][tier] = {}
        for league_rank, tiers in self.tiered_league.iteritems():
            for tier_rank, tier in tiers.iteritems():
                for player, points in tier.iteritems():
                    self.migrate_player(new_tiered_league, league_rank, tier_rank, player, points)
        self.tiered_league = new_tiered_league

    def migrate_player(self, new_tiered_league, league_rank, tier_rank, player_name, points):
        if points < 0:
            if tier_rank + 1 == self.NUMBER_OF_TIERS:
                if league_rank + 1 == self.NUMBER_OF_LEAGUES:
                    new_league = league_rank
                    new_tier = tier_rank
                    new_points = 0
                else:
                    new_league = league_rank + 1
                    new_tier = 0
                    new_points = self.POINTS_FOR_PROMOTION
            else:
                new_league = league_rank
                new_tier = tier_rank + 1
                new_points = self.POINTS_FOR_PROMOTION
        elif points >= self.POINTS_FOR_PROMOTION:
            if tier_rank - 1 < 0:
                if league_rank - 1 < 0:
                    new_league = league_rank
                    new_tier = tier_rank
                    new_points = points
                else:
                    new_league = league_rank - 1
                    new_tier = self.NUMBER_OF_TIERS - 1
                    new_points = 0
            else:
                new_league = league_rank
                new_tier = tier_rank - 1
                new_points = 0
        else:
            new_league = league_rank
            new_tier = tier_rank
            new_points = points
        new_tiered_league[new_league][new_tier][player_name] = new_points
