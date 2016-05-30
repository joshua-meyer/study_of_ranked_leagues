from lib.base import *
from lib.player_generators.base_player_generator import BasePlayerGenerator
from lib.matches.weakest_proportional_chance_match import WeakestProportionalChanceMatch
from lib.tiered_leagues.base_tiered_league import BaseTieredLeague

from sys import argv
if len(argv) < 2:
    baseline_strength = 0
else:
    baseline_strength = int(argv[1])

pb = BasePlayerGenerator(10000, baseline_strength)
tl = BaseTieredLeague(pb, WeakestProportionalChanceMatch)

for i in range(0, 100):
    tl.do_an_iteration()
tl.print_summary()
