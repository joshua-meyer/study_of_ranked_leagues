import string
from random import shuffle

from lib.base import *
from lib.matches.base_match import BaseMatch

class BaseTieredLeague():

    def __init__(self, player_generator, match_class,
            number_of_leagues = 3, number_of_tiers = 3,
            points_per_match = 1, points_for_promotion = 10,
            players_per_team = 5):
        self.player_generator = player_generator
        self.match_class = match_class
        self.number_of_leagues = number_of_leagues
        self.number_of_tiers = number_of_tiers
        self.points_per_match = points_per_match
        self.points_for_promotion = points_for_promotion
        self.players_per_team = players_per_team
        self.player_base = player_generator.player_base
        self.tiered_league = {}
        for league in range(0, self.number_of_leagues):
            self.tiered_league[league] = {}
            for tier in range(0, self.number_of_tiers):
                self.tiered_league[league][tier] = {}
        self.perform_initial_placement()

    def perform_initial_placement(self):
        for player in self.player_base.keys():
            self.tiered_league[self.number_of_leagues - 1][self.number_of_tiers - 1][player] = 0

    def print_summary(self):
        for league_rank, tiers in self.tiered_league.iteritems():
            print "league " + str(league_rank) + ":"
            for tier_rank, tier in tiers.iteritems():
                print "\ttier " + str(tier_rank) + ":"
                num_players = len(tier)
                print "\t\tplayers == " + str(num_players)
                if num_players == 0:
                    average_strength = -1
                else:
                    total_strength = 0
                    for player in tier.keys():
                        player_strength = self.player_base[player]
                        total_strength += player_strength
                    average_strength = total_strength / num_players
                print "\t\taverage strength == " + str(average_strength)

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
            match = self.match_class(team1, team2)
            winner = match.winner()
            loser = match.loser()
            for winning_player in matchup[winner].keys():
                self.tiered_league[league_rank][tier_rank][winning_player] += self.points_per_match
            for losing_player in matchup[loser].keys():
                self.tiered_league[league_rank][tier_rank][losing_player] -= self.points_per_match

    def construct_matches(self, players):
        matches = []
        shuffle(players)
        while len(players) >= self.players_per_team*2:
            players_for_match = []
            while len(players_for_match) < self.players_per_team*2:
                new_player = players.pop()
                players_for_match.append(new_player)
            shuffle(players_for_match)
            matchup = { 1: {}, 2: {} }
            while len(players_for_match) > self.players_per_team:
                next_player = players_for_match.pop()
                matchup[1][next_player] = self.player_base[next_player]
            while len(players_for_match) > 0:
                next_player = players_for_match.pop()
                matchup[2][next_player] = self.player_base[next_player]
            matches.append(matchup)
        return matches

    def apply_tier_adjustments(self):
        new_tiered_league = {}
        for league in range(0, self.number_of_leagues):
            new_tiered_league[league] = {}
            for tier in range(0, self.number_of_tiers):
                new_tiered_league[league][tier] = {}
        for league_rank, tiers in self.tiered_league.iteritems():
            for tier_rank, tier in tiers.iteritems():
                for player, points in tier.iteritems():
                    self.migrate_player(new_tiered_league, league_rank, tier_rank, player, points)
        self.tiered_league = new_tiered_league

    def migrate_player(self, new_tiered_league, league_rank, tier_rank, player_name, points):
        if points < 0:
            if tier_rank + 1 == self.number_of_tiers:
                if league_rank + 1 == self.number_of_leagues:
                    new_league = league_rank
                    new_tier = tier_rank
                    new_points = 0
                else:
                    new_league = league_rank + 1
                    new_tier = 0
                    new_points = self.points_for_promotion
            else:
                new_league = league_rank
                new_tier = tier_rank + 1
                new_points = self.points_for_promotion
        elif points >= self.points_for_promotion:
            if tier_rank - 1 < 0:
                if league_rank - 1 < 0:
                    new_league = league_rank
                    new_tier = tier_rank
                    new_points = points
                else:
                    new_league = league_rank - 1
                    new_tier = self.number_of_tiers - 1
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
